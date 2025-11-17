// This #include statement was automatically added by the Particle IDE.
#include <Adafruit_DHT_Particle.h>

// This #include statement was automatically added by the Particle IDE.
#include <coap.h>
#include "simple-coap.h"
// Include Particle Device OS APIs
#include "Particle.h"


#define DHTPIN D2 // Definir el pin donde está conectado el sensor (D2)
DHT dht(DHTPIN,DHT11); // Inicializar el sensor de temperatura y humedad en el pin D2

// Let Device OS manage the connection to the Particle Cloud
SYSTEM_MODE(AUTOMATIC);

// Show system, cloud connectivity, and application logs over USB
// View logs with CLI using 'particle serial monitor --follow'
SerialLogHandler logHandler(LOG_LEVEL_INFO);

IPAddress serverIP(54,235,30,244); // Reemplaza con la IP de tu servidor
int puerto=5683;
Coap coap;
bool sendTrue = true; // Variable para alternar entre "true" y "false"

void response_callback(CoapPacket &packet, IPAddress ip, int port);

void setup() {
    
    dht.begin(); // Iniciar el sensor DHT
    coap.start();
    coap.response(response_callback);

    Particle.publish("Cliente CoAP iniciado");
}

void loop() {
    // Enviar solicitud PUT al servidor
    
    float temp =dht.getTempCelcius();// Lee el sensor DHT11

    char payload[10]; // Define un array de char para hacer el put

    snprintf(payload, sizeof(payload), "%.2f", temp); // Convierte el valor en char[]
    
    
    Particle.publish("Enviando solicitud PUT con payload: ", payload);

    

    coap.put(serverIP, puerto, "temperature", payload);

    // Procesar eventos de CoAP
    coap.loop();

    // Esperar 2 segundos antes de enviar GET
    delay(2000);

    // Enviar solicitud GET al servidor
    Particle.publish("Enviando solicitud GET al servidor");
    coap.get(serverIP, puerto, "temperature");

    // Procesar eventos de CoAP
    coap.loop();

   
    // Esperar 10 segundos antes del próximo ciclo
    delay(10000);
}

void response_callback(CoapPacket &packet, IPAddress ip, int port) {
    Particle.publish("[Respuesta recibida]");

    char payload2[packet.payloadlen + 1];
    memcpy(payload2, packet.payload, packet.payloadlen);
    payload2[packet.payloadlen] = '\0';

    Particle.publish("Respuesta del servidor: ", payload2);
}







