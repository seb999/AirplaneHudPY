import time
import math
from smbus2 import SMBus
from micropython_mma8452q import MMA8452Q
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


# Video for ADXL345
# https://www.youtube.com/watch?v=QH1umP-duik

# Setup I2C for OLED & accel
serial = i2c(port=1, address=0x3C)
oled = ssd1306(serial, width=128, height=64)
bus = SMBus(1)
accel = MMA8452Q(bus)

NUM_DOTS = 100
dots = [{'x': math.floor(128 * math.random()), 'y': math.floor(32 + 32 * math.random()), 'speed': 0.1 + math.random() * 0.3} for _ in range(NUM_DOTS)]

smooth_pitch = smooth_roll = 0.0
alpha = 0.1

def read_attitude():
    x, y, z = accel.acceleration  # scaled to g
    roll = math.degrees(math.atan2(y, z))
    pitch = math.degrees(math.atan2(-x, math.hypot(y, z)))
    return roll, pitch

while True:
    roll, pitch = read_attitude()
    smooth_roll = smooth_roll * (1 - alpha) + roll * alpha
    smooth_pitch = smooth_pitch * (1 - alpha) + pitch * alpha
    smooth_roll = max(min(smooth_roll, 45), -45)
    smooth_pitch = max(min(smooth_pitch, 45), -45)

    tilt = math.radians(smooth_roll)
    dx, dy = math.cos(tilt)*80, math.sin(tilt)*80
    cx, cy = 64, 32
    x1, y1 = cx - dx, cy + dy + smooth_pitch
    x2, y2 = cx + dx, cy - dy + smooth_pitch

    with canvas(oled) as draw:
        draw.text((0, 0), f"Pitch: {smooth_pitch:.1f}  Roll: {smooth_roll:.1f}", fill="white")
        draw.line((x1, y1, x2, y2), fill="white")
        draw.line((cx-10, cy, cx+10, cy), fill="white")
        draw.ellipse((cx-2, cy-2, cx+2, cy+2), fill="white")

        for d in dots:
            d['y'] += d['speed']
            if d['y'] >= 64:
                d['y'] = 0
                d['x'] = int(math.random() * 128)
            horizon_y = ((y2 - y1) / (x2 - x1 + 1e-6)) * (d['x'] - x1) + y1
            if horizon_y < d['y'] < 64:
                draw.point((d['x'], int(d['y'])), fill="white")

    oled.show()
    time.sleep(0.03)
