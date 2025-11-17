// This #include statement was automatically added by the Particle IDE.
#include <coap.h>

// Include Particle Device OS APIs
#include "Particle.h"

// Let Device OS manage the connection to the Particle Cloud
SYSTEM_MODE(AUTOMATIC);

// Show system, cloud connectivity, and application logs over USB
// View logs with CLI using 'particle serial monitor --follow'
SerialLogHandler logHandler(LOG_LEVEL_INFO);

#include "simple-coap.h"

IPAddress serverIP(54,235,30,244); // Reemplaza con la IP de tu servidor
int puerto=5683;
Coap coap;
bool sendTrue = true; // Variable para alternar entre "true" y "false"

void response_callback(CoapPacket &packet, IPAddress ip, int port);

void setup() {
    delay(1000);

    coap.start();
    coap.response(response_callback);

    Particle.publish("Cliente CoAP iniciado");
}

void loop() {
    // Enviar solicitud PUT al servidor
    String payload = sendTrue ? "true" : "false";
    Particle.publish("Enviando solicitud PUT con payload: ", payload);

    // Convertir el payload a char array
    char payloadChar[payload.length() + 1];
    payload.toCharArray(payloadChar, payload.length() + 1);

    coap.put(serverIP, puerto, "basic", payloadChar);

    // Procesar eventos de CoAP
    coap.loop();

    // Esperar 2 segundos antes de enviar GET
    delay(2000);

    // Enviar solicitud GET al servidor
    Particle.publish("Enviando solicitud GET al servidor");
    coap.get(serverIP, puerto, "basic");

    // Procesar eventos de CoAP
    coap.loop();

    // Alternar entre "true" y "false" para el próximo ciclo
    sendTrue = !sendTrue;

    // Esperar 10 segundos antes del próximo ciclo
    delay(10000);
}

void response_callback(CoapPacket &packet, IPAddress ip, int port) {
    Particle.publish("[Respuesta recibida]");

    char payload[packet.payloadlen + 1];
    memcpy(payload, packet.payload, packet.payloadlen);
    payload[packet.payloadlen] = '\0';

    Particle.publish("Respuesta del servidor: ", payload);
}






























