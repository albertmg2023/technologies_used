package com.example.myapplication;

import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import android.widget.*;
import android.view.View;


public class MainActivity extends AppCompatActivity {
    Button connectButton;
    Button disconectButton;
    Button forButton;
    Button backButton;
    Button leftButton;
    Button rightButton;
    TextView statusLabel;
    public void onClickconnectButton(View view){
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Connect pressed");
    }
    public void onClickdisconnectButton(View view){
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Disconnect pressed");
    }
    public void onClickforButton(View view){
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Go Forward pressed");
    }
    public void onClickbackButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Go Backward pressed");
    }
    public void onClickleftButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Turn left pressed");
    }
    public void onClickrightButton(View view) {
        statusLabel = (TextView) findViewById(R.id.textView);
        statusLabel.setText("Turn right pressed");
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        connectButton = (Button) findViewById(R.id.connectButton);
        disconectButton = (Button) findViewById(R.id.disconectButton);
        forButton = (Button) findViewById(R.id.forButton);
        backButton= (Button) findViewById(R.id.backButton);
        leftButton= (Button) findViewById(R.id.leftButton);
        rightButton= (Button) findViewById(R.id.rightButton);

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