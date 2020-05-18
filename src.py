import PIL.Image
import PIL.ImageOps
import numpy as np
import PIL
from utils.write_xml import *
from utils.picture_show import *
from utils.with_label_change import *


def exif_transpose(img, names, obj):
    """
    If an image has an Exif Orientation tag, transpose the image
    accordingly.

    Note: Very recent versions of Pillow have an internal version
    of this function. So this is only needed if Pillow isn't at the
    latest version.

    :param image: The image to transpose.
    :return: An image and annotation.
    """
    if not img:
        return img

    exif_orientation_tag = 274

    # Check for EXIF data (only present on some files)
    if hasattr(img, "_getexif") and isinstance(img._getexif(), dict) and exif_orientation_tag in img._getexif():
        exif_data = img._getexif()
        orientation = exif_data[exif_orientation_tag]

        # Handle EXIF Orientation
        # print("orientation:",orientation)
        if orientation == 1:
            # Normal image - nothing to do!
            objs = names_objs(names, obj)
            pass
        elif orientation == 2:
            # Mirrored left to right
            w, h = img.size
            img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
            hf_box = horizontal_flip(w, h, obj)
            objs = names_objs(names, hf_box)
        elif orientation == 3:
            # Rotated 180 degrees
            w, h = img.size
            img = img.rotate(180)
            rotated_box = rote_180(w, h, obj)
            objs = names_objs(names, rotated_box)
        elif orientation == 4:
            # Mirrored top to bottom
            w, h = img.size
            img = img.rotate(180).transpose(PIL.Image.FLIP_LEFT_RIGHT)
            vf_box = vertical_flip(w, h, obj)
            objs = names_objs(names, vf_box)
        elif orientation == 5:
            # Mirrored along top-left diagonal
            w, h = img.size
            img = img.rotate(-90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
            objs = rote_90(w, h, obj)
            w, h = h, w
            hf_box = horizontal_flip(w, h, objs)
            objs = names_objs(names, hf_box)
        elif orientation == 6:
            # Rotated 90 degrees
            w, h = img.size
            img = img.rotate(-90, expand=True)
            objs = rote_90(w, h, obj)
            objs = names_objs(names, objs)
        elif orientation == 7:
            # Mirrored along top-right diagonal
            w, h = img.size
            img = img.rotate(90, expand=True).transpose(PIL.Image.FLIP_LEFT_RIGHT)
            objs = rote_270(w, h, obj)
            w, h = h, w
            hf_box = horizontal_flip(w, h, objs)
            objs = names_objs(names, hf_box)
        elif orientation == 8:
            # Rotated 270 degrees
            w, h = img.size
            img = img.rotate(90, expand=True)
            objs = rote_270(w, h, obj)
            objs = names_objs(names, objs)
    else:
        objs = names_objs(names, obj)
    return img, objs


def load_image_file(file, anno_path, mode='RGB'):
    """
    Loads an image file (.jpg, .png, etc) into a numpy array

    Defaults to returning the image data as a 3-channel array of 8-bit data. That is
    controlled by the mode parameter.

    Supported modes:
        1 (1-bit pixels, black and white, stored with one pixel per byte)
        L (8-bit pixels, black and white)
        RGB (3x8-bit pixels, true color)
        RGBA (4x8-bit pixels, true color with transparency mask)
        CMYK (4x8-bit pixels, color separation)
        YCbCr (3x8-bit pixels, color video format)
        I (32-bit signed integer pixels)
        F (32-bit floating point pixels)

    :param file: image file name or file object to load
    :param mode: format to convert the image to - 'RGB' (8-bit RGB, 3 channels), 'L' (black and white)
    :param anno_path:xml file path
    :return: image contents as numpy array and objs=[objects_name, xmin, ymin, xmax, ymax]
    """

    # Load the image with PIL
    img = PIL.Image.open(file)
    # Load the xml with PIL
    names, obj = read_xml(anno_path)
    # do the exif transpose ourselves
    img, objs_list = exif_transpose(img, names, obj)

    img = img.convert(mode)

    return np.array(img), objs_list


if __name__=='__main__':
    # picture_path = sys.argv[1]
    # annotation_path = sys.argv[2]
    picture_path = "data/demo.jpg"
    annotation_path = "data/demo.xml"
    img, objs = load_image_file(picture_path, annotation_path, mode='RGB')
    picture_save_path = "result/demo.jpg"
    anno_save_path = "result/demo.xml"
    im = PIL.Image.fromarray(img)
    im.save(picture_save_path)
    img_info = img.shape
    save_annotations_and_imgs(picture_save_path, anno_save_path, img_info, objs)
    save_path = "picture"
    save_picture_xml(picture_save_path,anno_save_path,save_path)
