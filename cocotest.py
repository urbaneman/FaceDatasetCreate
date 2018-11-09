import matplotlib
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
from PIL import Image
import pylab
import cv2
pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir=r'J:/Dataset/COCO/COCO2017'
imageDir = 'train2017'
dataType='val2017'
annFile='{}/annotations_tiny/instances_{}.json'.format(dataDir,dataType)

#maps = [0,5,2,15,9,40,6,3,16,57,20,61,17,18,4,1,59,19,58,7,63]
#maps = [0,5,2,16,9,44,6,3,17,62,21,67,18,19,4,1,64,20,63,7,72]

# initialize COCO api for instance annotations
coco=COCO(annFile)

# display COCO categories and supercategories
cats = coco.loadCats(coco.getCatIds())
nms=[cat['name'] for cat in cats]
# for i, name in enumerate(nms):
#     print("%d： %s"%(i+1, name))
print('COCO categories: \n{}\n'.format(' '.join(nms)))

nms = set([cat['supercategory'] for cat in cats])
print('COCO supercategories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['person','dog','couch'])
print(catIds)
imgIds = coco.getImgIds(catIds=catIds)
print(imgIds)
for imgid in imgIds:
    # imgIds = coco.getImgIds(imgIds=imgIds[0])
    img = coco.loadImgs(imgid)[0]

    # load and display image
    # I = io.imread('%s/images/%s/%s'%(dataDir, dataType, img['file_name']))
    # # use url to load image
    # # I = io.imread(img['coco_url'])
    # plt.figure("image")
    # plt.axis('off')
    # plt.imshow(I)
    # plt.show()
    image_mp = Image.open('%s/images/%s/%s'%(dataDir, dataType, img['file_name']))
    plt.figure("Image")
    plt.imshow(image_mp)
    plt.show()
    # image = cv2.imread('%s/images/%s/%s'%(dataDir,dataType,img['file_name']))
    # cv2.imshow("image", image)
    # cv2.waitKey(0)


