#include "wifiClient.h"
#include <esp_wifi.h>
#include "debug.h"
#include "can.h"

WiFiClient client;

void wifiSetupOrReconnect()
{
	if(WiFi.status() == WL_CONNECTED)
     return;
  
  //Make Sure Everything Is Reset
  client.stop();
  WiFi.disconnect();

  delay(50);
  // Set wifi mode as station
  DEBUG_PRINTLN("Setting Wifi mode to station (STA)");
  WiFi.mode(WIFI_STA);

  // Set communication protocol
  if(esp_wifi_set_protocol(WIFI_IF_STA, wifi_protocol) != ESP_OK)
  {
    DEBUG_PRINTLN("Setting WiFi protocol failed");
    ESP.restart();
  }

  delay(50);
  // Set tx max power
  if(esp_wifi_set_max_tx_power(wifi_tx_power) != ESP_OK)
  {
    DEBUG_PRINTLN("Setting max tx power failed");
    ESP.restart();
  }

  delay(50);
  // Connect to server
  if(WiFi.begin(ssid, password) ==  WL_CONNECT_FAILED)
  {
    DEBUG_PRINTLN("Connecting to server failed");
    ESP.restart();
  }

  delay(50);

  // Check if client is connected
  uint8_t fail_count = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    if(++fail_count > 8)
    {
      DEBUG_PRINTLN("Failed to get connection info");
      ESP.restart();
    }
    delay(100);
  }

  printWiFiInfo();
  connectToFormula();
}

void wifiHandler(void *parameter)
{
	int buff_len = 0;
	for(;;){
		buff_len = client.available();
    
    if(buff_len >= msg_size)
    {	
			CanMessage canMsg;
      client.readBytes(canMsg.msg, msg_size); 
      
			if(xQueueSend(messageQueue, (void *) &canMsg, 10*portTICK_PERIOD_MS) != pdPASS){
				DEBUG_PRINTLN("Failed to send Can message to queue");
			}
    }
		wifiSetupOrReconnect();
	}
}

void connectToFormula()
{
  client.stop(); //Make sure we are disconected
	delay(50);
  DEBUG_PRINTLN("Establishing connection to formula");
  client.connect(server_IP, port);
	delay(50);
  DEBUG_PRINTLN("Connection established");
	client.flush();
	delay(50);
}