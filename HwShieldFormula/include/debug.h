#ifndef DEBUG_H
#define DEBUG_H

#include "server.h"
#include <esp_wifi.h>
#include "can.h"

extern bool debug_enabled;

#define DEBUG_PRINTLN(msg) if(debug_enabled) Serial.println(msg)
#define DEBUG_PRINT(msg, args...) if(debug_enabled) Serial.print(msg, ##args)

// Also GPIO_15 must be pulled down in order to do not show boot log.
#define CONFIG_BOOTLOADER_LOG_LEVEL_NONE 1
#define CONFIG_BOOTLOADER_LOG_LEVEL 0


void printWiFiInfo();

void printBinary(byte b);
void printHex(byte b);
void printCanMsg(CanMessage &msg);

void generateTestData(uint32_t id, uint8_t *data);
#endif
