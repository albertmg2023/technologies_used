
// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_DHT_Particle.h>

// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

// Include Particle Device OS APIs
#include "Particle.h"

// Let Device OS manage the connection to the Particle Cloud

void callback(char* topic, byte* payload, unsigned int length) {
    // Implementar si se desea recibir mensajes
}
int puerto=1883;

MQTT client("54.235.8.1", puerto, callback);

#define DHTPIN D2 // Definir el pin donde está conectado el sensor (D2)
DHT dht(DHTPIN,DHT11);


void setup() {
    dht.begin();
    // Conectar al servidor
    if (client.connect(System.deviceID())) {
        Particle.publish("Conectado al servidor MQTT");
        // Publicar un mensaje
        
        
    } else {
        Particle.publish("No se pudo conectar al servidor MQTT");
    }
}

void loop() {
    if (client.isConnected()) {
        
        float temp =dht.getTempCelcius();// Lee el sensor DHT11

        char payloadT[10]; // Define un array de char para hacer el put

        snprintf(payloadT, sizeof(payloadT), "%.2f", temp);
        
        
        float hum =dht.getHumidity();// Lee el sensor DHT11

        char payloadH[10]; // Define un array de char para hacer el put

        snprintf(payloadH, sizeof(payloadH), "%.2f", hum);
        
         if (!isnan(temp) && !isnan(hum)) {
        
        //vamos cambiando el QOS y el retain 
        client.publish("nodo/temperatura", payloadT, MQTT::QOS0,false);
        
         }
        
            
        
        
        
        
        //client.publish("nodo/humedad", mensajeH);
        client.loop();
    } else {
        Particle.publish("Intentando reconectar...");
        if (client.connect(System.deviceID())) {
            Particle.publish("Reconectado al servidor MQTT");
        }
    }
    delay(100);
}
