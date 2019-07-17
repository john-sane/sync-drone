import neopixel
import board

pixels = neopixel.NeoPixel(pin=board.D21, n=36, brightness=1, pixel_order=neopixel.GRB)

pixels.fill((255, 0, 0))

"""for i in range(8):
    pixels[i] = (0, 255, 0)

for i in range(8, 16):
    pixels[i] = (0, 0, 255)

for i in range(16, 24):
    pixels[i] = (0, 255, 255)

for i in range(24, 32):
    pixels[i] = (255, 0, 255)

pixels.show()"""
print(pixels)