#include <ESP8266WiFi.h>
#include <Wire.h>

const char* ssid     = "nguyenmthien";
const char* password = "299792458";

IPAddress ip( 192, 168, 137, 128 );
IPAddress gateway( 192, 168, 0, 1 );
IPAddress subnet( 255, 255, 255, 0 );

const int16_t I2C_MASTER = 0x02;
const int16_t I2C_SLAVE = 0x40;

WiFiClient client;
const int port = 2033;
const char* host = "192.168.1.4";

void setupi2c();
void setupWiFi();
float readi2c(int mode);
void sendWiFi(int msg);

void setup()
{
    setupi2c();
    setupWiFi();
}

void loop()
{
    if (client.available())
    {
        while (client.available())
        {
            client.read();
        }
        float temp = readi2c(0xF3);
        float humid = readi2c(0xF5);
        String message = "";
        message = String(temp, 1) + " " + String(humid, 2);
        client.print(message);
    }
}

void setupi2c()
{
    Wire.pins(0, 2); 
    Wire.begin();
    Wire.beginTransmission(I2C_SLAVE);
    Wire.endTransmission();
    delay(300);
}



void setupWiFi()
{
    WiFi.forceSleepWake();
    delay(1);
    WiFi.persistent(false);
    WiFi.mode(WIFI_STA);
    WiFi.config( ip, gateway, subnet );

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
    delay(10);
    }

    delay(1000);
    
    client.connect(host, port);

}

float readi2c(int mode)
{
  unsigned int data[2];
  Wire.beginTransmission(I2C_SLAVE);
  //Send humidity measurement command
  Wire.write(mode);
  Wire.endTransmission();
  delay(10);
 
  // Request 2 bytes of data
  Wire.requestFrom(I2C_SLAVE, 2);
  // Read 2 bytes of data to get humidity
  if(Wire.available() == 2)
  {
    data[0] = Wire.read();
    data[1] = Wire.read();
  }
  
  // Convert the data for humidity
  if (mode == 0xF5)
  {
      float humidity  = ((data[0] * 256.0) + data[1]);
      humidity = ((125 * humidity) / 65536.0) - 6;
      return humidity;  
  }
  
  if (mode==0xF3)
  {
      float temp  = ((data[0] * 256.0) + data[1]);
      float celsTemp = ((175.72 * temp) / 65536.0) - 46.85;
      return celsTemp;
  }
} 