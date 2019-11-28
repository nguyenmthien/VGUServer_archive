#include <ESP8266WiFi.h>
#include "i2c.c"

#ifndef STASSID
#define STASSID "nguyenmthien"
#define STAPSK  "299792458"
#define SLEEPTIME 10e6 //in microseconds
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

IPAddress ip( 192, 168, 0, 128 );
IPAddress gateway( 192, 168, 0, 1 );
IPAddress subnet( 255, 255, 255, 0 );

const char* host = "192.168.0.102";
const uint16_t port = 2033;



void setup() {
    Serial.begin(115200);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.mode(WIFI_STA);    
    WiFi.config( ip, gateway, subnet );
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed"); delay(1000); return;
  }

  // Get data from sensor
  Serial.println("getting data from sensor");
  setupi2c();
  float temp = readi2c(0xF3);
  float humid = readi2c(0xF5);
  String message = "";
  message = String(temp, 1) + " " + String(humid);


  // This will send a string to the server
  Serial.println("sending data to server");
  if (client.connected()) { 
    client.println(message);
  }


  // Close the connection
  Serial.println();
  Serial.println("closing connection");
  client.stop();

  ESP.deepSleep(SLEEPTIME); // execute once every 5 minutes, don't flood remote service
}
