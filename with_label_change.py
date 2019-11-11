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
        xmin = h-box[1]
        ymin = box[0]
        xmax = h- box[3]
        ymax = box[2]
        objs.append([xmin,ymin,xmax,ymax])
    return objs


def rote_180(w, h, boxs):
    objs = []
    for box in boxs:
        xmin = w - box[0]
        ymin = h - box[1]
        xmax = w - box[2]
        ymax = h - box[3]
        objs.append([xmin,ymin,xmax,ymax])
    return objs


def rote_270(w, h, boxs):
    result = []
    #print("boxs:",boxs)
    for box in boxs:
        xmin = box[1]
        ymin = w - box[0]
        xmax = box[3]
        ymax = w - box[2]
        result.append([xmin, ymin, xmax, ymax])
    return result


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