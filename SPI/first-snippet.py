#!/usr/bin/python

import spidev
import time

spi0=spidev.SpiDev()
spi1=spidev.SpiDev()
spi0.open(0,0) #(channel0,CE0)
spi1.open(0,1) #(channel0,CE1)
spi0.max_speed_hz=10000
spi1.max_speed_hz=10000
while True:
    resp0 = spi0.xfer2([0x00])
    resp1 = spi1.xfer2([0x00])
    print ("{} {:.3f} : {} {:.3f}"
          .format(resp0[0],resp0[0]*3.3/256,resp1[0],resp1[0]*3.3/256))
    time.sleep(0.25)
