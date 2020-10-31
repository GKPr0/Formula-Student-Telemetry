#ifndef CAN_H
#define CAN_H

#include <Arduino.h>
#include <ESP32CAN.h>
#include <CAN_config.h>

struct canDataPack{
    uint32_t canID = 0;
    uint8_t canData [8] = {[0 ... 7] = 0};  // Works only with gcc compiler!
};

void canSetup(const size_t &can_queue_size);

canDataPack canReceive();

void convertDataPackToByteArray(uint8_t* data, canDataPack & dataPack);

void printBinary(byte b);
void printHex(byte b);

void generateTestData(uint32_t id ,uint8_t* data);
#endif