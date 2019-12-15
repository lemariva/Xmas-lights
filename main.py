#Copyright [2017] [Mauro Riva <lemariva@mail.com> <lemariva.com>]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

#The above copyright notice and this permission notice shall be
#included in all copies or substantial portions of the Software.

import gc
#import colors
from chars import chars_to_leds

import icons
from utime import sleep_ms
from wipyWS2812.ws2812 import WS2812
#from m5stack import buttonA, buttonB, buttonC

matrix_width = 16
matrix_height = 16

characters = {}

def char_to_leds(character, color, brightness):
    rgb = (255, 255, 255)   # colors.web_colors.get(color)
    rgb = lighter(rgb, brightness)
    if character == ' ':
        return [(16, 16, 16)]

    char_matrix = characters.get(character)
    if char_matrix is None:
        char_matrix = characters.get(character)

    if char_matrix is None:
        return [(16, 16, 16)]
    else:
        chars_rows = len(char_matrix)

    char_tupple = []
    for row in range(chars_rows):
        row_data = char_matrix[row]
        for column in range(len(row_data)):
            pixel = row_data[column]
            if pixel == 0:
                char_tupple.append((0, 0, 0))
            else:
    #pycom.rgbled(0x050505)
                char_tupple.append(rgb)
    return char_tupple


def lighter(color, percent):
    if percent == 1:
        return color
    if percent == 0:
        return ([0, 0, 0])
    #if(percent < 0.65):		# driver not working ok with percent under 0.65
    #   percent = 0.65
    rcolor = color[0] - color[0] * (1 - percent)
    gcolor = color[1] - color[1] * (1 - percent)
    bcolor = color[2] - color[2] * (1 - percent)
    newcolor = ([(rcolor), (gcolor), (bcolor)])
    return newcolor

my_string = "MERRY XMAS & HAPPY 2020!"
icons_label = ['pinguin', 'santa', 'gift', 'rudolf']

# reducing memory use

for character in my_string:
    char_matrix = chars_to_leds.get(character)
    if char_matrix is not None:
        characters[character] = char_matrix

chars_to_leds = None
gc.collect()

chain = WS2812(ledNumber=256, brightness=0.7)

while True:
    for c in my_string:
        data = char_to_leds(c, 'White', 0.2)
        if data != 0:
            chain.show(data)
            sleep_ms(500)
            gc.collect()

    for icon in icons_label:
        chain.show(icons.icons.get(icon))
        sleep_ms(1000)
        gc.collect()