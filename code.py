import pulseio
import board
import time
import touchio
from digitalio import DigitalInOut, Direction, Pull

# init buttons

touch1 = touchio.TouchIn(board.A0)
touch2 = touchio.TouchIn(board.A1)
touch3 = touchio.TouchIn(board.A2)

# init LEDs

ledG = DigitalInOut(board.D5)
ledG.direction = Direction.OUTPUT
ledR = DigitalInOut(board.D6)
ledR.direction = Direction.OUTPUT

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

# turn red = calibration

ledR.value = False
ledG.value = True

high1 = 0
high2 = 0
high3 = 0

# find low level

for x in range(0,1000):
    v = touch1.raw_value
    if v > high1:
        high1 = v
    v = touch2.raw_value
    if v > high2:
        high2 = v
    v = touch3.raw_value
    if v > high3:
        high3 = v
    time.sleep(.001)

# turn green = action!

ledR.value = True
ledG.value = False

# init PWMs

pwmspk1 = pulseio.PWMOut(board.D1, duty_cycle=0x7fff, frequency=440, variable_frequency=True)
pwmspk2 = pulseio.PWMOut(board.D2, duty_cycle=0x7fff, frequency=440, variable_frequency=True)
pwmspk3 = pulseio.PWMOut(board.D3, duty_cycle=0x7fff, frequency=440, variable_frequency=True)

# use button values to set freqency, no sound if near low level

while True:
    time.sleep(.01)
    v = touch1.raw_value
    if v > high1+10:
        pwmspk1.frequency = v>>2
        pwmspk1.duty_cycle = 0x7fff
    else:
        pwmspk1.duty_cycle = 0
    v = touch2.raw_value
    if v > high2+10:
        pwmspk2.frequency = v>>1
        pwmspk2.duty_cycle = 0x7fff
    else:
        pwmspk2.duty_cycle = 0
    v = touch3.raw_value
    if v > high3+10:
        pwmspk3.frequency = v
        pwmspk3.duty_cycle = 0x7fff
    else:
        pwmspk3.duty_cycle = 0
