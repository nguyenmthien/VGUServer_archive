#include <ESP8266WiFi.h>
#include <Wire.h>

const long long int sleep_time = 10e6;

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
    initWiFi();
}

void loop()
{
    setupWiFi();
    float temp = readi2c(0xF3);
    float humid = readi2c(0xF5);
    String message = "";
    message = String(temp, 1) + " " + String(humid, 2);
    client.print(message);
    ESP.deepSleep(sleep_time);
}

void setupi2c()
{
    Wire.pins(0, 2); 
    Wire.begin();
    Wire.beginTransmission(I2C_SLAVE);
    Wire.endTransmission();
    delay(3);
}

void initWiFi()
{
    WiFi.persistent(false);
    WiFi.mode(WIFI_STA);
    WiFi.config( ip, gateway, subnet );
}

void setupWiFi()
{
    WiFi.forceSleepWake();
    delay(1);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) 
    {
    delay(1);
    }

    delay(10);
    
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
  
  // Convert the data for humidity mode
  if (mode == 0xF5)
  {
      float humidity  = ((data[0] * 256.0) + data[1]);
      humidity = ((125 * humidity) / 65536.0) - 6;
      return humidity;  
  }
  
  // Convert the data for temperature mode
  if (mode == 0xF3)
  {
      float temp  = ((data[0] * 256.0) + data[1]);
      float celsTemp = ((175.72 * temp) / 65536.0) - 46.85;
      return celsTemp;
  }
} 