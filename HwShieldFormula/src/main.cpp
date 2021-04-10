#include <Arduino.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "server.h"
#include "can.h"
#include "soc/timer_group_struct.h"
#include "soc/timer_group_reg.h"

TaskHandle_t canTask;
TaskHandle_t serverTask;

// Queue init
const size_t msg_queue_size = 1000; 
const size_t msg_send_count = 700;
QueueHandle_t messageQueue =  xQueueCreate(msg_queue_size, sizeof(CanMessage));

void test(void *param){
  for(;;){
    if( uxQueueMessagesWaiting(messageQueue) > msg_send_count)
    {
      Serial.println("Sending data");
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

      for(int i = 0; i < msg_send_count * msg_size; i++){
        Serial.print(dataToSend[i]);
      }
    }
  }
}

void setup() {
  Serial.begin(115200);

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

