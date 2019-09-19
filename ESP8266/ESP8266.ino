#include <ESP8266WiFi.h>
#include <Wire.h>

const char* ssid     = "Tran gia phuc";
const char* password = "phm123456";

const int16_t I2C_MASTER = 0x02;
const int16_t I2C_SLAVE = 0x40;

WiFiClient client;
const int port = 9876;
const char* host = "192.168.1.15";

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
        client.read();
        float temp = readi2c(0xF3);
        float humid = readi2c(0xF5);
        client.print(temp);
        client.print(humid);
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
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
    delay(500);
    }

    delay(5000);
    
    client.connect(host, port);

}

float readi2c(int mode)
{
  unsigned int data[2];
  Wire.beginTransmission(I2C_SLAVE);
  //Send humidity measurement command
  Wire.write(mode);
  Wire.endTransmission();
  delay(500);
 
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