import xml.etree.ElementTree as ET
import pandas as pd
import os

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    labels = ["Viem thuc quan", "Ung thu da day", "Viem da day Hp duong", "Loet hanh ta trang", "Viem da day Hp am"]
    data = []
    for obj in root.findall('object'):
        obj_data = {}
        obj_data['image_name'] = os.path.splitext(os.path.basename(xml_file))[0] + ".jpg"
        obj_data['object_name'] = obj.find('name').text
        brea
        
    obj_data['annotation'] = [[labels.index(obj.find('name').text),
                                  obj.find('bndbox').find('xmin').text, 
                                  obj.find('bndbox').find('ymin').text, 
                                  obj.find('bndbox').find('ymin').text,
                                  obj.find('bndbox').find('ymax').text ] for obj in root.findall('object')]
        # data.append(obj_data)
    
    return pd.DataFrame(obj_data)

xml_file = 'mgca/data/EndoDanhHuy/val_xml/000000018461.xml'
df = parse_xml(xml_file)
print(df)
