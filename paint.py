# NeoPixel library strandtest example
# Author: ANsel Zandegran
# Thanks to  Tony DiCola (tony@tonydicola.com) for the SPI interface code
#

import  Image, time
from array import *
import struct
from neopixel import *
# Configurable values
filename  = "wave.jpg"

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


def pushPixels():
	for x in range(width):
			for i in range(strip.numPixels()):
				value = pixels[x, i]
				#colortoset=getColor(value[0],value[1],value[2])
				colortoset=getColor(gamma[value[1]],gamma[value[0]],gamma[value[2]])
				strip.setPixelColor(i, colortoset)
			strip.show()
			time.sleep(0.003)
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,0))
	strip.show()
	time.sleep(2)

def getColor(r,g,b):
	#print str(r)+" "+str(g)+" "+str(b)
	return Color(r,g,b)


# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	print "Loading..."
	img       = Image.open(filename).convert("RGB")
	pixels    = img.load()
	width     = img.size[0]
	height    = img.size[1]
	print "%dx%d pixels" % img.size
	# To do: add resize here if image is not desired height


	# Calculate gamma correction table.  This includes
	# LPD8806-specific conversion (7-bit color w/high bit set).
	# gamma = [0 for x in range(256)]
	# for i in range(256):
	# 	gamma[i] =  0x80 |int(pow(float(i) / 255.0, 2.5) * 127.0 + 0.5)
	gamma = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]
	 
	
	print "Allocating..."
	column = [[0 for y in range(height*3)] for x in range(width)] 
	# Convert 8-bit RGB image into column-wise GRB bytearray list.
	print "Converting..."
	for x in range(width):
		for y in range(height):
			value = pixels[x, y]
			#print value
			y3 = y * 3
			column[x][y3]     = gamma[value[0]]
			column[x][y3 + 1] = gamma[value[1]]
			column[x][y3 + 2] = gamma[value[2]]
	print ('Press Ctrl-C to quit.')
	while True:
		pushPixels()

