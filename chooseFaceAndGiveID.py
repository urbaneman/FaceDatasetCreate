import os
import shutil
import cv2

def statisticsAndGiveID(path_original, path_save, ID_start):
    if not os.path.exists(path_original):
        print("%s not exist!"%path_original)
        return -1
    if not os.path.exists(path_save):
        os.mkdir(path_save)
    for root, dirs, files in os.walk(path_original):
        if len(files) >= 5:
            path_save_id = os.path.join(path_save, "%07d" % ID_start)
            if not os.path.exists(path_save_id):
                os.mkdir(path_save_id)
            # shutil.copytree(root, path_save_id)

            for i, file in enumerate(files):
                image_path_o = os.path.join(root, file)
                image_path = os.path.join(path_save_id, file)
                shutil.copy(image_path_o, image_path)
                image_rename = os.path.join(path_save_id, "%07d_%03d.jpg" % (ID_start, i))
                os.rename(image_path, image_rename)

            ID_start += 1
    return ID_start


if __name__ == "__main__":
    path_original = r"J:\Face_test"
    path_save = r"J:\Face_save"
    ID_start = 0
    ID_start = statisticsAndGiveID(path_original, path_save, ID_start)
    assert ID_start >= 0, "read files error"
    path_original = r""
    ID_start = (path_original, path_save, ID_start)
    assert ID_start >= 0, "read files error"


