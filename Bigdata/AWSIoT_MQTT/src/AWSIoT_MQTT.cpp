/* 
 * Project myProject
 * Author: Your Name
 * Date: 
 * For comprehensive documentation and examples, please visit:
 * https://docs.particle.io/firmware/best-practices/firmware-template/
 */

// Include Particle Device OS APIs
#include "Particle.h"
#include "MQTT-TLS.h"

// Configurations
SYSTEM_MODE(AUTOMATIC);
SYSTEM_THREAD(ENABLED);
SerialLogHandler logHandler(LOG_LEVEL_INFO);

void callback(char* topic, byte* payload, unsigned int length);
//amazonrootca1
#ifndef AMAZON_IOT_ROOT_CA_PEM
#define AMAZON_IOT_ROOT_CA_PEM                                          \
"-----BEGIN CERTIFICATE-----\r\n"                                       \
"MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF\r\n" 	\
"ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6\r\n" 	\
"b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL\r\n" 	\
"MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv\r\n" 	\
"b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj\r\n" 	\
"ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM\r\n" 	\
"9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw\r\n" 	\
"IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6\r\n" 	\
"VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L\r\n" 	\
"93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm\r\n" 	\
"jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC\r\n" 	\
"AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA\r\n" 	\
"A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI\r\n" 	\
"U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs\r\n" 	\
"N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv\r\n" 	\
"o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU\r\n" 	\
"5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy\r\n" 	\
"rqXRfboQnoZsG4q5WTP468SQvvG5\r\n" 	\
"-----END CERTIFICATE-----"
#endif

//certificado del dispositivo
#ifndef CLIENT_CERTIFICATE_PEM
#define CLIENT_CERTIFICATE_PEM                                              \
"-----BEGIN CERTIFICATE-----\r\n"                                       \
"MIIDWjCCAkKgAwIBAgIVAJGRGUtApf7tgykz4D4coeDeNEm5MA0GCSqGSIb3DQEB\r\n" 	\
"CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t\r\n" 	\
"IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yNDEyMDgxMzUy\r\n" 	\
"NTVaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh\r\n" 	\
"dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC02/4c4i99zSJVuqaM\r\n" 	\
"htE3bHLb+AwFLkKEufAQ2OX81R0U36dvyIG+5Z8MiK8jsHiaodmHDis/3QIFkz2W\r\n" 	\
"fzIfLkOhnWTBlvSP0TK7iB3swMbhZchxYhAd7JgmV2YTQbDm1d4zy7iJfCrxCg9s\r\n" 	\
"e5L0FODdbEAXE6iw091JBNYwE7byW58WPXkDOPu+lwYYgu1FB48aioAC2ZAULKBT\r\n" 	\
"5hEUUnZ/8QJ6bbfvE4b9hIKaXPQPHbr4dBmP1M0/B15dkud4niLPbAgybw2ypD0u\r\n" 	\
"8DKmZ3ecjPtek6hFd8hzqrfGuZRqOjMHJ351gnAvmgPjcODhtnaJN1uBbzvIClCw\r\n" 	\
"mEERAgMBAAGjYDBeMB8GA1UdIwQYMBaAFH2221VucWhrelvO5bdq8VFsrZFtMB0G\r\n" 	\
"A1UdDgQWBBRSVOuvE0Uk/FTjoTSP6OyQ31EoazAMBgNVHRMBAf8EAjAAMA4GA1Ud\r\n" 	\
"DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAkKh8uAWtkHHJJXvoAgoq5C0d\r\n" 	\
"SB1JsFIvEDDApu7jAVttUVhpXXAXqIRRYEfeOMv7iOQAhRg0VhgwN29BcX2cnGS3\r\n" 	\
"KY2j17FQcY9T00jV//5GaO6fUnc1W/GNDxOiDoeqWmnwm8kmldd8v9mbppskticM\r\n" 	\
"TdSJbMRTsyr1MB70gGxsY9P28SdHVoYDlZj1BRet83lQoGSU7duMESFqIAeOM/Ch\r\n" 	\
"NE6icBSZ2G76doSdMly81SQyIPorrXtqmGXauk33MN1elNLM+rStSbidGCdHxGf4\r\n" 	\
"osiu5a0fIgOsZJ1QowlZ8voyivEvtroN//eDeS0QDU8dYrylaZ8iG0WiUecXaA==\r\n" 	\
"-----END CERTIFICATE-----"
#endif


