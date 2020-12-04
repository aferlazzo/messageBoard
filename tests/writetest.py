import time
import board
import digitalio

# There are 16 registers on the Max7219

#It’s then a matter of sending commands to the Max7219 via the data in, clock and load line.

#For instance, to display the number 4 on digit 1 we would send the command 0x104 (0x01 : use
#digit 1, 0x04 : display the number 4). Which might look something like this :

#     Set LOAD to 1
#     Send 16 bits command and data (0x104 = 0000000100000100), and for each binary digit we
#         set CLOCK to 0
#         send the binary digit
#         set CLOCK to 1.
#     Set LOAD to 0 then set LOAD to 1.

#At this point it might be worth mentioning that the Max7219 can work in two modes, BCD decode on or BCD decode off.

i = 0
while i < 16:
    #print('register ', i)
    if i == 0:
        cmd = int('00000010', 2)
    print('register ', i, ' in binary ', bin(i))  # print in binary
    
    packet = i << 8
    print('16-bit packet with 4-bit command and 8-bit value', bin(packet))
    i += 1


i = 0
while i < 16:
    cmd = i
    value = int("00000000", 2)
    print('cmd ', bin(cmd))  # print in binary
    #print('cmd %4d %8d' bin(cmd), ' value ', value)  # print in binary
    #
    i += 1


#led = digitalio.DigitalInOut(board.D18)
#led.direction = digitalio.Direction.OUTPUT

#button = digitalio.DigitalInOut(board.D4)
#button.direction = digitalio.Direction.INPUT
#button.pull = digitalio.Pull.UP

#while True:
#    led.value = not button.value # light when button is pressed!
