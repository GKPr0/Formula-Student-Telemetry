#include <Arduino.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "server.h"
#include "can.h"
#include "debug.h"
#include "soc/timer_group_struct.h"
#include "soc/timer_group_reg.h"

//Uncomment following line to enable TEST mode (simalution of can messages)
//#define TEST

TaskHandle_t canTask;
TaskHandle_t serverTask;

// COM settings
const uint baud_rate = 256000;

// Config pin numbers
const int debugPin = GPIO_NUM_15; 
const int wifiModePin = GPIO_NUM_33;

// Queue init
const size_t msg_queue_size = 1000; 
const size_t msg_send_count = 700;
QueueHandle_t messageQueue =  xQueueCreate(msg_queue_size, sizeof(CanMessage));

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
  Serial.begin(baud_rate);

  applyUserConfig();

  canSetup();
  delay(50);

  serverSetup();
  delay(50);
  
  // Run CanHandler on core 1
  xTaskCreatePinnedToCore(
    canHandler,      /* Function to implement the task */
    "CanHandler",    /* Name of the task */
    10000,           /* Stack size in words */
    NULL,            /* Task input parameter */
    0,               /* Priority of the task */
    &canTask,        /* Task handle. */
    1);              /* Core where the task should run */
  
  delay(50);

  // Run ServerHandler on core 0
  xTaskCreatePinnedToCore(
    serverHandler,   /* Function to implement the task */
    "ServerHandler", /* Name of the task */
    20000,           /* Stack size in words */
    NULL,            /* Task input parameter */
    0,               /* Priority of the task */
    &serverTask,     /* Task handle. */
    0);              /* Core where the task should run */
  
  delay(50);

}

void loop() {
  //Delete arduino framework main task (loop)
  vTaskDelete(NULL);
}

