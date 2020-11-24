#include <Arduino.h>
#include <esp_wifi.h>
#include <Wifi.h>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

// Wifi setting
IPAddress server_IP(192, 168, 4, 1);
IPAddress gateway(192, 168, 4, 1);
IPAddress subnet(255, 255, 0, 0);
unsigned int port = 23;

const uint8_t wifi_protocol = 8; //  802.11 available b=1, g=2, n=4 ,lr=8 can be combinedas follow 1,2,3,4,7,8
const int8_t wifi_tx_power = 82;  // Maximum WiFi transmitting power, unit is 0.25dBm, range is [40, 82] corresponding to 10dBm - 20.5dBm here.

WiFiClient client;

// Data Variables
const size_t buff_size = 12;
uint8_t buffer[buff_size];

void espWiFiInfo()
{
  int8_t power = 0;
  esp_wifi_get_max_tx_power(&power);
  Serial.print("Max tx power set to: ");
  Serial.print((float)(power/4));
  Serial.println("dBm");

  uint8_t protocol;
  esp_wifi_get_protocol(WIFI_IF_AP, &protocol);
  Serial.print("Protocol set to:");
  Serial.println(protocol);
}

void connectToFormula()
{
  
  client.stop(); //Make sure we are disconected
  Serial.println("Establishing connection to formula");
  client.connect(server_IP, port);
  Serial.println("Connection established");
}

void wifiSetupOrReconnect()
{
  if(WiFi.status() != WL_CONNECTED)
  { 
    
    //Make Sure Everything Is Reset
    client.stop();
    WiFi.disconnect();

    delay(50);

    // Set wifi mode as station
    Serial.println("Setting Wifi mode to station (STA)");
    WiFi.mode(WIFI_STA);

    // Set communication protocol
    if(esp_wifi_set_protocol(WIFI_IF_STA, wifi_protocol) != ESP_OK)
    {
      Serial.println("Setting WiFi protocol failed");
      ESP.restart();
    }

    // Set tx max power
    if(esp_wifi_set_max_tx_power(wifi_tx_power) != ESP_OK)
    {
      Serial.println("Setting max tx power failed");
      ESP.restart();
    }

    // Connect to server
    if(WiFi.begin(ssid, password) ==  WL_CONNECT_FAILED)
    {
      Serial.println("Connecting to server failed");
       ESP.restart();
    }

    delay(50);

    // Check if client is connected
    uint8_t fail_count = 0;
    while (WiFi.status() != WL_CONNECTED)
    {
      if(++fail_count > 8)
      {
        Serial.println("Failed to get connection info");
        ESP.restart();
      }
      delay(100);
    }

    espWiFiInfo();
    connectToFormula();
  }
}

void setup() {
  Serial.begin(921600); //921600 buad-> max speed of CP2102

  wifiSetupOrReconnect();

  /*// TEST data
  for(int i = 0; i < buff_size; i++)
  {
    buffer[i] = 255;
  }*/
}

void loop() {
  // Test data
  //Serial.write(buffer, buff_size);
  
  while(1)
  {
    int buff_len = client.available();
    
    if(buff_len > 0)
    {
      client.readBytes(buffer, buff_size);
      Serial.write(buffer, buff_size);
      /*Serial.print("Data received:");
      Serial.println(buff_len);
      for(int i = 0; i < buff_size; i++)
        Serial.println(buffer[i]);*/
      
    }
  }
  
  client.flush();
  wifiSetupOrReconnect();
}