//clave PRIBADA
#ifndef CLIENT_PRIVATE_KEY_PEM
#define CLIENT_PRIVATE_KEY_PEM                                                  \
"-----BEGIN RSA PRIVATE KEY-----\r\n"                                   \
"MIIEowIBAAKCAQEAtNv+HOIvfc0iVbqmjIbRN2xy2/gMBS5ChLnwENjl/NUdFN+n\r\n"  \
"b8iBvuWfDIivI7B4mqHZhw4rP90CBZM9ln8yHy5DoZ1kwZb0j9Eyu4gd7MDG4WXI\r\n"  \
"cWIQHeyYJldmE0Gw5tXeM8u4iXwq8QoPbHuS9BTg3WxAFxOosNPdSQTWMBO28luf\r\n"  \
"Fj15Azj7vpcGGILtRQePGoqAAtmQFCygU+YRFFJ2f/ECem237xOG/YSCmlz0Dx26\r\n"  \
"+HQZj9TNPwdeXZLneJ4iz2wIMm8NsqQ9LvAypmd3nIz7XpOoRXfIc6q3xrmUajoz\r\n"  \
"Byd+dYJwL5oD43Dg4bZ2iTdbgW87yApQsJhBEQIDAQABAoIBAHdxesd0kczRd0WK\r\n"  \
"+YeBWhbyZoDjtnyNapzhd6yIsoth68znUFtA3n9Ggt3yP0iguWXWUiUhtGp++WDZ\r\n"  \
"Nyl3Y5C4Ky5HFk3L9kQs8wZrBOhhAHfHkrNfAinhITLhMaayEbTBtfgbKQqTmICM\r\n"  \
"Flec3RaZ21Agt8sFzrjJkzEwIoyovBZNZz/9ZCJtJ+5jKNuftVRIth1ahQHIMHDC\r\n"  \
"WouvygNSKuZeQo9X3TMpp87s1Re26VRASyi0vFvxJwFuxfd/YxlTZvCZ2jOz37EX\r\n"  \
"9rMwPsvYxMvudeHmSMcU2RmqwCTQOGnQY70FCM+kkdjH8b1Y1kAvcuEREr6yFXpk\r\n"  \
"AmEgbOECgYEA31pzUHzzAV2dJnVjwiQKH3wwTa23JT05ZyDTR+4FEeEEGYTaTFGPM\r\n"  \
"URUKonktZulVNwcE/iQ7aW3wq2tJwudotxNX5QZOnGWwU1oE49pUblkviAHnDHzA\r\n"  \
"S6M46zThbKWpUFI6jxkSNTw0fSNHAYsC/n0duKtnAYadqkWqCvXw1lUCgYEAz0t7\r\n"  \
"EK/zxNvElVO72iXwZ76DdzB34C6gzCSyUX1GhL9snBNeG7qs54OUl5M6zOF+yIXe\r\n"  \
"eDBcejvP7wpAd7YnYcd0ll023INOxCirCaEIWVPtp8WX4YNFs2f55dSSLnIImujU\r\n"  \
"fUZooAkpmcaIM/A+i6RV0QPkmsJH8bQA4CSzI80CgYEAr7cyN2VFrJJgewwpgmfm\r\n"  \
"CuUh/0qmZkanbWnWrqUkGe/D0OvC7f3QWYLLTg01WdxB7Tu5gtMwZn5WtBWA/zQd\r\n"  \
"HsK6CHUQzVv2/2w3oqZ2fCXwDfkpM5rFkfwEYI7GtjoSXR2D8mZP+8+0n6psR1t8\r\n"  \
"7Ie0JT+7lui4C2gpIdxhL80CgYAI95fsQeBGrMcVOpkOt8NtiXVAa61T2lCEZDX+\r\n"  \
"hm/NgEZffgr9IhcmsK912x2ZDUwhuoDELDtj4kB9c7EUPKH5fdpSQtgDs/5tR+EW\r\n"  \
"OowU6SeHsWl/jOEwAJhz0707Gx26LcY7YRdXjO3qxAbSUFs0STiZIRT7iNn537KF\r\n"  \
"/7BsJQKBgE0glDvDzrkIvAOM8RyV1t/IAwXYcVqji033Po14kjwds6j/MrmPFb4O\r\n"  \
"u13THIJPdA/BEnMQaGWz4MxqFmclUGpWB5P2vgJNrw0mtiZbOiouJCAp2MgDXRXO\r\n"  \
"2y+MwoSCfAW9GJXWBnOiWqyvyGK+f673PpB/CD3FtfO8cY/8O9WH\r\n"  \
"-----END RSA PRIVATE KEY-----"
#endif

