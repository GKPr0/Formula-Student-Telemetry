#include <Arduino.h>
#include "wifiClient.h"
#include "can.h"
#include "debug.h"

TaskHandle_t wifiTask;

// COM settings
const uint baud_rate = 256000;

// Queue init
const size_t msg_queue_size = 100;
QueueHandle_t messageQueue =  xQueueCreate(msg_queue_size, sizeof(CanMessage));

void setup() {
  Serial.begin(baud_rate); //921600 buad/s-> max speed of CP2102

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