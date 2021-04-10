#include "can.h"

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
    Serial.println("CAN failed to initialize");
    ESP.restart();
  }
  Serial.println("CAN setup complete");
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
          Serial.println("Failed to send Can message to queue");
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

void printBinary(byte b) 
{
  for (int i = 7; i >= 0; i-- )
  {
    Serial.print((b >> i) & 0X01);
  }
  Serial.print(" ");
}

void printHex(byte b) 
{
   if (b < 10) {Serial.print("0");}

   Serial.print(b, HEX);
   Serial.print(" ");

}

void printCanMsg(CanMessage &msg)
{
  for(int i = 0; i < msg_size; i++){
    if(i == 0)
      Serial.print("ID: ");
    else if(i == 4)
      Serial.print("Data: ");
    printHex(msg.msg[i]);
  }
  Serial.print("\n");
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
