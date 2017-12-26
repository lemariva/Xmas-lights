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

#import colors
import letters
import icons
import gc
from utime import sleep_ms
from ws2812 import WS2812

matrix_width = 10
matrix_height = 10


def letter_to_leds(letter, color, brightness):
    rgb = (255, 255, 255)   # colors.web_colors.get(color)
    rgb = lighter(rgb, brightness)
    if(letter == ' '):
        return [(10, 10, 10)]
    letter_matrix = letters.letters.get(letter)
    letters_rows = len(letter_matrix)

    letter_tupple = []
    for row in range(letters_rows):
        row_data = letter_matrix[row]
        for column in range(len(row_data)):
            pixel = row_data[column]
            if(pixel == 0):
                letter_tupple.append((0, 0, 0))
            else:
                letter_tupple.append(rgb)
    return letter_tupple


def lighter(color, percent):
    if(percent == 1):
        return color
    if(percent == 0):
        return ([0, 0, 0])
    #if(percent < 0.65):		# driver not working ok with percent under 0.65
    #   percent = 0.65
    rcolor = color[0] - color[0] * (1 - percent)
    gcolor = color[1] - color[1] * (1 - percent)
    bcolor = color[2] - color[2] * (1 - percent)
    newcolor = ([(rcolor), (gcolor), (bcolor)])
    return newcolor


chain = WS2812(ledNumber=100, brightness=60)
my_string = "MERRY XMAS AND HAPPY NEW YEAR"
icons_label = ['goomba', 'goomba_move', 'goomba', 'goomba_move', 'mario', 'duck', 'home']

gc.collect()
gc.mem_free()

while True:
    for c in my_string:
        data = letter_to_leds(c, 'White', 0.8)
        if(data != 0):
            chain.show(data)
            sleep_ms(500)
            gc.collect()
            gc.mem_free()
    for icon in icons_label:
        chain.show(icons.icons.get(icon))
        sleep_ms(1500)
        gc.collect()
        gc.mem_free()
