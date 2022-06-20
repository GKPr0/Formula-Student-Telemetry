#include "debug.h"

void printWiFiInfo()
{
  IPAddress IP = WiFi.softAPIP();
  
  DEBUG_PRINTLN("Network " + String(ssid) +" is running");
  DEBUG_PRINT("AP IP address: ");
  DEBUG_PRINTLN(IP);

  int8_t power = 0;
  esp_wifi_get_max_tx_power(&power);
  DEBUG_PRINT("Max tx power set to: ");
  DEBUG_PRINT((float)(power/4));
  DEBUG_PRINTLN("dBm");

  uint8_t protocol;
  esp_wifi_get_protocol(WIFI_IF_AP, &protocol);
  DEBUG_PRINT("Protocol set to:");
  DEBUG_PRINTLN(protocol);
}

void printBinary(byte b) 
{
  for (int i = 7; i >= 0; i-- )
  {
    DEBUG_PRINT((b >> i) & 0X01);
  }
  DEBUG_PRINT(" ");
}

void printHex(byte b) 
{
   if (b < 10) {DEBUG_PRINT("0");}

   DEBUG_PRINT(b, HEX);
   DEBUG_PRINT(" ");

}

void printCanMsg(CanMessage &msg)
{
  for(int i = 0; i < msg_size; i++){
    if(i == 0)
      DEBUG_PRINT("ID: ");
    else if(i == 4)
      DEBUG_PRINT("Data: ");
    printHex(msg.msg[i]);
  }
  DEBUG_PRINT("\n");
}

void generateTestData(uint32_t id, uint8_t *data)
{
  for(int i(0); i < 4; i ++){
    *data = ((uint8_t*)&id)[3-i];
    data++;
  }

  data[4] = (uint8_t) 215;
  data[5] = (uint8_t) 196;
  data[6] = (uint8_t) 0;
  data[7] = (uint8_t) 0;
  data[8] = (uint8_t) 128;
  data[9] = (uint8_t) 13;
  data[10] = (uint8_t) 32;
  data[11] = (uint8_t) 64;
}
