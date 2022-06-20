#include "can.h"
#include "debug.h"

// the variable name CAN_cfg is fixed, do not change 
CAN_device_t CAN_cfg;

void canSetup()
{  
  // Set CAN pins and baudrate
  CAN_cfg.speed = can_speed;
  CAN_cfg.tx_pin_id = can_tx_pin;
  CAN_cfg.rx_pin_id = can_rx_pin;
  
  // Create a queue for CAN receiving 
  CAN_cfg.rx_queue = xQueueCreate(can_queue_size, sizeof(CAN_frame_t));
  
  // Initialize CAN Module
  if(ESP32Can.CANInit() != 0){
    DEBUG_PRINTLN("CAN failed to initialize");
    ESP.restart();
  }
  DEBUG_PRINTLN("CAN setup complete");
}

void canHandler(void *parameter) 
{
  for(;;){
    CAN_frame_t rx_frame;
    CanMessage canMsg;
    // Receive next CAN frame from queue
    if(xQueueReceive(CAN_cfg.rx_queue, &rx_frame, 10*portTICK_PERIOD_MS) == pdPASS)
    { 
      // take data only if Standart Frame and not RTR
      if(rx_frame.FIR.B.FF==CAN_frame_std && rx_frame.FIR.B.RTR != CAN_RTR)
      {
        canMsg = convertCanFrameToCanMessage(rx_frame);
        //printCanMsg(canMsg);
        if(xQueueSend( messageQueue, (void *) &canMsg, 100*portTICK_PERIOD_MS) != pdPASS)
        {
          DEBUG_PRINTLN("Failed to send Can message to queue");
        }
      }
    }
  }
}

CanMessage convertCanFrameToCanMessage(CAN_frame_t &dataPack)
{
  CanMessage canMsg;

  // ID bytes
  for(int i(3); i >= 0; i--)
  {
    canMsg.msg[3 - i] = ((uint8_t*)&dataPack.MsgID)[i];
  }

  // data bytes
  for(int i(0); i < 8; i ++)
  {
    canMsg.msg[4 + i] = dataPack.data.u8[i];
  }

  return canMsg;
}

