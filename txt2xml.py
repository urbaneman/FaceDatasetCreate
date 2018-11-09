# -*- coding: utf-8 -*-
"""
根据txt生成xml文件
@author: bai
"""
import argparse
import os, cv2

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class gen_xml():
    def __init__(self, root='annotation'):
        '''
        最多3层
        '''
        self.root_a = ET.Element(root)

        self.sub_root_a = None
        self.sub_sub_root_a = None

    def set_sub_node(self, last, sub_node, val):  # last = root','sub_root' or 'sub_sub_root'
        if last == 'root':
            b = ET.SubElement(self.root_a, sub_node)
            b.text = val
        elif last == 'sub_root':
            b = ET.SubElement(self.sub_root_a, sub_node)
            b.text = val
        elif last == 'sub_sub_root':
            b = ET.SubElement(self.sub_sub_root_a, sub_node)
            b.text = val

    def set_sub_root(self, last, sub_root):  # last = root','sub_root'
        if last == 'root':
            self.sub_root_a = ET.SubElement(self.root_a, sub_root)
        elif last == 'sub_root':
            self.sub_sub_root_a = ET.SubElement(self.sub_root_a, sub_root)

    def out(self, filename):
        fp = open(filename, 'wb')
        tree = ET.ElementTree(self.root_a)
        tree.write(fp)
        fp.close()


def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='txt2xml demo')
    parser.add_argument('--JPEGImages', '-J', dest='image_path', type=str, help='JPEGImages path to read',
                        default='None')
    parser.add_argument('--txt', '-T', dest='txt_path', help='txt path to read',
                        default='None')
    parser.add_argument('--Annotations', '-A', dest='xml_path', help='xml path to save',
                        default='None')
    args = parser.parse_args()

    return args


def main(args):
    list_txt = os.listdir(args.txt_path)
    #    list_need=['filename','size','name','part']
    #    list_sub_need=['width','height','depth','xmin','ymin','xmax','ymax']
    if len(list_txt) == 0:
        return

    for txt_name in list_txt:
        txt = open(os.path.join(args.txt_path, txt_name), 'r')
        image_name = os.path.join(args.image_path, txt_name.replace('.txt', '.jpg'))
        img = cv2.imread(image_name)
        height = img.shape[0]
        width = img.shape[1]
        depth = img.shape[2]

        my_xml = gen_xml('annotation')
        my_xml.set_sub_node('root', 'filename', '%s' % image_name)
        my_xml.set_sub_root('root', 'size')
        my_xml.set_sub_node('sub_root', '%s' % 'height', '%s' % height)
        my_xml.set_sub_node('sub_root', '%s' % 'width', '%s' % width)
        my_xml.set_sub_node('sub_root', '%s' % 'depth', '%s' % depth)

        lines = txt.readlines()
        for line in lines:
            class_name_coor = line.split(' ')
            #            print(line,'len:',len(class_name_coor))
            if len(class_name_coor) == 5:
                my_xml.set_sub_root('root', 'object')
                my_xml.set_sub_node('sub_root', 'name', class_name_coor[0])
                my_xml.set_sub_root('sub_root', 'bndbox')
                my_xml.set_sub_node('sub_sub_root', '%s' % 'xmin', '%s' % class_name_coor[1])
                my_xml.set_sub_node('sub_sub_root', '%s' % 'ymin', '%s' % class_name_coor[2])
                my_xml.set_sub_node('sub_sub_root', '%s' % 'xmax', '%s' % class_name_coor[3])
                my_xml.set_sub_node('sub_sub_root', '%s' % 'ymax', '%s' % class_name_coor[4])

        if os.path.exists(image_name):
            my_xml.out(os.path.join(args.xml_path, txt_name.replace('.txt', '.xml')))


if __name__ == '__main__':
    args = parse_args()
    if args.image_path == 'None' or args.xml_path == 'None':
        exit(0)
    main(args)
    print('end')