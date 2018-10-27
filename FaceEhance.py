import os
import shutil
import cv2
import random
import numpy as np

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

def gamma_trans(img, gamma):

    (r,g,b) = cv2.split(img)
    gamma_table = [np.power(x/255.0, gamma)*255.0 for x in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)

    r_g = cv2.LUT(r,gamma_table)
    g_g = cv2.LUT(g,gamma_table)
    b_g = cv2.LUT(b,gamma_table)
    # cv2.imshow("image_gamma_g", g_g)
    return cv2.merge([r_g, g_g, b_g])

def DataEnhance(root_path, root_path_enhance, min_num_1):
    if not os.path.exists(root_path):
        print("%s not exist!" % root_path)
        return -1
    if not os.path.exists(root_path.replace("Face_save", root_path_enhance)):
        os.mkdir(root_path.replace("Face_save", root_path_enhance))
    count_dir = 0
    for root, dirs, files in os.walk(root_path):
        count_dir +=1
        if count_dir%500 == 0:
            print(root)
        dir_enhance = root.replace("Face_save", root_path_enhance)
        if not os.path.exists(dir_enhance):
            os.mkdir(dir_enhance)
        files_num = len(files)
        if files_num == 0:
            continue
        for file in files:
            face_path = os.path.join(root, file)
            shutil.copy(face_path, dir_enhance)
        if files_num >= min_num_1:
            continue
        elif files_num >= int(min_num_1/2):
            num_lack = min_num_1 - files_num
            random.shuffle(files)
            files_enhance = files[:num_lack]
            for i, file in enumerate(files_enhance):
                face = cv2.imread(os.path.join(root, file))
                face_flip = cv2.flip(face, 1)
                face_enhance_name = os.path.join(dir_enhance, "%s_%03d.jpg" % (file[:7], files_num + i))
                cv2.imwrite(face_enhance_name, face_flip)
        elif files_num >= int(min_num_1/6):
            i = files_num
            files_enhance = [] + files
            for file in files:
                face = cv2.imread(os.path.join(root, file))
                face_flip = cv2.flip(face, 1)
                face_enhance_name = "%s_%03d.jpg" % (file[:7], i)
                face_enhance_path = os.path.join(dir_enhance, face_enhance_name)
                cv2.imwrite(face_enhance_path, face_flip)
                files_enhance.append(face_enhance_name)
                i += 1
            files_enhance += files_enhance
            num_lack = min_num_1 - files_num*2
            random.shuffle(files_enhance)
            for file in files_enhance[:num_lack]:
                face = cv2.imread(os.path.join(dir_enhance, file))
                if random.randint(0, 1):
                    face_gamma = gamma_trans(face, random.randint(60, 100)/100)
                    face_enhance_name = os.path.join(dir_enhance, "%s_%03d.jpg" % (file[:7], i))
                    cv2.imwrite(face_enhance_name, face_gamma)
                else:
                    face_gamma = gamma_trans(face, 1/(random.randint(60, 100)/100))
                    face_enhance_name = os.path.join(dir_enhance, "%s_%03d.jpg" % (file[:7], i))
                    cv2.imwrite(face_enhance_name, face_gamma)
                i += 1
        else:
            i = files_num
            files_enhance = [] + files
            for file in files:
                face = cv2.imread(os.path.join(root, file))
                face_flip = cv2.flip(face, 1)
                face_enhance_name = "%s_%03d.jpg" % (file[:7], i)
                face_enhance_path = os.path.join(dir_enhance, face_enhance_name)
                cv2.imwrite(face_enhance_path, face_flip)
                files_enhance.append(face_enhance_name)
                i += 1
            num_lack = min_num_1 - files_num * 2
            for j in range(num_lack):
                file_ = files_enhance[random.randint(0, files_num*2)]
                face = cv2.imread(os.path.join(dir_enhance, file_))
                if random.randint(0, 1):
                    face_gamma = gamma_trans(face, random.randint(60, 100) / 100)
                    face_enhance_name = os.path.join(dir_enhance, "%s_%03d.jpg" % (file[:7], i))
                    cv2.imwrite(face_enhance_name, face_gamma)
                else:
                    face_gamma = gamma_trans(face, 1/(random.randint(60, 100)/100))
                    face_enhance_name = os.path.join(dir_enhance, "%s_%03d.jpg" % (file[:7], i))
                    cv2.imwrite(face_enhance_name, face_gamma)
                i += 1
    return 1





if __name__ == "__main__":
    # path_original = r"J:\Face_test"
    # path_save = r"J:\Face_save"
    # ID_start = 0
    # ID_start = statisticsAndGiveID(path_original, path_save, ID_start)
    # assert ID_start >= 0, "read files error"
    # path_original = r""
    # ID_start = (path_original, path_save, ID_start)
    # assert ID_start >= 0, "read files error"
    path_original = r"/media/gzzn/WITAI/Face_save"
    path_save = r"Face_enhance"
    DataEnhance(path_original, path_save, 30)
