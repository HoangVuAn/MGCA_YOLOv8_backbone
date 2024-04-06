import ipdb
import math
import numpy as np
import pandas as pd
from mgca.constants import *
import pickle
from shapely.geometry import LineString
from shapely.algorithms.polylabel import polylabel
from shapely.ops import unary_union
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree as ET


np.random.seed(0)


OBJECT_SEP = ';'
ANNOTATION_SEP = ' '


def rectangle_box(anno):
    x = []
    y = []

    anno = anno[2:]
    anno = anno.split(ANNOTATION_SEP)
    for i in range(len(anno)):
        if i % 2 == 0:
            x.append(int(anno[i]))
        else:
            y.append(int(anno[i]))

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    w = xmax - xmin
    h = ymax - ymin
    box = [xmin, ymin, w, h]
    return box


# source: https://github.com/xuyuan/xsd/blob/master/data/object_cxr_to_coco.ipynb
def annotation_to_bbox(annotation):
    bbox = []
    if not annotation:
        return bbox

    annotation_list = annotation
    for anno in annotation_list:
        # box = rectangle_box(anno)
        bbox.append(anno)
    return bbox


def save_pkl(df, pkl_path):
    filenames, bboxs_list = [], []
    for row in df.itertuples():
        filenames.append(row.image_name)
        if row.annotation != row.annotation:
            bboxs_list.append(np.zeros((1, 5)))
        else:
            bboxs = annotation_to_bbox(row.annotation)
            bboxs_list.append(bboxs)

    filenames = np.array(filenames)
    bboxs_list = np.array(bboxs_list)
    with open(pkl_path, "wb") as f:
        pickle.dump([filenames, bboxs_list], f)

def xml_object_to_boxes(root):
    labels = ["Viem thuc quan", "Ung thu da day", "Viem da day Hp duong", "Loet hanh ta trang", "Viem da day Hp am", "Ung thu thuc quan"]

    

    boxes = [[int(labels.index(obj.find('name').text)),
                                  int(obj.find('bndbox').find('xmin').text), 
                                  int(obj.find('bndbox').find('ymin').text), 
                                  int(obj.find('bndbox').find('xmax').text) - int(obj.find('bndbox').find('xmin').text),
                                  int(obj.find('bndbox').find('ymax').text) - int(obj.find('bndbox').find('ymin').text)
                                ] for obj in root.findall('object')]
    return boxes

def xml_to_csv(list_csv, list_path_xml, list_pkl):
    for csv, path_xml,pkl in zip(list_csv, list_path_xml, list_pkl):
        bboxs_list = []
        img_path_list = []
        for path_xml_file in os.listdir(path_xml):
            tree = ET.parse(os.path.join(path_xml, path_xml_file))
            root = tree.getroot()

            img_path_list.append(os.path.splitext(os.path.basename(path_xml_file))[0] + ".jpg")
            bboxs_list.append(xml_object_to_boxes(root))

        df = pd.DataFrame({'image_name': img_path_list, 'annotation': bboxs_list})
        df.to_csv(csv, index=False)
        save_pkl(df, pkl)


    return df

def main():
    list_path = [ENDODANHHUY_TRAIN_IMG_PATH, ENDODANHHUY_VAL_IMG_PATH, ENDODANHHUY_TEST_IMG_PATH]
    list_csv = [ENDODANHHUY_ORIGINAL_TRAIN_CSV, ENDODANHHUY_ORIGINAL_VAL_CSV, ENDODANHHUY_ORIGINAL_TEST_CSV]
    list_pkl = [ENDODANHHUY_TRAIN_PKL, KENDODANHHUY_VAL_PKL, ENDODANHHUY_TEST_PKL]
    list_path_xml = [ENDODANHHUY_TRAIN_XML_IMG_PATH, ENDODANHHUY_VAL_XML_IMG_PATH, ENDODANHHUY_TEST_XML_IMG_PATH]

    obj_data = xml_to_csv(list_csv, list_path_xml, list_pkl)
    print("hi")


if __name__ == "__main__":
    main()