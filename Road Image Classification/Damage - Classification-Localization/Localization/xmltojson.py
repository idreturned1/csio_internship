import json
import xml.etree.ElementTree as ET
import os

category_dict = {"D00": 1, "D01": 2, "D10": 3, "D11": 4, "D20": 5, "D40": 6, "D43": 7, "D44": 8, "D30": -1}
image_list = []
temp_list = []
annotation_list = []
category_list = [{"id":1,"name":"D00"},{"id":2,"name":"D01"},{"id":3,"name":"D10"},{"id":4,"name":"D11"},
                 {"id":5,"name":"D20"},{"id":6,"name":"D40"},{"id":7,"name":"D43"},{"id":8,"name":"D44"}]

for dirName in os.listdir('C:/Users/Administrator/Desktop/road_damage_dataset'): 
    for fileName in os.listdir('C:/Users/Administrator/Desktop/road_damage_dataset'+'/'+dirName+'/Annotations'): 
        tree = ET.parse('C:/Users/Administrator/Desktop/road_damage_dataset'+'/'+dirName+'/Annotations'+'/'+fileName)    
        root = tree.getroot()
        
        image_dict = {}
        
        image_dict["file_name"] = root[1].text
        image_dict["height"] = int(root[2][0].text)
        image_dict["width"] = int(root[2][1].text)
        image_dict["id"] = int(root[1].text[-9:-4])
        
        image_list.append(image_dict)
        print("Added Image",image_dict)
        annotation_id = 1
        object_index = 4
        
        
        for child in root:
            if (child.tag == "object"):
                count = 0
                for temp in root[object_index]:
                    if (temp.tag == 'bndbox'):
                        bbox_index = count
                    count += 1
                    
                annotation_dict = {}
                annotation_dict["category_id"] = category_dict[root[object_index][0].text]
                if annotation_dict["category_id"] == -1:
                    continue
    
                annotation_dict["image_id"] = int(root[1].text[-9:-4])
                annotation_dict["bbox"] = [int(root[object_index][bbox_index][0].text),int(root[object_index][bbox_index][3].text),
                                int(root[object_index][bbox_index][3].text)-int(root[object_index][bbox_index][1].text),
                                int(root[object_index][bbox_index][2].text)-int(root[object_index][bbox_index][0].text)]
                
                annotation_dict["id"] = annotation_id
                annotation_id += 1
                object_index += 1
                annotation_list.append(annotation_dict)
                print("Added Annotation",annotation_dict)

data = {"images": image_list, "type":"instances", "annotations": annotation_list, "categories": category_list}
print(data)


with open('JSONData.json', 'w') as f:
     json.dump(data, f)






