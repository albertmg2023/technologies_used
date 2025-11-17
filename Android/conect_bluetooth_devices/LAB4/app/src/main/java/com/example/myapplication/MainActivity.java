package com.example.myapplication;

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

import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.UUID;


public class MainActivity extends AppCompatActivity {
    Button connectButton;
    Button disconectButton;
    Button forButton;
    Button backButton;
    Button leftButton;
    Button rightButton;
    TextView statusLabel;
    BluetoothAdapter bluetooth ;
    InputStream inputStream;
    OutputStream outputStream;
    //posib error
    BluetoothSocket btSocket;
    public  Boolean bluetoothActive = Boolean.FALSE ;
    private ArrayList<BluetoothDevice> deviceList = new ArrayList<BluetoothDevice>();
    public void forward() {
        try {
            String tmpStr = "w";
            byte bytes[] = tmpStr.getBytes();
            if (outputStream != null) outputStream.write(bytes);
            if (outputStream != null) outputStream.flush();
        } catch (Exception e) {
            Log.e("forward", "ERROR:" + e);
        }
    }
    public void backward() {
        try {
            String tmpStr = "s";
            byte bytes[] = tmpStr.getBytes();
            if (outputStream != null) outputStream.write(bytes);
            if (outputStream != null) outputStream.flush();
        } catch (Exception e) {
            Log.e("forward", "ERROR:" + e);
        }
    }
    public void right() {
        try {
            String tmpStr = "d";
            byte bytes[] = tmpStr.getBytes();
            if (outputStream != null) outputStream.write(bytes);
            if (outputStream != null) outputStream.flush();
        } catch (Exception e) {
            Log.e("forward", "ERROR:" + e);
        }
    }
    public void left() {
        try {
            String tmpStr = "a";
            byte bytes[] = tmpStr.getBytes();
            if (outputStream != null) outputStream.write(bytes);
            if (outputStream != null) outputStream.flush();
        } catch (Exception e) {
            Log.e("forward", "ERROR:" + e);
        }
    }
    /* protected void connect(BluetoothDevice device) {
        try {
            btSocket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));
            btSocket.connect();
            Log.d("MyFirstApp", "Client connected");
            inputStream = btSocket.getInputStream();
            outputStream = btSocket.getOutputStream();
        }catch (Exception e) {
            Log.e("ERROR: connect", ">>", e);
        }
    }
    /*
     */
    BroadcastReceiver discoveryResult = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            Log.d("MyFirstApp", "EntraOnrecieve ");
            //Guardamos el nombre del dispositivo descubierto
            String remoteDeviceName = intent.getStringExtra(BluetoothDevice.EXTRA_NAME);
            //Guardamos el objeto Java del dispositivo descubierto, para poder
            //conectar.
            BluetoothDevice remoteDevice = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
            //Leemos la intensidad de la radio con respecto a este dispositivo
            //bluetooth
            int rssi = intent.getShortExtra(BluetoothDevice.EXTRA_RSSI,Short.MIN_VALUE);
            //Guardamos el dispositivo encontrado en la lista
            /*if(remoteDeviceName != null) {
                if (remoteDeviceName.equals("ROBOTIS_210_70")) {
                    Log.d("onReceive", "Discovered ROBOTIS_210_70:connecting");

                    connect(remoteDevice);
                }
            }
            */

            

            deviceList.add(remoteDevice);
            //Mostramos el evento en el Log.
            Log.d("MyFirstApp", "Discovered "+ remoteDeviceName);
            Log.d("MyFirstApp", "RSSI "+ rssi + "dBm");



        }
    };
    private void startDiscovery(){

        if (bluetoothActive){

            //Borramos la lista de dispositivos anterior
            deviceList.clear();
            checkBTPermissions();
            //Activamos un Intent Android que avise cuando se encuentre un dispositivo
            //NOTA: <<discoveryResult>> es una clase <<callback>> que describiremos en
            //el siguiente paso
            registerReceiver(discoveryResult, new IntentFilter(BluetoothDevice.ACTION_FOUND));

            //Ponemos el adaptador bluetooth en modo <<Discovery>>

            Log.d("MyFirstApp", "BLUETOOTH STARTDISCOVERY");

            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                return;
            }
            bluetooth.startDiscovery();


        }
    }


    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 1) //Bluetooth permission request code
            if (resultCode == RESULT_OK){
                bluetoothActive=true;
                Toast.makeText(getApplicationContext(),"User Enabled Bluetooth ",
                        Toast.LENGTH_SHORT).show();
                Toast.makeText(getApplicationContext(),"bluetoothEnabled="+bluetoothActive,
                        Toast.LENGTH_SHORT).show();
            }else{
                Toast.makeText(getApplicationContext(),"User Did no" +
                                "t enable Bluetooth",
                        Toast.LENGTH_SHORT).show();
                bluetoothActive=false;
            }
    }
    public void checkBTPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            // Para Android 10 (API 29) y superior, necesitamos ACCESS_FINE_LOCATION
            if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{
                        android.Manifest.permission.ACCESS_FINE_LOCATION,
                        android.Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);
            }

            // Para Android 12 (API 31) y superior, también necesitamos BLUETOOTH_CONNECT y BLUETOOTH_SCAN
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_CONNECT)
                        != PackageManager.PERMISSION_GRANTED ||
                        ContextCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_SCAN)
                                != PackageManager.PERMISSION_GRANTED) {

                    ActivityCompat.requestPermissions(this, new String[]{
                            android.Manifest.permission.BLUETOOTH_CONNECT,
                            android.Manifest.permission.BLUETOOTH_SCAN}, 1002);
                }
            }
        }
    }

    public void onClickconnectButton(View view){
        Log.d("MyFirstApp", "CONNECT ");
        bluetooth = (BluetoothAdapter) BluetoothAdapter.getDefaultAdapter();
        if (bluetooth.isEnabled()){
            bluetoothActive=true;
            
            String address = bluetooth.getAddress();
            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                return;
            }
            String name = bluetooth.getName();
            Log.d("MyFirstApp", "PERMISIONS ");
            startDiscovery();
            Log.d("MyFirstApp", "DISCOVERY ");
//Mostramos la datos en pantalla (The information is shown in the screen)
            Toast.makeText(getApplicationContext(),"Bluetooth ENABLED:"+name+":"+address,
                    Toast.LENGTH_SHORT).show();
        }else{
            bluetoothActive=Boolean.FALSE;
            if (ActivityCompat.checkSelfPermission(this, android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                return;
            }
            startActivityForResult(new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE),1);


        }
    }
    public void onClickdisconnectButton(View view){
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Disconnect pressed");
    }
    public void onClickforButton(View view){
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Go Forward ");
        forward();
    }
    public void onClickbackButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Go Backward pressed");
        backward();
    }
    public void onClickleftButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Turn left pressed");
        left();
    }
    public void onClickrightButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Turn right pressed");
        right();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        connectButton = (Button) findViewById(R.id.connectButton);
        disconectButton = (Button) findViewById(R.id.disconectButton);
        forButton = (Button) findViewById(R.id.forButton);
        backButton= (Button) findViewById(R.id.backButton);
        leftButton= (Button) findViewById(R.id.leftButton);
        rightButton= (Button) findViewById(R.id.rightButton);
        InputStream inputStream;
        OutputStream outputStream;
        //posib error
        BluetoothSocket btSocket;
        BluetoothAdapter bluetooth;
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }
}