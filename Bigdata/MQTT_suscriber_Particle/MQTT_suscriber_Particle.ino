// This #include statement was automatically added by the Particle IDE.
#include <Grove_4Digit_Display.h>

// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>



// Incluir las APIs de Particle
#include "Particle.h"

// Let Device OS manage the connection to the Particle Cloud
SYSTEM_MODE(AUTOMATIC);

// Show system, cloud connectivity, and application logs over USB
SerialLogHandler logHandler(LOG_LEVEL_INFO);

// Definir los pines para el display de 4 dígitos (CLK y DIO)
#define CLK D2
#define DIO D3
TM1637 tm1637(CLK, DIO);


const int buttonPin = D4; // Conectar el botón al puerto D2 del shield Grove
int buttonState = 0;

// Variable para almacenar la temperatura como String
String temperatura;

// Configuración del puerto MQTT
int puerto = 1883;
MQTT client("54.235.8.1", puerto, callback);

// Callback para manejar los mensajes entrantes de MQTT
void callback(char* topic, byte* payload, unsigned int length) {
    // Convertir el payload (byte*) a String
    temperatura = String((char*)payload);
    
}

void setup() {
    tm1637.init(); // Inicializar la pantalla de 4 dígitos
    tm1637.set(BRIGHT_TYPICAL); // Establecer el brillo típico de la pantalla
    tm1637.point(POINT_ON); // Encender el punto decimal, si es necesario
    pinMode(buttonPin, INPUT);

    // Conectar al servidor MQTT
    if (client.connect(System.deviceID())) {
        Particle.publish("Conectado al servidor MQTT");
        // Suscribirse al tema MQTT
        client.subscribe("nodo/temperatura");
    } else {
        Particle.publish("No se pudo conectar al servidor MQTT");
    }
}

void loop() {
    if (client.isConnected()) {
        // Asegurarse de que el cliente MQTT maneje su conexión
        client.loop();
        buttonState = digitalRead(buttonPin);
        
        // si se opulsa el oton se envia un mensaje 
        //a un topico al que esta suscrito el particle con el DHT
        if(buttonState==HIGH){
            
            client.publish("nodo/mensaje", "boton pulsado");
            
        }
        // Si se ha recibido una temperatura, procesarla y mostrarla
        if (temperatura.length() > 0) {
            // Convertir la temperatura de String a float
            float temp = temperatura.toFloat();

            // Convertir la temperatura a entero para la parte entera
            int tempInt = (int)temp;

            // Dividir la parte entera y decimal para mostrarlos en el display
            int8_t ListDisp[4];
            ListDisp[0] = tempInt / 10;  // Primer dígito de la parte entera
            ListDisp[1] = tempInt % 10;  // Segundo dígito de la parte entera
            ListDisp[2] = 0;  // Primer dígito de la parte decimal
            ListDisp[3] = 0;  // Segundo dígito de la parte decimal

            // Mostrar los números en la pantalla de 4 dígitos
            tm1637.display(0, ListDisp[0]); // Mostrar el primer dígito (parte entera, decenas)
            tm1637.display(1, ListDisp[1]); // Mostrar el segundo dígito (parte entera, unidades)
            tm1637.display(2, ListDisp[2]); // Mostrar el tercer dígito (parte decimal, décimas)
            tm1637.display(3, ListDisp[3]); // Mostrar el cuarto dígito (parte decimal, centésimas)

            // Publicar el valor de la temperatura
            Particle.publish("Temperatura: " + String(temp));
        }

    } else {
        // Si no está conectado, intentar reconectar
        Particle.publish("Intentando reconectar...");
        if (client.connect(System.deviceID())) {
            Particle.publish("Reconectado al servidor MQTT");
            client.subscribe("nodo/mensaje");
        }
    }
    delay(100); // Esperar 5 segundos antes de volver a intentarlo
}








