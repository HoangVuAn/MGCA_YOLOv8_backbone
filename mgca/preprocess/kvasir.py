import numpy as np
import pandas as pd
from mgca.constants import *
import pickle
import cv2

def masks_to_boxes(mask_path):
    boxes = []

    mask_image = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    _, mask_image = cv2.threshold(mask_image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area_threshold = 4
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area_threshold:
            xmin, ymin, w, h = cv2.boundingRect(contour)
            boxes.append([xmin, ymin, w, h])

    return boxes
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
            bboxs_list.append(np.zeros((1, 4)))
        else:
            bboxs = annotation_to_bbox(row.annotation)
            bboxs_list.append(bboxs)

    filenames = np.array(filenames)
    bboxs_list = np.array(bboxs_list)
    with open(pkl_path, "wb") as f:
        pickle.dump([filenames, bboxs_list], f)
def main():
    #create bbox from mask
    
    list_path_masks = [KVASIR_TRAIN_MASK_PATH, KVASIR_VAL_MASK_PATH, KVASIR_TEST_MASK_PATH]
    list_csv = [KVASIR_ORIGINAL_TRAIN_CSV, KVASIR_ORIGINAL_VAL_CSV, KVASIR_ORIGINAL_TEST_CSV]
    list_pkl = [KVASIR_TRAIN_PKL, KVASIR_VAL_PKL, KVASIR_TEST_PKL]
    for path, csv, pkl in zip(list_path_masks,list_csv, list_pkl):
        bboxs_list = []
        img_path_list = []
        for mask_path in os.listdir(path):
            img_path_list.append(mask_path)
            boxes = masks_to_boxes(os.path.join(path, mask_path))
            bboxs_list.append(boxes)

        df = pd.DataFrame({'image_name': img_path_list, 'annotation': bboxs_list})
        # print(df)
        df.to_csv(csv, index=False)
        save_pkl(df, pkl)

if __name__ =="__main__":
    main()
