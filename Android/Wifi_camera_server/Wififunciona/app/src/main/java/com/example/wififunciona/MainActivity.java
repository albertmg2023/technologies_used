package com.example.wififunciona;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Build;
import android.Manifest;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.os.Environment;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.bluetooth.BluetoothAdapter;

import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Handler;
import android.os.Message;

import android.hardware.Camera;

import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Build;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import android.util.Log;
import android.widget.*;
import android.view.View;
import android.bluetooth.BluetoothAdapter;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
 public class MainActivity extends AppCompatActivity {
     //hilo
     NetworkExecutor networkExecutor;
     //inicializo carpeta y archivo donde se guardara la imagen de la camara
     public File mediaStorageDir;
     public File mediaFile;
     Camera.PictureCallback mPicture = new
             Camera.PictureCallback() {
                 @Override
                 public void onPictureTaken(byte[] data, Camera camera) {
                     byte[] resized = resizeImage(data);
                     File pictureFile = getOutputMediaFile();
                     if (pictureFile == null) {
                         return;
                     }
                     try {
                         FileOutputStream fos = new FileOutputStream(pictureFile);
                         fos.write(resized);
                         fos.close();
                     } catch (Exception e) {
                         Log.e("onPictureTaken", "ERROR:" + e);
                     }
                 }
             };

     FrameLayout cameraPreviewFrameLayout;
     android.hardware.Camera mCamera;
     CameraPreview mCameraPreview;
     public Handler handlerNetworkExecutorResult;

     @SuppressLint("MissingInflatedId")
     @Override
     protected void onCreate(Bundle savedInstanceState) {
         super.onCreate(savedInstanceState);
         setContentView(R.layout.activity_main);
         ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
             Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
             v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
             return insets;
         });
         handlerNetworkExecutorResult = new Handler(Looper.getMainLooper()) {
             @Override
             public void handleMessage(Message msg) {
                 Log.d("handlerNetworkExecutorResult", (String) msg.obj);
                 if (msg != null) {
                     if (msg.obj.equals("FORWARD")) {
                         forward();
                     } else if (msg.obj.equals("BACKWARD")) {
                         backward();
                     } else if (msg.obj.equals("LEFT")) {
                         left();
                     } else if (msg.obj.equals("RIGHT")) {
                         right();
                     } else if (msg.obj.equals("CAMERA")) {
                         captureCamera();
                     }
                 }
             }
         };
         networkExecutor = new NetworkExecutor(this, handlerNetworkExecutorResult);
         // Ejecutar NetworkExecutor en un hilo en segundo plano

         networkExecutor.start();

         cameraPreviewFrameLayout = (FrameLayout) findViewById(R.id.cameraView);
         if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
             ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.CAMERA}, 100);
         }

         mCamera = getCameraInstance();
         if (mCamera != null) {
             mCameraPreview = new CameraPreview(this, mCamera);
             if (cameraPreviewFrameLayout.getChildCount() == 0) {
                 cameraPreviewFrameLayout.addView(mCameraPreview);
             }
         } else {
             Log.e("CameraError", "No se pudo acceder a la cámara");
         }





     }
     private android.hardware.Camera getCameraInstance () {
         android.hardware.Camera camera = null;
         try {
             camera = android.hardware.Camera.open(0);
         } catch (Exception e) {
// cannot get camera or does not exist
             Log.d("getCameraInstance", "ERROR" + e);
         }
         return camera;
     }

     public File getOutputMediaFile () {
         if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
                 != PackageManager.PERMISSION_GRANTED) {
             ActivityCompat.requestPermissions(this,
                     new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 101);
         }
         if (mediaStorageDir == null) {
             mediaStorageDir = new
                     File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES), "MyCameraApp");
             if (!mediaStorageDir.exists()) {
                 if (!mediaStorageDir.mkdirs()) {
                     Log.d("MyCameraApp", "failed to create directory");
                     return null;
                 }
             }
         }
         if (mediaFile == null) {
             mediaFile = new File(mediaStorageDir.getPath() + File.separator + "IMG.jpg");
         }
         return mediaFile;
     }

     public void captureCamera () {
         if (mCamera != null) {
             mCamera.takePicture(null, null, mPicture);
         }
     }

     //redimensionar imagen y comprimirla con jpeg
     byte[] resizeImage ( byte[] input){
         Bitmap originalBitmap = BitmapFactory.decodeByteArray(input, 0, input.length);
         Bitmap resizedBitmap = Bitmap.createScaledBitmap(originalBitmap, 80, 107,
                 true);
         ByteArrayOutputStream blob = new ByteArrayOutputStream();
         resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 100, blob);
         return blob.toByteArray();
     }
     //mostrar mensajes recibidos por un cliente wifis

     public void showDisplayMessage (String s){
         Log.d("mensajes recibidos", "HA SIDO RECIBIDO: " + s);
     }
     public void forward(){
         Log.d("forward", "forward");
     }
     public void backward(){
         Log.d("backward", "backward");
     }
     public void left(){
         Log.d("left", "left");
     }
     public void right(){
         Log.d("right", "right");
     }
 }


