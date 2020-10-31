#include <Arduino.h>
#include <WiFi.h>

#include <can.hpp>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

// Wifi setting
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
unsigned int port = 80;

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

void serverSetup() 
{
  // Stop any previous WiFi
  WiFi.disconnect(); 

  // Setting WiFi mode
  Serial.println("Setting WiFi mode to Access Point (AP)");
  WiFi.mode(WIFI_AP);

  // Starting the AP
  if(!WiFi.softAPConfig(local_IP, gateway, subnet)){
    Serial.println("AP failed to configurate");
    ESP.restart();
  }

  delay(50);

  if(!WiFi.softAP(ssid, password, 1, 0, 1)){ // softAP(ssid, password, channel, hidden, num_of_clients)
    Serial.println("Starting AP faild");
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

  //generateTestData(603, data);

  serverSetup();
  canSetup(can_queue_size);
}

void loop() {
  
  WiFiClient client = server.available();
  client.setNoDelay(true); // allow fast communication

  if (client) {
    
    Serial.println("New connection");
    while (client.connected()) {  
      
      canDataPack dataPack = canReceive();

      if(dataPack.canID != 0){
        convertDataPackToByteArray(data, dataPack);

        client.write(data, 12); 
      }
      delay(1); 
    }

    client.stop();
    
  }
}

