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

from __future__ import print_function
import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import json

def char_to_pixels(text, path='fonts/Arial.ttf', fontsize=14):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    Based on https://stackoverflow.com/a/36386628 (unutbu)
    """
    font = ImageFont.truetype(path, fontsize)
    w, h = font.getsize(text)
    h *= 2
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    return arr

def display(arr):
    result = np.where(arr, '#', ' ')
    print('\n'.join([''.join(row) for row in result]))


letters = {}
# parameters
matrix_height = 10
matrix_width  = 10
font_file = 'fonts/LiberationSerif-Bold.ttf'
font_size = 10

for c in string.ascii_uppercase+string.digits+string.punctuation:
    letter = char_to_pixels(
        c,
        path=font_file,
        fontsize=font_size)
    #setting to matrix dimension and centering letters
    print("letter: " + c)
    print("old shape: " + str(letter.shape))
    [letter_rows, letter_columns] = letter.shape
    if(letter_columns < matrix_width):
        add_columns = matrix_width - letter_columns
        add_columns_l = int(add_columns/2)
        add_columns_r = int(add_columns/2)
        if(add_columns_l + add_columns_r != add_columns):
            add_columns_r += 1
        print("adding: " + str(add_columns_l) + " columns on the left side and " + str(add_columns_r) + " columns on the right side")
        for x in range(add_columns_r):
            letter = np.column_stack((letter, np.zeros(letter_rows, dtype=int)))
        for x in range(add_columns_l):
            letter = np.column_stack((np.zeros(letter_rows, dtype=int), letter))

    if(letter_rows < matrix_height):
        add_row = matrix_height - letter_rows
        add_row_u = int(add_row/2)
        add_row_l = int(add_row/2)
        if(add_row_u + add_row_l != add_row):
            add_row_u += 1
        print("adding: " + str(add_row_u) + " rows at the upper side and " + str(add_row_l) + " rows on the lower side")
        for x in range(add_row_l):
            letter = np.row_stack((letter, np.zeros((1, matrix_height), dtype=int)))
        for x in range(add_row_u):
            letter = np.row_stack((np.zeros((1, matrix_height), dtype=int),letter))

    print("new shape: " + str(letter.shape))
    letters[c] = letter.tolist()
    display(letter)

with open('letters.txt', 'w') as file:
    file.write(json.dumps(letters))
