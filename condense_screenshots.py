#!/usr/bin/env python3
import tomlkit
school_list_filename = "schools.toml"

from PIL import Image

with open(school_list_filename) as s_file:
    toml_string = s_file.read()
schools = tomlkit.parse(toml_string)['school']

summery_filename = ("summery.jpeg")
thumbsize = (700, 700)
summery = None
for index, school in enumerate(schools):
    school_name = schools[school]['name']
    image_filename = school_name + "_status.png"

    im = Image.open(image_filename)
    im.thumbnail(thumbsize)

    if summery == None:
        summery = Image.new("RGB", (im.size[0]*3, im.size[1]*2))

    x = index // 2 * im.size[0]
    y = index % 2 * im.size[1]

    w, h = im.size

    summery.paste(im, (x,y,x+w, y+h))
summery.save(summery_filename)
