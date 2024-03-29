#include "server.h"
#include <esp_wifi.h>
#include "can.h"
#include "debug.h"

WiFiServer server(port); 

void serverSetup() 
{
  // Stop any previous WiFi
  WiFi.disconnect(); 

  WiFi.mode(WIFI_AP);

  // Set communication protocol
  // Způsobuje problémy
  if(esp_wifi_set_protocol(WIFI_IF_AP, wifi_protocol) != ESP_OK)
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

  if(!WiFi.softAP(ssid, password)) // softAP(ssid, password, channel, hidden, num_of_clients)
  {
    DEBUG_PRINTLN("Starting AP failed");
    ESP.restart();
  }

  delay(50);

  // Configurating the AP
  if(!WiFi.softAPConfig(server_IP, gateway, subnet))
  {
    DEBUG_PRINTLN("AP failed to configurate");
    ESP.restart();
  }
  
  delay(50);

  printWiFiInfo();

  server.begin();
}

void serverHandler(void *parameter){
	for(;;){
		WiFiClient client = server.available();
		
		if (client) 
		{
			while (client.connected()) 
			{  
				#ifndef TEST
				if( uxQueueMessagesWaiting(messageQueue) > msg_send_count)
				{
          DEBUG_PRINTLN("Sending data");
					uint8_t dataToSend[msg_send_count * msg_size];
					CanMessage canMsg;
					for(int i = 0; i < msg_send_count; i++)
					{
						if(xQueueReceive(messageQueue, &(canMsg), (TickType_t) 0) == pdPASS)
						{
							printCanMsg(canMsg);
							memcpy(dataToSend + msg_size * i, canMsg.msg, msg_size);
						}
					}
					client.write(dataToSend, msg_send_count * msg_size);
				}
				#else
					uint8_t data[12];
					generateTestData(1582, data);
					client.write(data, msg_size);
				#endif
			}
			client.stop();	 
		}
		delay(10);
	}
}