#ifndef CONSTANTS_DEFINED
#define CONSTANTS_DEFINED
const char amazonIoTRootCaPem[] = AMAZON_IOT_ROOT_CA_PEM;
const char clientKeyCrtPem[] = CLIENT_CERTIFICATE_PEM;
const char clientKeyPem[] = CLIENT_PRIVATE_KEY_PEM;
#endif

// MQTT Configuration
const char* CLIENT_ID = "IR2131";
MQTT client("a1uvxdawvdudhp-ats.iot.us-east-1.amazonaws.com", 8883, callback);

// Constants
#define ONE_DAY_MILLIS (24 * 60 * 60 * 1000)

// Global Variables
unsigned long lastSync = millis();

// Function Prototypes
void callback(char* topic, byte* payload, unsigned int length);
String generateRandomObservation();

// Callback for MQTT Messages
void callback(char* topic, byte* payload, unsigned int length) {
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = '\0';
    String message(p);
    Serial.printlnf("Message arrived [%s]: %s", topic, message.c_str());
    delay(1000);
}

// Generate Random Sensor Data
String generateRandomObservation() {
    float temperature = random(20, 30) + random(0, 100) / 100.0;
    float humidity = random(40, 60) + random(0, 100) / 100.0;
    float pressure = random(950, 1050) + random(0, 100) / 100.0;
    return String::format(
        "{\"temperature\": %.2f, \"humidity\": %.2f, \"pressure\": %.2f}", 
        temperature, humidity, pressure
    );
}

// Setup Function
void setup() {
    Serial.begin(9600);
    delay(15000);

    if (millis() - lastSync > ONE_DAY_MILLIS) {
        Particle.syncTime();
        lastSync = millis();
    }

    if (!WiFi.ready()) {
        Serial.println("Error: WiFi not connected.");
        return;
    }

    int ret = client.enableTls(
        amazonIoTRootCaPem, sizeof(amazonIoTRootCaPem),
        clientKeyCrtPem, sizeof(clientKeyCrtPem),
        clientKeyPem, sizeof(clientKeyPem)
    );

    if (ret > 0) {
        Serial.printlnf("TLS enable failed with code: %d", ret);
        return;
    }

    if (client.connect(CLIENT_ID) < 0) {
        Serial.println("MQTT connection failed.");
        return;
    }

    if (client.isConnected()) {
        client.publish("/outTopic", "Hello World");
        client.subscribe("inTopic/message");
        Serial.println("Client connected.");
    }
}

// Main Loop
void loop() {
    if (client.isConnected()) {
        String json = generateRandomObservation();
        client.publish("/outTopic", json);
        client.loop();
    } else {
        Serial.println("Client not connected. Reconnecting...");
        client.connect(CLIENT_ID);
    }
    delay(200);
	
	client.loop();
}