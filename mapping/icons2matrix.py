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

import os, sys
from PIL import Image
import os
import re
import json

size = 10, 10
folder = 'img'
files = [f for f in os.listdir(folder) if re.match(r'[a-z]+.*\.png', f)]

icons = {}

for file in files:
    try:
        infile = folder + "/" + file
        outfile = os.path.splitext(infile)[0] + "_small.jpg"
        icon_name = file.split('.')[0]
        
        # converting img to jpg with black background
        im_png = Image.open(infile)
        
        bg = Image.new('RGB',im_png.size,(0,0,0))
        bg.paste(im_png,(0,0),im_png)
        bg.save(infile.split('.')[0] + ".jpg", subsampling=0, quality=100)    
        
        old_width, old_height = im_png.size
        im = Image.open(infile.split('.')[0] + ".jpg")
        # reduce image size
        if(old_width > size[0] or old_height > size[1]):
            im.thumbnail(size, Image.NEAREST)
            im.save(outfile, "JPEG")
            im_small = Image.open(outfile)
        else:
            im_small = im
            
        # reading pixel color
        width, height = im_small.size
        
        icon_data = []
        for y in range(height):
            for x in range(width):
                r, g, b = im_small.getpixel((x, y))
                icon_data.append((r,g,b))
        
        icons[icon_name] = icon_data
    except Exception as e:
        print("Error processing file: " + file + " | " + str(e))

with open('icons.txt', 'w') as file:
    file.write(json.dumps(icons))