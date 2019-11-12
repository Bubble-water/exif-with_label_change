from __future__ import division
import xml.etree.ElementTree as ET
import os
from PIL import Image, ImageDraw, ImageFile,ImageFont
ImageFile.LOAD_TRUNCATED_IMAGES =True

# picture_path = "data/demo.jpg"
picture_path = "result/demo.jpg"
# xml_path = "data/demo.xml"
xml_path = "result/demo.xml"
img = Image.open(picture_path)
img = img.convert("RGB")
draw = ImageDraw.Draw(img)
tree = ET.parse(xml_path)
rootll = tree.getroot()
for obj in rootll.iter("object"):
    cls = obj.find("name").text
    xmlbox = obj.find("bndbox")
    xmin = int(xmlbox.find("xmin").text)
    ymin = int(xmlbox.find("ymin").text)
    xmax = int(xmlbox.find("xmax").text)
    ymax = int(xmlbox.find("ymax").text)
    # draw.rectangle((xmin, ymin, xmax, ymax), outline=(255, 0, 255))
    draw.line([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)], width=6,fill=(255, 0, 255))
    Font1 = ImageFont.truetype("C:\Windows\Fonts\simsunb.ttf", 200)
    draw.text((xmin+30, ymin-180), cls, fill=(255, 0, 0), font=Font1)
# img.save("picture/source.jpg")
img.save("picture/result.jpg")