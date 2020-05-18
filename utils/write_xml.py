import shutil
from PIL import Image
headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""
objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''

def write_xml(anno_path, head, objs, tail, mark_xml=0):
    f = open(anno_path, "w")
    f.write(head)
    if mark_xml == 0:
        for obj in objs:
            f.write(objstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
        f.write(tail)
        f.close()
    else:
        f.write(tail)
        f.close()

def save_annotations_and_imgs(image_path, anno_path, img_info, objs):

    if objs is None:
        mark_xml = 1
    else:
        mark_xml = 0

    w, h, channel = img_info
    if (channel == 1):
        print(image_path + " not a RGB image")
        return
    #print("headstr:",headstr)
    head = headstr % (image_path, w, h, channel)
    tail = tailstr
    write_xml(anno_path, head, objs, tail, mark_xml)
