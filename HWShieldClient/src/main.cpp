#include <Arduino.h>
#include <Wifi.h>

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

void setup() {
  Serial.begin(1024000);
}

void loop() {
  while(Serial.available())
  {
    Serial.write("Ahoj");
  }
  delay(1);
}