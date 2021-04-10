#include "can.h"
#include "debug.h"

void printBinary(byte b) 
{
  for (int i = 7; i >= 0; i-- )
  {
    DEBUG_PRINT((b >> i) & 0X01);
  }
  DEBUG_PRINT(" ");
}

void printHex(byte b) 
{
   if (b < 10) {DEBUG_PRINT("0");}

   DEBUG_PRINT(b, HEX);
   DEBUG_PRINT(" ");

}

void printCanMsg(CanMessage &msg)
{
  for(int i = 0; i < msg_size; i++){
    if(i == 0)
      DEBUG_PRINT("ID: ");
    else if(i == 4)
      DEBUG_PRINT("Data: ");
    printHex(msg.msg[i]);
  }
  DEBUG_PRINT("\n");
}