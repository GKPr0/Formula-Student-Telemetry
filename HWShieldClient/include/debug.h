#ifndef DEBUG_H
#define DEBUG_H

//#define DEBUG

#ifdef DEBUG
    #define DEBUG_PRINTLN(msg) Serial.println(msg)
    #define DEBUG_PRINT(msg, args...) Serial.print(msg, ##args)
#else
    // Also GPIO_15 must be pulled down in order to do not show boot log.
    #define CONFIG_BOOTLOADER_LOG_LEVEL_NONE 1
    #define CONFIG_BOOTLOADER_LOG_LEVEL 0

    #define DEBUG_PRINTLN(msg) do {} while (0)
    #define DEBUG_PRINT(msg, args...) do {} while (0)
#endif

#endif
