#include <can.hpp>

// the variable name CAN_cfg is fixed, do not change 
CAN_device_t CAN_cfg;

void printBinary(byte b) {
  for (int i = 7; i >= 0; i-- )
  {
    Serial.print((b >> i) & 0X01);//shift and select first bit
  }
  Serial.print(" ");
}

void printHex(byte b) {

   if (b < 10) {Serial.print("0");}

   Serial.print(b, HEX);
   Serial.print(" ");

}

void canSetup() {    
    Serial.println("Setting up Can...");
    /* set CAN pins and baudrate */
    CAN_cfg.speed = CAN_SPEED_1000KBPS;
    CAN_cfg.tx_pin_id = GPIO_NUM_5;
    CAN_cfg.rx_pin_id = GPIO_NUM_14;
    /* create a queue for CAN receiving */
    CAN_cfg.rx_queue = xQueueCreate(10,sizeof(CAN_frame_t));
    //initialize CAN Module
    ESP32Can.CANInit();
    Serial.println("Can setup complete");
}

canDataPack canReceive() {
    CAN_frame_t rx_frame;
    canDataPack dataPack;
    dataPack.canID = 000;
    for(int i = 0; i< 8; i ++){
      dataPack.canData[i] = 0;
    }
    //receive next CAN frame from queue
    if(xQueueReceive(CAN_cfg.rx_queue,&rx_frame, 3*portTICK_PERIOD_MS)==pdTRUE){

      //do stuff!
      if(rx_frame.FIR.B.FF==CAN_frame_std)
        printf("New standard frame");
      else
        printf("New extended frame");

      if(rx_frame.FIR.B.RTR==CAN_RTR)
        printf(" RTR from 0x%08x, DLC %d\r\n",rx_frame.MsgID,  rx_frame.FIR.B.DLC);
      else{
        printf(" from 0x%08x, DLC %d\n",rx_frame.MsgID,  rx_frame.FIR.B.DLC);
        dataPack.canID = rx_frame.MsgID;
        for(int i = 0; i < 8; i++){
          //Serial.print((h)rx_frame.data.u8[i]);
          //printBinary(rx_frame.data.u8[i]);
          printHex(rx_frame.data.u8[i]);
          dataPack.canData[i] = rx_frame.data.u8[i];
        }
        Serial.print("\n");
      }
    }
    return dataPack;
}

String canDataToHexString(uint8_t rawData[]){  
  String canData;
  char tmp [3];
  for(int i = 0; i < 8; i++){
     snprintf(tmp,4, "%02x", rawData[i]);
     canData += tmp;
  }
 
  return canData;
}

String canIdToString(uint32_t rawId){
  char tmp [4];
  snprintf(tmp, 32, "%03x", rawId);

  String canId(tmp);

  return canId;
}

String convertDataPackToString(canDataPack dataPack){
  String canData = canDataToHexString(dataPack.canData);
  String canId = canIdToString(dataPack.canID);
  
  String canMsg = "ID" + canId + "X" + canData;

  return canMsg;
}
