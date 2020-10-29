#include <Arduino.h>
#include <Wifi.h>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

// Wifi setting
IPAddress server_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
unsigned int port = 80;

WiFiClient client;

// Data Variables
const size_t buff_size = 12;
uint8_t buffer[buff_size];

void wifiSetupOrReconnect()
{
  if(WiFi.status() != WL_CONNECTED)
  { 
    //Make Sure Everything Is Reset
    client.stop();
    WiFi.disconnect();

    delay(50);

    // Set wifi as station and connect to server
    WiFi.mode(WIFI_STA);
    if(WiFi.begin(ssid, password) ==  WL_CONNECT_FAILED)
      ESP.restart();

    delay(50);

    // Check if client is connected
    uint8_t fail_count = 0;
    while (WiFi.status() != WL_CONNECTED)
    {
      if(++fail_count > 8)
        ESP.restart();
      delay(500);
    }

    connectToFormula();
  }
}

void connectToFormula()
{
  client.stop(); //Make sure we are disconected

  client.connect(server_IP, port);
  client.setNoDelay(true); //allow fast communication
}

void setup() {
  Serial.begin(921600); //921600 buad-> max speed of CP2102

  wifiSetupOrReconnect();

  // TEST data
  for(int i = 0; i < buff_size; i++)
  {
    buffer[i] = 255;
  }
}

void loop() {
  // Test data
  Serial.write(buffer, buff_size);
  
  while(1)
  {
    int buff_len = client.available();
    if(buff_len > 0)
    {
      client.readBytes(buffer, buff_size);
      Serial.write(buffer, buff_size);
    }
  }
  
  client.flush();
  wifiSetupOrReconnect();
}