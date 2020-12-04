# The MIT License (MIT)
#
# Copyright (c) 2020 Dan Halbert for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ble_adafruit.tone_service`
================================================================================

BLE access to play tones.

* Author(s): Dan Halbert
"""

__version__ = "1.2.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit.git"

import struct

from _bleio import PacketBuffer

from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic, ComplexCharacteristic
from adafruit_ble_adafruit.adafruit_service import AdafruitService


class _TonePacket(ComplexCharacteristic):
    uuid = AdafruitService.adafruit_service_uuid(0xC01)

    format = "<HI"
    format_size = struct.calcsize(format)

    def __init__(self):
        super().__init__(
            properties=Characteristic.WRITE,
            read_perm=Attribute.NO_ACCESS,
            max_length=self.format_size,
            fixed_length=True,
        )

    def bind(self, service):
        """Binds the characteristic to the given Service."""
        bound_characteristic = super().bind(service)
        return PacketBuffer(bound_characteristic, buffer_size=1)


class ToneService(AdafruitService):
    """Play tones."""

    uuid = AdafruitService.adafruit_service_uuid(0xC00)
    _tone_packet = _TonePacket()
    """
    Tuple of (frequency: 16 bits, in Hz, duration: 32 bits, in msecs).
    If frequency == 0, a tone being played is turned off.
    if duration == 0, play indefinitely.
    """

    def __init__(self, service=None):
        super().__init__(service=service)
        self._tone_packet_buf = bytearray(_TonePacket.format_size)

    @property
    def tone(self):
        """Return (frequency, duration), or None if no value available"""
        buf = self._tone_packet_buf
        if self._tone_packet.readinto(buf) == 0:
            # No new values available.
            return None
        return struct.unpack(_TonePacket.format, buf)

    def play(self, frequency, duration):
        """
        Frequency is in Hz. If frequency == 0, a tone being played is turned off.
        Duration is in seconds. If duration == 0, play indefinitely.
        """
        self._tone_packet = struct.pack(
            _TonePacket.format,
            frequency,
            0 if duration == 0 else int(duration * 1000 + 0.5),
        )
