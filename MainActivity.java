package com.example.flow;
//Reference sites
//https://www.androidauthority.com/use-remote-web-api-within-android-app-617869/
//https://github.com/obaro/SimpleWebAPI/blob/master/app/src/main/java/com/sample/foo/simplewebapi/MainActivity.java
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    //Attempt to launch an activity outside our app
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button surflineBtn = (Button) findViewById(R.id.surflineBtn);
        surflineBtn.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                String SurfLine = "https://www.surfline.com/surf-report/pacific-beach/5842041f4e65fad6a7708841";
                Uri webAddress = Uri.parse(SurfLine);

                Intent goToSurfLine = new Intent(Intent.ACTION_VIEW, webAddress);
                if (goToSurfLine.resolveActivity(getPackageManager()) != null) {
                    startActivity(goToSurfLine);
                }
            }
        });

        class retrieveFeedTask extends AsyncTask <Void, Void, String> {

            private Exception exception;

            protected void onPreExecute() {
                //progressBar.setVisibility(View.VISIBLE);
                TextView resultTextView = (TextView) findViewById(R.id.resultTextView);
                resultTextView.setText("");
            }

            protected String doInBackground(Void... urls) {
                //EditText buoyID = (EditText) findViewById(R.id.buoyIdEditText)
                //String buoyId = buoyID
                // Do some validation here

                try {
                    URL url = new URL("https://tidesandcurrents.noaa.gov/api/datagetter?date=latest&station=9410230&product=water_level&datum=mllw&units=english&time_zone=lst&application =ports_screen&format=json");
                    HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                    try {
                        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                        StringBuilder stringBuilder = new StringBuilder();
                        String line;
                        while ((line = bufferedReader.readLine()) != null) {
                            stringBuilder.append(line).append("\n");
                        }
                        bufferedReader.close();
                        return stringBuilder.toString();
                    } finally {
                        urlConnection.disconnect();
                    }
                } catch (Exception e) {
                    Log.e("ERROR", e.getMessage(), e);
                    return null;
                }
            }

        }
    }
}
