#include <Arduino.h>
#include <WiFi.h>
#include <esp_wifi.h>

#include <can.hpp>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

// Wifi setting
const IPAddress local_IP(192, 168, 4, 1);
const IPAddress gateway(192, 168, 4, 100);
const IPAddress subnet(255, 255, 255, 0);
const unsigned int port = 23;

const uint8_t wifi_protocol = 7; //  802.11 available b=1, g=2, n=4 ,lr=8 can be combined as follow 1,3,7,8,15
const int8_t wifi_tx_power = 82;  // Maximum WiFi transmitting power, unit is 0.25dBm, range is [40, 82] corresponding to 10dBm - 20.5dBm here.

WiFiServer server(port); 

// Data Variables
const size_t can_queue_size = 10;
const size_t msg_size = 12; 
uint8_t data[msg_size];
uint32_t id;

void printWiFiInfo()
{
  IPAddress IP = WiFi.softAPIP();
  
  Serial.println("Network " + String(ssid) +" is running");
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

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

void serverSetup() 
{
  // Stop any previous WiFi
  WiFi.disconnect(); 

  // Setting WiFi mode
  Serial.println("Setting WiFi mode to Access Point (AP)");
  WiFi.mode(WIFI_AP);

  // Set communication protocol
  // Způsobuje problémy
  /*if(esp_wifi_set_protocol(WIFI_IF_AP, wifi_protocol) != ESP_OK)
  {
    Serial.println("Setting WiFi protocol failed");
    ESP.restart();
  }*/

  // Set tx max power
  if(esp_wifi_set_max_tx_power(wifi_tx_power) != ESP_OK)
  {
    Serial.println("Setting max tx power failed");
    ESP.restart();
  }

  espWiFiInfo();

  // Configurating the AP
  if(!WiFi.softAPConfig(local_IP, gateway, subnet))
  {
    Serial.println("AP failed to configurate");
    ESP.restart();
  }

  delay(50);

  if(!WiFi.softAP(ssid, password)) // softAP(ssid, password, channel, hidden, num_of_clients)
  {
    Serial.println("Starting AP failed");
    ESP.restart();
  }
  
  delay(50);

  // Printing Server info
  printWiFiInfo();

  // Starting server
  server.begin();
  Serial.println("Server started");
}

void setup() {
  Serial.begin(115200);

  //generateTestData(1538, data);

  serverSetup();
  canSetup(can_queue_size);
}

void loop() {
  
  WiFiClient client = server.available();

  if (client) {
    while (client.connected()) {  
      Serial.println("Connected");
      canDataPack dataPack = canReceive();

      if(dataPack.canID != 0){
        
        convertDataPackToByteArray(data, dataPack);        
        Serial.println("Converted");
        client.write(data, msg_size);
        Serial.println("Send"); 
      }

      //client.write(data, msg_size);
      delay(10); 
    }

    client.stop();
    
  }
}

