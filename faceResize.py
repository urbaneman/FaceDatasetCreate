import os
import cv2

root_path = r"/media/gzzn/WITAI/Face_save"
root_face_resize = r"Face_resize"
count = 0
for root, dirs, files in os.walk(root_path):
    face_resize_dir = root.replace("Face_save", root_face_resize)
    if not os.path.exists(face_resize_dir):
        os.mkdir(face_resize_dir)
    for file in files:
        face_resize_path = os.path.join(face_resize_dir, file)
        face_path = os.path.join(root, file)
        face = cv2.imread(face_path)
        try:
            if len(face.shape) != 3:
                continue
        except AttributeError:
            print("open error: %s"%face_path)
            continue
        face_resize = cv2.resize(face, (112, 112))
        # cv2.imshow("face", face)
        # cv2.imshow("face_resize", face_resize)
        # cv2.waitKey(0)
        cv2.imwrite(face_resize_path, face_resize)
        count += 1
        if count %1000 == 0:
            print("face count: %d" % count)
