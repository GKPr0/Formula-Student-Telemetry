#ifndef CAN_H
#define CAN_H

#include <Arduino.h>
#include <ESP32CAN.h>
#include <CAN_config.h>

extern QueueHandle_t messageQueue;

static const size_t msg_size = 12;
static const size_t can_queue_size = 100;

static const CAN_speed_t can_speed = CAN_SPEED_1000KBPS;
static const gpio_num_t can_tx_pin  = GPIO_NUM_26;
static const gpio_num_t can_rx_pin  = GPIO_NUM_25;

struct CanMessage{
  uint8_t msg[msg_size];
};

void canSetup();
void canHandler(void *parameter);

CanMessage convertCanFrameToCanMessage(CAN_frame_t &dataPack);

#endif
