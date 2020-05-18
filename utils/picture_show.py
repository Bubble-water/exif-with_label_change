from __future__ import division
import xml.etree.ElementTree as ET
import os
from PIL import Image, ImageDraw, ImageFile,ImageFont
ImageFile.LOAD_TRUNCATED_IMAGES =True

def save_picture_xml(img_path,xml_path,save_path):
    """
    function:输入图片img_path和其xml(xml_path)文件，并根据xml信息将标注信息在图片上显示并保存在save_path路径下面
    """
    picture_name = os.path.split(img_path)
    img = Image.open(img_path)
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
        draw.rectangle((xmin, ymin, xmax, ymax), outline=(255, 0, 255))
        Font1 = ImageFont.truetype("C:\\Windows\\Fonts\\simsunb.ttf", 200)
        draw.text((xmin+30, ymin-180), cls, fill=(255, 0, 0), font=Font1)
    final_path = os.path.join(save_path,picture_name[-1])
    img.save(final_path)

if __name__=='__main__':
    img_path = "../data/demo.jpg"
    xml_path = "../data/demo.xml"
    save_path = "../picture/"
    save_picture_xml(img_path,xml_path,save_path)