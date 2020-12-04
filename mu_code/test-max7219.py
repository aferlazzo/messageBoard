
import RPi.GPIO as GPIO
import time

"""

Output in terminal window should be:

Starting test-max7219.py
Setting the RPi's GPIO pins 
19, 23, 12, and 24 to be output pins

Setting the RPi's GPIO pins 24 CS (Chip Select) 
LOW then HIGH

Setting the RPi's GPIO pins 12 SCLK (Clock) 
LOW then HIGH

Preparing to send Max7219 the command data to set LED display 
intensity to max: 0b101000001111
That is, Max7219: initiate a transfer of command 
data by lowering and raising the SCLK pin

Max7219 was told to set LED display intensity: 
GPIO.output(GPIO10, 0b101000001111)

Preparing to send Max7219 the command data to resume normal 
operation: 0b001100000001
That is, Max7219: initiate a transfer of command 
data by lowering and raising the SCLK pin

Max7219 was told to resume normal operation: 
GPIO.output(GPIO10, 0b001100000001)

Preparing to send Max7219 the command data to perform 
a display test: 0b1111000000
That is, Max7219: initiate a transfer of command 
data by lowering and raising the SCLK pin

Max7219 was told to light all the dots, which is the 
display test: GPIO.output(GPIO1, 0b111100000000)

Sleep for 5 seconds

Cleanup and Ending test-max7219.py
"""

#   define GPIO pin mappings
GPIO10 = 19   # pin 19 aka SPI pin MOSI
GPIO11 = 23   # pin 23 aka SPI Pin SCLK
SCLK = 23
CLK = 12      # pin 12 aka CLK
CS = 24       # pin 24 aka CS (Chip Select GPIO8)
LOW = 0x00
HIGH = 0xff

#   First, set the mode to address GPIOs via their GPIO number using
#   the following command
GPIO.setmode(GPIO.BCM)

#   Next, pins 19, 23, 12, and 24 will be set to be output pins
print("\nStarting test-max7219.py\nSetting the RPi's GPIO pins ")
print("19, 23, and 24 to be output pins\n")
GPIO.setup(GPIO10, GPIO.OUT)
GPIO.setup(GPIO11, GPIO.OUT)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(SCLK, GPIO.OUT)

#   The Decode Mode is set to no decode by default

#   To start programming Max7219, set CS LOW then HIGH and SCLK LOW then HIGH
print("Setting the RPi's GPIO pins 24 CS (Chip Select) " )
print("LOW then HIGH\n")
GPIO.output(CS, LOW)
GPIO.output(CS, HIGH)

#   drive CLOCK LOW then HIGH
print("Setting the RPi's GPIO pins 23 SCLK (SPI Clock) ")
print("LOW then HIGH\n")
GPIO.output(SCLK, LOW)
GPIO.output(SCLK, HIGH)

# now set CS to 0 for the rest of the script
GPIO.output(CS, 0)

#   Display intensity is address 0x0a / 0b1010 (command portion) and
#   portion 0x0f
#                     1234         4-bits command hex A = binary 1010
#                         12345678 8-bits data
GPIO.output(GPIO10, 0b101000001111)
print("Preparing to send Max7219 the command data to set LED display ")
print("intensity to max: 0b101000001111")
print("That is, Max7219: initiate a transfer of command ")
print("data by lowering and raising the SCLK pin\n")

#   Perform the data load into the register on Clock's rising edge
GPIO.output(GPIO11, LOW)
GPIO.output(GPIO11, HIGH)

print("Max7219 was told to set LED display intensity: ")
print("GPIO.output(GPIO10, 0b101000001111)\n")

#   Scan Limit Register set number of digits displayed We have 5-column LEDs
#   so set Command 0x0b and Data 0x05


#                     1234         4-bits command hex B = binary 1011
#                         12345678 8-bits data (not used by chip)
GPIO.output(GPIO10, 0b101100000101)
print("Preparing to send Max7219 the command data to limit ")
print("the display to 5 columns of dots: 0b1011000101")
print("That is, Max7219: initiate a transfer of command ")
print("data by lowering and raising the SCLK pin\n")

#   Data is loaded into the register on Clock's rising edge
GPIO.output(GPIO11, LOW)
GPIO.output(GPIO11, HIGH)

print("Max7219 was told to limit the scan to 5 digits of columns, which is the ")
print("Scan limit register: GPIO.output(GPIO1, 0b101100000101)\n")



#   From page 7 of datasheet, at initial power up of Max7219 enters
#   Shutdown mode. Table 3, Shutdown Register
#   The command to resume Normal Operation
#                     1234         4-bits command hex C = binary 1100
#                         12345678 8-bits data
GPIO.output(GPIO10, 0b001100000001)
print("Preparing to send Max7219 the command data to resume normal ")
print("operation: 0b001100000001")
print("That is, Max7219: initiate a transfer of command ")
print("data by lowering and raising the SCLK pin\n")

#   Perform the data load into the register on Clock's rising edge
GPIO.output(GPIO11, LOW)
GPIO.output(GPIO11, HIGH)

print("Max7219 was told to resume normal operation: ")
print("GPIO.output(GPIO10, 0b001100000001)\n")


#   From page 7, Table . Display Test Register
#   The command to test the LED by lighting all dots
#                     1234         4-bits command hex F = binary 1111
#                         12345678 8-bits data
GPIO.output(GPIO10, 0b111100000001)
print("Preparing to send Max7219 the command data to perform ")
print("a display test: 0b1111000001")
print("That is, Max7219: initiate a transfer of command ")
print("data by lowering and raising the SCLK pin\n")

#   Data is loaded into the register on Clock's rising edge
GPIO.output(GPIO11, LOW)
GPIO.output(GPIO11, HIGH)

print("Max7219 was told to light all the dots, which is the ")
print("display test: GPIO.output(GPIO1, 0b111100000000)\n")

print("Sleep for 5 seconds\n")
#   The command to wait for 5 seconds
time.sleep(5)

#   The command to cleanup all the GPIO pins as expected by the chip
GPIO.cleanup()
print("Cleanup and Ending test-max7219.py\n")

