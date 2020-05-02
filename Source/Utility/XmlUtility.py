import xml.etree.ElementTree as ET
import os


def GetAttribute(path, t, att):
    myTree = os.path.abspath(path)
    myTree = ET.parse(myTree)
    myRoot = myTree.getroot()

    for i in myRoot:
        if i.tag == t:
            return i.attrib[att]
        else:
            for j in i:
                if j.tag == t:
                    return j.attrib[att]
                else:
                    pass


# print(GetAttribute('../../res/Config/actor.xml', 'Sprite', 'Alpha'))