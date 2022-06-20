#include <Arduino.h>
#include "wifiClient.h"
#include "can.h"
#include "debug.h"

TaskHandle_t wifiTask;

// COM settings
const uint baud_rate = 256000;

// Queue init
const size_t msg_queue_size = 1000;
QueueHandle_t messageQueue =  xQueueCreate(msg_queue_size, sizeof(CanMessage));

// Config pin numbers
const int debugPin = GPIO_NUM_15; 
const int wifiModePin = GPIO_NUM_33;

//Default user config
bool debug_enabled = false;
uint8_t wifi_protocol = 8; // 7=802.11/b/g/r, 8=802.11lr

void applyUserConfig()
{
  pinMode(debugPin, INPUT_PULLUP);
  pinMode(wifiModePin, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(debugPin), [](){ESP.restart();}, CHANGE);
  attachInterrupt(digitalPinToInterrupt(wifiModePin), [](){ESP.restart();}, CHANGE);

  int isProductionMode = digitalRead(debugPin);
  int isLRWifiMode = digitalRead(wifiModePin);

  if(isProductionMode == LOW){
    debug_enabled = true;
    DEBUG_PRINTLN("Debug mode");
  }

  if(isLRWifiMode == LOW){
    wifi_protocol = 7;
    DEBUG_PRINTLN("802.11.b/g/n mode");
  }else{
    DEBUG_PRINTLN("802.11.LR mode");
  }
}

void setup() {
  Serial.begin(baud_rate); //921600 buad/s-> max speed of CP2102

  applyUserConfig();

  DEBUG_PRINTLN("Starting client shield");

  wifiSetupOrReconnect();
  delay(50);

  // Run WifiHandler on core 0
  xTaskCreatePinnedToCore(
    wifiHandler,     /* Function to implement the task */
    "WiFiHandler",   /* Name of the task */
    10000,           /* Stack size in words */
    NULL,            /* Task input parameter */
    0,               /* Priority of the task */
    &wifiTask,       /* Task handle. */
    0);              /* Core where the task should run */
  
  delay(50);
}

void loop() { 
  CanMessage canMsg;

  if(xQueueReceive(messageQueue, &canMsg, 10*portTICK_PERIOD_MS) == pdPASS)
  {
    printCanMsg(canMsg);
    Serial.write(canMsg.msg, msg_size);
  }
}