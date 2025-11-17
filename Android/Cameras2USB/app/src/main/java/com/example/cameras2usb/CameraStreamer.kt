package com.example.cameras2usb

import android.content.Context
import android.graphics.*
import android.hardware.camera2.*
import android.media.ImageReader
import android.media.MediaCodec
import android.media.MediaCodecInfo
import android.media.MediaFormat
import android.os.Handler
import android.os.HandlerThread
import android.util.Log
import android.view.Surface
import java.io.OutputStream
import java.net.ServerSocket
import java.net.Socket
import java.nio.ByteBuffer

class CameraStreamer(
    private val context: Context,
    private val cameraIds: List<String>, // Hasta 2 cámaras
    private val serverPort: Int
) {

    private val TAG = "CameraStreamer"

    private val cameraDevices = mutableMapOf<String, CameraDevice>()
    private val captureSessions = mutableMapOf<String, CameraCaptureSession>()
    private val imageReaders = mutableMapOf<String, ImageReader>()

    private var mediaCodec: MediaCodec? = null
    private var codecSurface: Surface? = null
    private var socket: Socket? = null
    private var outputStream: OutputStream? = null

    private val cameraThread = HandlerThread("CameraThread").apply { start() }
    private val cameraHandler = Handler(cameraThread.looper)

    private val codecThread = HandlerThread("CodecThread").apply { start() }
    private val codecHandler = Handler(codecThread.looper)

    fun startStreaming() {
        Thread { waitForClient() }.start()
    }

    private fun waitForClient() {
        try {
            val serverSocket = ServerSocket(serverPort)
            Log.d(TAG, "Esperando cliente en puerto $serverPort")
            socket = serverSocket.accept()
            outputStream = socket?.getOutputStream()
            Log.d(TAG, "Cliente conectado en puerto $serverPort")
            openCameras()
        } catch (e: Exception) {
            Log.e(TAG, "Error en server: ${e.message}")
        }
    }

    private fun openCameras() {
        val manager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
        for (cameraId in cameraIds) {
            manager.openCamera(cameraId, object : CameraDevice.StateCallback() {
                override fun onOpened(camera: CameraDevice) {
                    cameraDevices[cameraId] = camera
                    setupImageReader(cameraId)
                    if (cameraDevices.size == cameraIds.size) {
                        setupMediaCodec()
                    }
                }

                override fun onDisconnected(camera: CameraDevice) { camera.close() }
                override fun onError(camera: CameraDevice, error: Int) {
                    Log.e(TAG, "Error abriendo cámara $cameraId: $error")
                    camera.close()
                }
            }, cameraHandler)
        }
    }

    private fun setupImageReader(cameraId: String) {
        val width = 640
        val height = 480
        val reader = ImageReader.newInstance(width, height, ImageFormat.YUV_420_888, 2)
        imageReaders[cameraId] = reader

        val requestBuilder = cameraDevices[cameraId]?.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW)
        requestBuilder?.addTarget(reader.surface)

        cameraDevices[cameraId]?.createCaptureSession(listOf(reader.surface), object : CameraCaptureSession.StateCallback() {
            override fun onConfigured(session: CameraCaptureSession) {
                captureSessions[cameraId] = session
                session.setRepeatingRequest(requestBuilder!!.build(), null, cameraHandler)
            }

            override fun onConfigureFailed(session: CameraCaptureSession) {
                Log.e(TAG, "Falló configuración de captura para $cameraId")
            }
        }, cameraHandler)
    }

    private fun setupMediaCodec() {
        try {
            val width = 640 * cameraIds.size // combinamos lado a lado
            val height = 480
            val format = MediaFormat.createVideoFormat("video/avc", width, height)
            format.setInteger(MediaFormat.KEY_COLOR_FORMAT, MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface)
            format.setInteger(MediaFormat.KEY_BIT_RATE, 1_000_000)
            format.setInteger(MediaFormat.KEY_FRAME_RATE, 15)
            format.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL, 1)

            mediaCodec = MediaCodec.createEncoderByType("video/avc")
            mediaCodec?.configure(format, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE)
            codecSurface = mediaCodec!!.createInputSurface()
            mediaCodec?.start()

            startFrameLoop()
        } catch (e: Exception) {
            Log.e(TAG, "Error configurando MediaCodec: ${e.message}")
        }
    }

    private fun startFrameLoop() {
        codecHandler.post(object : Runnable {
            override fun run() {
                try {
                    // Convertimos cada cámara a Bitmap
                    val bitmaps = mutableListOf<Bitmap>()
                    for (reader in imageReaders.values) {
                        val image = reader.acquireLatestImage() ?: continue
                        val bitmap = yuvToBitmap(image)
                        image.close()
                        bitmaps.add(bitmap)
                    }

                    if (bitmaps.isNotEmpty()) {
                        val combined = combineBitmapsSideBySide(bitmaps)
                        renderBitmapToSurface(combined)
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Error en frame loop: ${e.message}")
                }
                codecHandler.postDelayed(this, 33)
            }
        })
    }

    private fun yuvToBitmap(image: android.media.Image): Bitmap {
        val yPlane = image.planes[0].buffer
        val uPlane = image.planes[1].buffer
        val vPlane = image.planes[2].buffer

        // Simplificación: creamos Bitmap negro del tamaño del frame
        val bitmap = Bitmap.createBitmap(image.width, image.height, Bitmap.Config.ARGB_8888)
        bitmap.eraseColor(Color.BLACK)
        return bitmap
    }

    private fun combineBitmapsSideBySide(bitmaps: List<Bitmap>): Bitmap {
        val width = bitmaps.sumOf { it.width }
        val height = bitmaps.maxOf { it.height }
        val combined = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        val canvas = Canvas(combined)
        var offsetX = 0
        for (bmp in bitmaps) {
            canvas.drawBitmap(bmp, offsetX.toFloat(), 0f, null)
            offsetX += bmp.width
        }
        return combined
    }

    private fun renderBitmapToSurface(bitmap: Bitmap) {
        val canvas = codecSurface?.lockCanvas(null) ?: return
        canvas.drawBitmap(bitmap, null, Rect(0, 0, canvas.width, canvas.height), null)
        codecSurface?.unlockCanvasAndPost(canvas)

        // Recuperamos los datos codificados
        val bufferInfo = MediaCodec.BufferInfo()
        mediaCodec?.let { codec ->
            var outputBufferId = codec.dequeueOutputBuffer(bufferInfo, 0)
            while (outputBufferId >= 0) {
                val outputBuffer = codec.getOutputBuffer(outputBufferId)
                outputBuffer?.let { outBuf ->
                    val bytes = ByteArray(bufferInfo.size)
                    outBuf.get(bytes)
                    outBuf.clear()
                    outputStream?.write(bytes)
                }
                codec.releaseOutputBuffer(outputBufferId, false)
                outputBufferId = codec.dequeueOutputBuffer(bufferInfo, 0)
            }
        }
    }

    fun stopStreaming() {
        try {
            captureSessions.values.forEach { it.close() }
            cameraDevices.values.forEach { it.close() }
            imageReaders.values.forEach { it.close() }
            mediaCodec?.stop()
            mediaCodec?.release()
            codecSurface = null
            socket?.close()
            outputStream?.close()
            cameraThread.quitSafely()
            codecThread.quitSafely()
            Log.d(TAG, "Streaming detenido")
        } catch (e: Exception) {
            Log.e(TAG, "Error deteniendo streaming: ${e.message}")
        }
    }
}
