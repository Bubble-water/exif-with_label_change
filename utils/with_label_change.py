import cv2
import numpy as np

def horizontal_flip(w, h, boxes):
    img_center = [w/2.0, h/2.0]
    results = []
    for box in boxes:
        xmin3 = 2*img_center[0] - box[2]
        ymin3 = box[1]
        xmax3 = 2*img_center[0] - box[0]
        ymax3 = box[3]
        results.append([int(xmin3), int(ymin3), int(xmax3), int(ymax3)])
    return results


def vertical_flip(w, h, boxes):
    img_center = [w/2.0, h/2.0]
    results = []
    for box in boxes:
        xmin3 = box[0]
        ymin3 = 2*img_center[1] - box[3]
        xmax3 = box[2]
        ymax3 = 2*img_center[1] - box[1]
        results.append([int(xmin3), int(ymin3), int(xmax3), int(ymax3)])
    return results


def rote_90(w, h, boxs):
    objs = []
    for box in boxs:
        result = rotate_xml(w,h, box[0], box[1], box[2], box[3], -90, scale = 1)
        objs.append(result)
    return objs


def rote_180(w, h, boxs):
    objs = []
    for box in boxs:
        result = rotate_xml(w,h, box[0], box[1], box[2], box[3], -180, scale = 1)
        objs.append(result)
    return objs


def rote_270(w, h, boxs):
    objs = []
    #print("boxs:",boxs)
    for box in boxs:
        result = rotate_xml(w,h, box[0], box[1], box[2], box[3], -270, scale = 1)
        objs.append(result)
    return objs


def read_xml(path):
    import xml.etree.ElementTree as ET
    tree = ET.parse(path)
    rootll = tree.getroot()
    objs = []
    names = []
    for obj in rootll.iter("object"):
        cls = obj.find("name").text
        xmlbox = obj.find("bndbox")
        xmin = int(xmlbox.find("xmin").text)
        ymin = int(xmlbox.find("ymin").text)
        xmax = int(xmlbox.find("xmax").text)
        ymax = int(xmlbox.find("ymax").text)
        names.append(cls)
        objs.append([xmin, ymin, xmax, ymax])
    return names, objs


def names_objs(names,boxs):
    objs = []
    for i, box in enumerate(boxs):
        objs.append([names[i], box[0], box[1], box[2], box[3]])
    return objs

def rotate_xml(w,h, xmin, ymin, xmax, ymax, angle, scale = 1):
    width = w
    height = h
    re_angle = np.deg2rad(angle)
    new_width = (abs(np.sin(re_angle) * height) + abs(np.cos(re_angle) * width)) * scale
    new_height = (abs(np.cos(re_angle) * height) + abs(np.sin(re_angle) * width)) * scale
    rotate_matrix = cv2.getRotationMatrix2D((new_width * 0.5, new_height * 0.5), angle, scale)
    rotate_move = np.dot(rotate_matrix, np.array([(new_width - width) * 0.5, (new_height - height) * 0.5, 0]))
    rotate_matrix[0, 2] += rotate_move[0]
    rotate_matrix[1, 2] += rotate_move[1]
    # 获取原始矩形的四个中点，然后将这四个点转换到旋转后的坐标系下
    point1 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymin, 1]))
    point2 = np.dot(rotate_matrix, np.array([xmax, (ymin + ymax) / 2, 1]))
    point3 = np.dot(rotate_matrix, np.array([(xmin + xmax) / 2, ymax, 1]))
    point4 = np.dot(rotate_matrix, np.array([xmin, (ymin + ymax) / 2, 1]))
    concat = np.vstack((point1, point2, point3, point4))  # 合并np.array
    # 改变array类型
    concat = concat.astype(np.int32)
    rx, ry, rw, rh = cv2.boundingRect(concat)#rx,ry,为新的外接框左上角坐标，rw为框宽度，rh为高度
    new_xmin = rx
    new_ymin = ry
    new_xmax = rx + rw
    new_ymax = ry + rh
    result = [new_xmin,new_ymin,new_xmax,new_ymax]
    return result