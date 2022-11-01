import csv
import xml.etree.ElementTree as ET
import os



myFile = open('labels.csv', 'w')
with myFile:
    writer = csv.writer(myFile, delimiter=',', lineterminator='\n')
    writer.writerows([['id','damage']])
    for fileName in os.listdir('C:/Users/Administrator/Desktop/road_damage_dataset'): 
        for className in os.listdir('C:/Users/Administrator/Desktop/road_damage_dataset'+'/'+fileName+'/Annotations'): 
            tree = ET.parse('C:/Users/Administrator/Desktop/road_damage_dataset'+'/'+fileName+'/Annotations' +'/'+className)    
            root = tree.getroot()
            damage_list =[]
            object_index = 4
            flag = 0
            for child in root:
                if (child.tag == "object" and flag == 0):
                    if (root[object_index][0].text != 'D30'):
                        flag = 1
                        damage_list.append(root[object_index][0].text)
                    object_index += 1
            #print("filename is:",root[1].text)
            add_data = [[root[1].text[:-4]]+damage_list]
            if (len(damage_list) > 0):
                writer.writerows(add_data)