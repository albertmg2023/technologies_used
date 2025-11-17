package com.example.wififunciona;


import android.content.Context;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.StringTokenizer;

public class NetworkExecutor extends Thread {
    public Context mContext;
    public Handler handlerNetworkExecutor;
    // Constructor que recibe el contexto
    public NetworkExecutor(Context context, Handler handlerexeutor) {
        this.mContext = context;
        this.handlerNetworkExecutor = handlerexeutor;
    }



    File cameraFile;
    final public int HTTP_SERVER_PORT  = 5057;
    final public int CODE_OK = 200;
    final public int CODE_BADREQUEST = 400;
    final public int CODE_FORBIDDEN = 403;
    final public int CODE_NOTFOUND = 404;
    final public int CODE_INTERNALSERVERERROR = 500;
    final public int CODE_NOTIMPLEMENTED = 501;

    //InputStream is;
    //lee linea a linea el index.html y lo pasa a string
    public String readResourceTextFile() {
        StringBuilder fileStr = new StringBuilder();

        try(InputStream is = mContext.getResources().openRawResource(R.raw.index);
            BufferedReader br = new BufferedReader(new InputStreamReader(is))) {

            String readLine;
            while ((readLine = br.readLine()) != null) {
                fileStr.append(readLine).append("\r\n");
            }
            return fileStr.toString();
        } catch (IOException e) {
            Log.e("readResourceTextFile", "ERROR:" + e) ;

        }
        return "";

    }
    public void run()  {
        Socket scliente=null;

        ServerSocket unSocket=null;
        try {
        unSocket = new ServerSocket(HTTP_SERVER_PORT); //Creamos el puerto
        while(true) {


                scliente = unSocket.accept(); //Aceptando conexiones del navegador Web
                System.setProperty("line.separator", "\r\n");
//Creamos los objetos para leer y escribir en el socket
                BufferedReader in = new BufferedReader(new
                        InputStreamReader(scliente.getInputStream()));
                PrintStream out = new PrintStream(new
                        BufferedOutputStream(scliente.getOutputStream()));
//Leemos el comando que ha sido enviado por el servidor web
//Ejemplo de comando: GET /index.html HTTP\1.0
                String cadena = in.readLine();
                StringTokenizer st = new StringTokenizer(cadena);
                String commandString = st.nextToken().toUpperCase();
                String fileStr = readResourceTextFile();
                if (commandString.equals("GET")) {
                    String urlObjectString = st.nextToken();
                    Log.v("urlObjectString", urlObjectString);
                    if (urlObjectString.toUpperCase().startsWith("/INDEX.HTML") ||
                            urlObjectString.equalsIgnoreCase("/INDEX.HTML") ||
                            urlObjectString.equals("/")) {
                        String headerStr = getHTTP_Header(CODE_OK, "text/html", fileStr.length());
                        out.print(headerStr);
                        out.println(fileStr);
                        out.flush();}
                    if (urlObjectString.toUpperCase().startsWith("/FORWARD")) {
                        sendmessage("FORWARD");
                        String headerStr = getHTTP_Header(CODE_OK, "text/html", fileStr.length());
                        out.print(headerStr);
                        out.println(fileStr);
                        out.flush();
                    }
                    if (urlObjectString.toUpperCase().startsWith("/BACKWARD")) {
                        sendmessage("BACKWARD");
                        String headerStr = getHTTP_Header(CODE_OK, "text/html", fileStr.length());
                        out.print(headerStr);
                        out.println(fileStr);
                        out.flush();
                    }
                    if (urlObjectString.toUpperCase().startsWith("/LEFT")) {
                        sendmessage("LEFT");
                        String headerStr = getHTTP_Header(CODE_OK, "text/html", fileStr.length());
                        out.print(headerStr);
                        out.println(fileStr);
                        out.flush();
                    }
                    if (urlObjectString.toUpperCase().startsWith("/RIGHT")) {
                        sendmessage("RIGHT");
                        String headerStr = getHTTP_Header(CODE_OK, "text/html", fileStr.length());
                        out.print(headerStr);
                        out.println(fileStr);
                        out.flush();
                    }


                    if ( urlObjectString.toUpperCase().startsWith("/CAMERA.JPG")||
                            urlObjectString.toUpperCase().startsWith("/CAMERA.") ) {
                        sendmessage("CAMERA");

                        cameraFile = ((MainActivity)  mContext).getOutputMediaFile();
                        FileInputStream fis = null;
                        boolean exist = true;
                        try {
                            fis = new FileInputStream(cameraFile);
                        } catch (FileNotFoundException e) {
                            exist = false;
                        }
                        if (exist) {
                            String headerStr = getHTTP_Header(CODE_OK,
                                    "image/jpeg",(int)cameraFile.length());
                            out.print(headerStr);
                            byte[] buffer = new byte[4096];
                            int n;
                            while ( (n = fis.read(buffer)) > 0 ) { // enviar archivo
                                out.write(buffer, 0, n);
                            }
                            out.flush();
                            out.close();
                        }
                        //mensaje si no existe la imagen
                        if(!exist){
                            String headerStr = getHTTP_Header(CODE_NOTFOUND, "text/html", 0);
                            out.print(headerStr);
                            out.println("<html><body><h1>Image File Not Found</h1></body></html>");
                            out.flush();
                            out.close();


                        }
                    }
                }}
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }

    private void sendmessage(String message){
        if(handlerNetworkExecutor!=null){
            Message msg =new Message();
            msg.obj = message;
            handlerNetworkExecutor.sendMessage(msg);
        }
    }
    private String getHTTP_HeaderContentLength(int headerFileLength){
        return "Content-Length: " + headerFileLength + "\r\n";
    }
    private String getHTTP_HeaderContentType(String headerContentType){
        return "Content-Type: "+headerContentType+"\r\n";
    }
    //codifica a "lenguaje" http los diferentes
    // //campos que le proporcionamos desde codigo
    private String getHTTP_Header(int headerStatusCode, String headerContentType, int
            headerFileLength) {
        String result = getHTTP_HeaderStatus(headerStatusCode) +
                "\r\n" +
                getHTTP_HeaderContentLength(headerFileLength)+
                getHTTP_HeaderContentType(headerContentType)+
                "\r\n";
        return result;
    }
    private String getHTTP_HeaderStatus(int headerStatusCode){
        String result = "";
        switch (headerStatusCode) {
            case CODE_OK:
                result = "200 OK"; break;
            case CODE_BADREQUEST:
                result = "400 Bad Request"; break;
            case CODE_FORBIDDEN:
                result = "403 Forbidden"; break;
            case CODE_NOTFOUND:
                result = "404 Not Found"; break;
            case CODE_INTERNALSERVERERROR:
                result = "500 Internal Server Error"; break;
            case CODE_NOTIMPLEMENTED:
                result = "501 Not Implemented"; break;
        }
        return ("HTTP/1.0 "+result);
    }
    //muestra mensajes en el log
    public void showDisplayMessage(String s){
        Log.d("mensajes recibidos", "HA SIDO RECIBIDO: " + s);
    }


}


