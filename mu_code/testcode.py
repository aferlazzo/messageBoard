# Write your code here :-)

# gpiozero is a simple interface to GPIO devices with Raspberry Pi
from gpiozero import LED
import time

#   RPi Zero's pinouts Should be

#   RPI Signal  GPIO     PCB-to-Max7219# Python program to
#  print the binary value
# of the numbers from 1 to N

#   pin Name    Name    PCB pin
#   6   GND     Ground  1
#   19  DIN     GPIO10  2
#   24  CS      GPIO8   3
#   23  SCLK    GPIO11  4   Chip Select
#   2   5V      VCC     5

#
# 7219 commands are ('16-bit packet with 4-bit junk,
# 4-bit command and 8-bit data', bin(packet))

DIN = LED(19)
# input the value of n
n = int(input("Enter the value to send: "))

DIN.value = n
time.sleep(0.5)
print("n: ", bin(n))
print("DIN: ", bin(DIN.value))