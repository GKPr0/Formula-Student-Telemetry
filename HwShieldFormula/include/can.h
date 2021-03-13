#ifndef CAN_H
#define CAN_H

#include <Arduino.h>
#include <ESP32CAN.h>
#include <CAN_config.h>

extern QueueHandle_t messageQueue;

const size_t msg_size = 12;
const size_t can_queue_size = 100;

const CAN_speed_t can_speed = CAN_SPEED_1000KBPS;
const gpio_num_t can_tx_pin  = GPIO_NUM_5;
const gpio_num_t can_rx_pin  = GPIO_NUM_14;

struct CanMessage{
  uint8_t msg[msg_size];
};

void canSetup();
void canHandler(void *parameter);

CanMessage convertCanFrameToCanMessage(CAN_frame_t &dataPack);

void printBinary(byte b);
void printHex(byte b);
void printCanMsg(CanMessage &msg);

void generateTestData(uint32_t id, uint8_t *data);

#endif
