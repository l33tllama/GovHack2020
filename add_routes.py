# This script is used for fixing .osm files to work with OSRM by adding extra tags to denote passable roads
import xml.etree.ElementTree as ET
tree = ET.parse("test2.osm")
root = tree.getroot()

replaced_num = 0
for child in root:
    if child.tag == "way":
        new_el = ET.Element("tag")
        new_el.attrib = {"k": "route", "v" : "road"}
        new_el2 = ET.Element("tag")
        new_el2.attrib = {"k": "highway", "v" : "residential"}
        child.append(new_el)
        child.append(new_el2)
        replaced_num += 1

print("Replaced " + str(replaced_num))
tree.write("test3.osm")
            


