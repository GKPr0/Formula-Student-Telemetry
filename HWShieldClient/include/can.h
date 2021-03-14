#ifndef CAN_H
#define CAN_H

#include <Arduino.h>

const size_t msg_size = 12;

struct CanMessage{
  uint8_t msg[msg_size];
};

void printBinary(byte b);

void printHex(byte b);

void printCanMsg(CanMessage &msg);

#endif