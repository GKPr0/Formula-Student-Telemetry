#include <Arduino.h>
#include <Wifi.h>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

uint8_t b = 255;
uint8_t data[12];

void setup() {
  Serial.begin(921600); //921600 buad-> max speed of CP2102

  for(int i = 0; i < 12; i++)
  {
    data[i] = b;
  }
}

void loop() {
  
  Serial.write(data, 12);
  
}