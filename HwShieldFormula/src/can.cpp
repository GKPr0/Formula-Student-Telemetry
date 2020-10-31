#include <can.hpp>

// the variable name CAN_cfg is fixed, do not change 
CAN_device_t CAN_cfg;

void canSetup(const size_t &can_queue_size)
{  
  // Set CAN pins and baudrate
  CAN_cfg.speed = CAN_SPEED_1000KBPS;
  CAN_cfg.tx_pin_id = GPIO_NUM_5;
  CAN_cfg.rx_pin_id = GPIO_NUM_4;
  
  // Create a queue for CAN receiving 
  CAN_cfg.rx_queue = xQueueCreate(can_queue_size,sizeof(CAN_frame_t));
  
  // Initialize CAN Module
  if(ESP32Can.CANInit() != 0){
    Serial.println("CAN failed to initialize");
    ESP.restart();
  }
  Serial.println("CAN setup complete");
}

canDataPack canReceive() 
{
  CAN_frame_t rx_frame;
  canDataPack dataPack;
 
  // Receive next CAN frame from queue
  if(xQueueReceive(CAN_cfg.rx_queue, &rx_frame, 3*portTICK_PERIOD_MS)==pdTRUE)
  {
    // take data only if Standart Frame and not RTR
    if(rx_frame.FIR.B.FF==CAN_frame_std)
    {
      if(rx_frame.FIR.B.RTR != CAN_RTR)
      {
        printf(" from 0x%08x, DLC %d\n",rx_frame.MsgID,  rx_frame.FIR.B.DLC);
        dataPack.canID = rx_frame.MsgID;
        for(int i = 0; i < 8; i++)
        {
          //Serial.print((h)rx_frame.data.u8[i]);
          //printBinary(rx_frame.data.u8[i]);
          //printHex(rx_frame.data.u8[i]);
          dataPack.canData[i] = rx_frame.data.u8[i];
        }
        Serial.print("\n");
      }
    }
  }
  return dataPack;
}

void convertDataPackToByteArray(uint8_t* data, canDataPack & dataPack)
{
  // ID bytes
  for(int i(3); i >= 0; i--)
  {
    *data = ((uint8_t*)&dataPack.canID)[i];
    data++;
  }

  // data bytes
  for(int i(0); i < 8; i ++)
  {
    *data = dataPack.canData[i];
    data++;
  }
}

void printBinary(byte b) 
{
  for (int i = 7; i >= 0; i-- )
  {
    Serial.print((b >> i) & 0X01);//shift and select first bit
  }
  Serial.print(" ");
}

void printHex(byte b) 
{
   if (b < 10) {Serial.print("0");}

   Serial.print(b, HEX);
   Serial.print(" ");

}

void generateTestData(uint32_t id, uint8_t *data)
{
  for(int i(0); i < 4; i ++){
    data[i] = ((uint8_t*)&id)[3-i];
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
