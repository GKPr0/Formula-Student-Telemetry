#ifndef CAN_H
#define CAN_H

#include <Arduino.h>
#include <ESP32CAN.h>
#include <CAN_config.h>

struct canDataPack{
    uint32_t canID;
    uint8_t canData [8];
};

void printBinary(byte b);
void printHex(byte b);

void canSetup();
canDataPack canReceive();

String convertDataPackToString(canDataPack dataPack);
void convertDataPackToByteArray(uint8_t* data, canDataPack & dataPack);

String canDataToHexString(uint8_t rawData[]);
String canIdToString(uint32_t rawId);

#endif