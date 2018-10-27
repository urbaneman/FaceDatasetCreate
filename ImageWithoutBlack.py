import os
import shutil
import cv2
import numpy as np


def count_zero(src):
    width = src.shape[1]
    height = src.shape[0]
    area = width*height
    count_0 = 0
    if len(src.shape) == 3:
        if src.shape[2] == 3:
            for h in range(height):
                for w in range(width):
                    if src[h, w, 0] == 0 and src[h, w, 1] ==0 and src[h, w, 2]==0:
                        count_0 += 1
    else:
        for h in range(height):
            for w in range(width):
                if src[h, w] == 0:
                    count_0 += 1
    return float(count_0)/area


def remove_image_black(root_head, threshold):
    for root, dirs, files in os.walk(root_head):
        print(root)
        root_rm = root.replace("faces_2", "faces_2_rm")
        if not os.path.exists(root_rm):
            os.mkdir(root_rm)
        for file in files:
            image_path = os.path.join(root, file)
            # print(image_path)
            # image = cv2.imread(image_path)
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), -1)
            # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
            # cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
            try:
                if len(image.shape) == 0:
                    continue
            except AttributeError:
                print("open image failed!")
                continue
            # cv2.imshow("image", image)
            # cv2.waitKey(0)
            if count_zero(image) >= threshold:
                # os.remove(image_path)
                shutil.move(image_path, root_rm)


if __name__ == "__main__":
    threshold = 0.005
    root_head = r"/media/gzzn/WITAI//WIT_Face/faces_2"
    remove_image_black(root_head, threshold)

    root_head = r"/media/gzzn/WITAI//XT_Face/faces_2"
    remove_image_black(root_head, threshold)



# image_path = "F://29.jpg"
# image = cv2.imread(image_path)
# if len(image) == 0:
#     print("Open Image Failed!")
#     exit()
# cv2.imshow("image", image)
# cv2.waitKey(0)
#
# print(len(image))
#
# if count_zero(image) >= 0.01:
#     os.remove(image_path)
