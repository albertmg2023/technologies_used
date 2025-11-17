package com.example.cameras2usb

import android.Manifest
import android.content.pm.PackageManager
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {

    private lateinit var cameraManager: CameraManager
    private var cameraStreamer: CameraStreamer? = null
    private val basePort = 5600

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        cameraManager = getSystemService(CAMERA_SERVICE) as CameraManager

        // Pedimos permisos si es necesario
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 1)
        } else {
            setupStreamer()
        }

        checkCameraCapabilities()

        val startBtn = findViewById<Button>(R.id.startButton)
        val stopBtn = findViewById<Button>(R.id.stopButton)

        startBtn.setOnClickListener {
            cameraStreamer?.startStreaming()
            Toast.makeText(this, "Streaming iniciado (ambas cámaras)", Toast.LENGTH_SHORT).show()
        }

        stopBtn.setOnClickListener {
            cameraStreamer?.stopStreaming()
            Toast.makeText(this, "Streaming detenido", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int, permissions: Array<String>, grantResults: IntArray
    ) {
        if (requestCode == 1 && grantResults.isNotEmpty()
            && grantResults[0] == PackageManager.PERMISSION_GRANTED
        ) {
            setupStreamer()
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
    }

    private fun setupStreamer() {
        val cameraIds = cameraManager.cameraIdList.take(2).toList() // Tomamos máximo 2 cámaras
        cameraStreamer = CameraStreamer(
            context = this,
            cameraIds = cameraIds,
            serverPort = basePort
        )
    }

    private fun checkCameraCapabilities() {
        val cameraIds = cameraManager.cameraIdList
        var canUseFrontAndBack = false

        for (id in cameraIds) {
            val characteristics = cameraManager.getCameraCharacteristics(id)
            val capabilities = characteristics.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES)
            val facing = characteristics.get(CameraCharacteristics.LENS_FACING)

            val facingStr = when (facing) {
                CameraCharacteristics.LENS_FACING_FRONT -> "Frontal"
                CameraCharacteristics.LENS_FACING_BACK -> "Trasera"
                CameraCharacteristics.LENS_FACING_EXTERNAL -> "Externa"
                else -> "Desconocida"
            }

            Log.d("CameraCheck", "Cámara ID=$id, tipo=$facingStr")
            capabilities?.forEach { cap ->
                val capName = when (cap) {
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_BACKWARD_COMPATIBLE -> "Compatibilidad backward"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_SENSOR -> "Sensor manual"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_POST_PROCESSING -> "Postprocesamiento manual"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_RAW -> "RAW"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_PRIVATE_REPROCESSING -> "Reprocesamiento privado"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_READ_SENSOR_SETTINGS -> "Lectura settings sensor"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_BURST_CAPTURE -> "Burst"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_YUV_REPROCESSING -> "YUV reprocessing"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_DEPTH_OUTPUT -> "Depth output"
                    CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_LOGICAL_MULTI_CAMERA -> "Logical multi-camera"
                    else -> "Otro ($cap)"
                }
                Log.d("CameraCheck", " - Capacidad: $capName")
            }

            // Verifica si hay frontal y trasera disponible
            if (facing == CameraCharacteristics.LENS_FACING_FRONT || facing == CameraCharacteristics.LENS_FACING_BACK) {
                canUseFrontAndBack = true
            }
        }

        if (canUseFrontAndBack) {
            Log.d("CameraCheck", "Se pueden usar frontal y trasera simultáneamente: POSIBLE")
        } else {
            Log.d("CameraCheck", "Se pueden usar frontal y trasera simultáneamente: NO")
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraStreamer?.stopStreaming()
    }
}
