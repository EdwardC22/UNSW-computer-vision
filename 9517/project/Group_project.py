import cv2
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os
import random
from math import ceil
from math import sqrt


def in_rec(out_side, in_side):
    if out_side[0] > in_side[0]:
        if out_side[1] > in_side[1]:
            if out_side[0] + out_side[2] < in_side[0] + in_side[2]:
                if out_side[1] + out_side[3] < in_side[1] + in_side[3]:
                    return True
    return False


def draw_rec_image(point, add_size, image, color):
    p_x = point[0]
    p_y = point[1] + add_size
    p_x_plus = point[2] + p_x
    p_y_plus = p_y + point[3]
    cv2.rectangle(image, (p_x, p_y), (p_x_plus, p_y_plus), color, 2)


text_para = {
    "fontFace": cv2.FONT_HERSHEY_DUPLEX,
    "fontScale": 1,
    "color": (255, 255, 255),
    "thickness": 2,
    "lineType": cv2.LINE_AA,
    "cord": (0, 30)
}


def hog_dect(gray_image):
    gray_image_dec = hog_des.detectMultiScale(gray_image, winStride=(4, 4), padding=(4, 4), scale=1.05)[0]
    cur_find = []
    index_out = 0
    index_in = 0
    length_found = len(gray_image_dec)
    while index_out < length_found:
        flag = 0
        while index_in < length_found:
            if index_in != index_out:
                if in_rec(gray_image_dec[index_out], gray_image_dec[index_in]):
                    flag = 1
            index_in += 1
        if flag == 0:
            cur_find.append(gray_image_dec[index_out])
        index_out += 1
        index_in = 0
    print(len(cur_find))


# step1   生成视频
def resize(img_array, align_mode):
    _height = len(img_array[0])
    _width = len(img_array[0][0])
    for i in range(1, len(img_array)):
        img0 = img_array[i]
        height = len(img0)
        width = len(img0[0])
        if align_mode == 'smallest':
            if height < _height:
                _height = height
            if width < _width:
                _width = width
        else:
            if height > _height:
                _height = height
            if width > _width:
                _width = width

    for i in range(0, len(img_array)):
        img1 = cv2.resize(img_array[i], (_width, _height), interpolation=cv2.INTER_CUBIC)
        img_array[i] = img1

    return img_array, (_width, _height)


def images_to_video(path):
    img_array = []

    for f1 in os.listdir(path):
        filename = os.path.join(path, f1)
        img0 = cv2.imread(filename)
        if img0 is None:
            print(filename + " is error!")
            continue
        img_array.append(img0)

    img_array, size = resize(img_array, 'largest')
    fps = 30
    out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


# step2   跳出弹窗
# step3   让用户可以画框
# step4   获得用户画框的数据

# 鼠标操作函数
def OnMouseAction(event, x, y, flags, param):
    global img, position1, position2
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        position1 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        cv2.rectangle(img2, position1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:
        position2 = (x, y)
        cv2.rectangle(img2, position1, position2, (0, 0, 255), 1, 4)
        cv2.imshow('image', img2)

        if position1 != position2:
            min_x = min(position1[0], position2[0])
            min_y = min(position1[1], position2[1])
            width = abs(position1[0] - position2[0])
            height = abs(position1[1] - position2[1])
            img2 = img2[min_y:min_y + height, min_x:min_x + width]
            img2_gray = img2.copy()
            img2_gray = cv2.cvtColor(img2_gray, cv2.COLOR_BGR2GRAY)
            hog_dect(img2_gray)
            cv2.namedWindow('cut')
            cv2.imshow('cut', img2)


def video_cap(cap):
    global img, position1, position2
    print('press any key to start the video')
    print('press s to pause the video, q to quit the process')
    print('you can stop the video before you draw the rectangular region')
    cv2.namedWindow('image')
    cv2.waitKey(0)
    cv2.setMouseCallback('image', OnMouseAction)
    position1 = None
    position2 = None
    img = None
    while cap.isOpened():
        ret, img = cap.read()
        if ret:
            height, width = img.shape[:2]

            cv2.imshow('image', img)
            k1 = cv2.waitKey(1)
            if k1 == ord('q'):
                break

            if k1 == ord('s'):
                print('pause now, you can draw the rectangular region, press any key to continue')
                print('to quit the video, you should continue the video first ')
                cv2.waitKey(0)

        else:
            cap.release()
            cv2.destroyAllWindows()
            break

# get the image address
image_address = "./step_images/test/STEP-ICCV21-01/"
# then, get the file number
files = sorted(os.listdir(image_address))
number_of_files = len(files)
# define the crop_size
crop_size = 400
# define a hogdescriptor
hog_des = cv2.HOGDescriptor()
hog_des.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# record the central point and the person position
task_1_1_dict = defaultdict(list)
group_out_dict = defaultdict(dict)
cur_index = 0
for index in range(1, number_of_files + 1):
    distinct = set()
    group_index = 0
    group_out_index = 0
    task_3_3_index = 0
    task_3_3_dict = defaultdict(list)
    group_dict = defaultdict(list)
    cur_address = image_address + files[index - 1]
    # then, get the image of rgb and image of gray
    cur_image_rgb = cv2.imread(cur_address)
    cur_image_gray = cv2.imread(cur_address, 0)
    # then, since the upper image is useless for detection, we first resize it
    cur_image_gray_resize = cur_image_gray[crop_size:1080, 0:1920]
    people_cur_list = hog_dect(cur_image_gray_resize)
    people_list = []
    # then, we will also
    for people in people_cur_list:
        if people[0] < 400 or people[1] > 600:
            continue
        else:
            people_list.append(people)
    for point in people_list:
        # draw_rec_image(point, crop_size, cur_image_rgb, (0,255,0))
        central_point = (ceil(point[2] / 2 + point[0]), ceil((point[3]) / 2 + point[1] + crop_size))
        # cv2.circle(cur_image_rgb, central_point, 1, (0, 0,255), 1)
        # task_1_1.append(cur_image_rgb)
        color = list(random.sample(range(0, 255), 3))
        if index - 1 == 0:
            task_1_1_dict[str(cur_index)].append([central_point])
            task_1_1_dict[str(cur_index)].append(color)
            task_1_1_dict[str(cur_index)].append(point)
            task_1_1_dict[str(cur_index)].append([index])
            draw_rec_image(point, crop_size, cur_image_rgb, task_1_1_dict[str(cur_index)][1])
            cv2.circle(cur_image_rgb, central_point, 2, task_1_1_dict[str(cur_index)][1], 1)
            cur_index += 1

        else:
            for key in task_1_1_dict.keys():
                x_dis = central_point[0] - task_1_1_dict[key][0][-1][0]
                y_dis = central_point[1] - task_1_1_dict[key][0][-1][1]
                x_dis_abs = abs(x_dis)
                y_dis_abs = abs(y_dis)
                distance = sqrt(x_dis_abs ** 2 + y_dis_abs ** 2)

                if distance < 10:
                    # same person
                    draw_rec_image(point, crop_size, cur_image_rgb, task_1_1_dict[key][1])
                    cv2.circle(cur_image_rgb, central_point, 2, task_1_1_dict[key][1], 1)
                    # cv2.line(cur_image_rgb, task_1_1_dict[key][0], central_point, task_1_1_dict[key][1], 2)
                    # update central point and point
                    task_1_1_dict[key][0].append(central_point)
                    task_1_1_dict[key][2] = point
                    task_1_1_dict[key][3].append(index)
                    if central_point[0] <= 150:
                        if x_dis < 0:
                            task_3_3_dict[str(task_3_3_index)].append(central_point)
                            task_3_3_dict[str(task_3_3_index)].append("leave")
                        else:
                            task_3_3_dict[str(task_3_3_index)].append(central_point)
                            task_3_3_dict[str(task_3_3_index)].append("enter")
                        task_3_3_index += 1
                    elif central_point[0] >= 1770:
                        if x_dis < 0:
                            task_3_3_dict[str(task_3_3_index)].append(central_point)
                            task_3_3_dict[str(task_3_3_index)].append("enter")
                        else:
                            task_3_3_dict[str(task_3_3_index)].append(central_point)
                            task_3_3_dict[str(task_3_3_index)].append("leave")
                        task_3_3_index += 1
                    break

            else:
                task_1_1_dict[str(cur_index)].append([central_point])
                task_1_1_dict[str(cur_index)].append(color)
                task_1_1_dict[str(cur_index)].append(point)
                task_1_1_dict[str(cur_index)].append([index])
                draw_rec_image(point, crop_size, cur_image_rgb, task_1_1_dict[str(cur_index)][1])
                cv2.circle(cur_image_rgb, central_point, 2, task_1_1_dict[str(cur_index)][1], 1)
                cur_index += 1

    cur_people_count = len(people_list)
    cur_text = f"Person Number:{cur_people_count}"
    cv2.putText(img=cur_image_rgb, text=cur_text, org=text_para["cord"], fontFace=text_para["fontFace"],
                fontScale=text_para["fontScale"], color=text_para["color"], thickness=text_para["thickness"],
                lineType=text_para["lineType"])
    # draw lines
    for key in task_1_1_dict.keys():
        if len(task_1_1_dict[key][0]) > 1 and task_1_1_dict[key][3][-1] == index:
            prev = task_1_1_dict[key][0][0]
            for index_cur in range(1, len(task_1_1_dict[key][0])):
                cv2.line(cur_image_rgb, prev, task_1_1_dict[key][0][index_cur], task_1_1_dict[key][1], 2)
                prev = task_1_1_dict[key][0][index_cur]
    # get group information
    for key_out in task_1_1_dict.keys():
        for key_in in task_1_1_dict.keys():
            if key_in == key_out:
                continue
            else:
                x_dis = abs(task_1_1_dict[key_out][0][-1][0] - task_1_1_dict[key_in][0][-1][0])
                y_dis = abs(task_1_1_dict[key_out][0][-1][1] - task_1_1_dict[key_in][0][-1][1])
                distance = ceil(sqrt(x_dis ** 2 + y_dis ** 2))
                cur_item = []
                if distance <= 80:
                    if (task_1_1_dict[key_out][0][-1] not in distinct and task_1_1_dict[key_in][0][
                        -1] not in distinct) and task_1_1_dict[key_out][3][-1] == task_1_1_dict[key_in][3][-1] and \
                            task_1_1_dict[key_out][3][-1] == index and task_1_1_dict[key_in][3][-1] == index:
                        if len(task_1_1_dict[key_out][3]) >= 2 and len(task_1_1_dict[key_in][3]) >= 2:
                            if task_1_1_dict[key_out][3][-2] == task_1_1_dict[key_in][3][-2]:
                                group_dict[str(group_index)].append(True)
                                cur_item.append(task_1_1_dict[key_out][0][-1])
                                cur_item.append(task_1_1_dict[key_in][0][-1])
                                group_dict[str(group_index)].append(cur_item)
                        else:
                            group_dict[str(group_index)].append(False)
                            cur_item.append(task_1_1_dict[key_out][0][-1])
                            cur_item.append(task_1_1_dict[key_in][0][-1])
                            group_dict[str(group_index)].append(cur_item)
                        distinct.add(task_1_1_dict[key_out][0][-1])
                        distinct.add(task_1_1_dict[key_in][0][-1])
                        group_index += 1
                    elif (task_1_1_dict[key_out][0][-1] not in distinct and task_1_1_dict[key_in][0][
                        -1] not in distinct) and task_1_1_dict[key_out][3][-1] == task_1_1_dict[key_in][3][-1] and \
                            task_1_1_dict[key_out][3][-1] == index and task_1_1_dict[key_in][3][-1] == index:
                        for key in group_dict.keys():
                            if task_1_1_dict[key_out][0][-1] in group_dict[key][1]:
                                group_dict[key][1].add(task_1_1_dict[key_in][0][-1])
                            else:
                                group_dict[key][1].add(task_1_1_dict[key_out][0][-1])
                            if len(task_1_1_dict[key_out][3]) >= 2 and len(task_1_1_dict[key_in][3]) >= 2:
                                if task_1_1_dict[key_out][3][-2] == task_1_1_dict[key_in][3][-2]:
                                    # group
                                    group_dict[key][1] = True
                        distinct.add(task_1_1_dict[key_out][0][-1])
                        distinct.add(task_1_1_dict[key_in][0][-1])
                        group_index += 1

    if index - 1 == 0:
        group_out_dict['0'] = group_dict
    elif index - 1 == 1:
        group_out_dict['1'] = group_dict
    else:
        group_out_dict['0'] = group_out_dict['1']
        group_out_dict['1'] = group_dict
        for key in group_out_dict['0'].keys():
            flag = 0
            for key_ in group_out_dict['1'].keys():
                # make sure that they are they are not the same pair
                x_abs = abs(group_out_dict['0'][key][1][1][0] - group_out_dict['1'][key_][1][1][0])
                y_abs = abs(group_out_dict['0'][key][1][1][1] - group_out_dict['1'][key_][1][1][1])
                dis_tan = sqrt(x_abs ** 2 + y_abs ** 2)
                if dis_tan < 10:
                    flag = 1
            if flag == 0:
                cur_text = f'{str(key)}-d'
                cv2.putText(img=cur_image_rgb, text=cur_text,
                            org=(group_out_dict['0'][key][1][1][0], group_out_dict['0'][key][1][1][1] - 20),
                            fontFace=text_para["fontFace"],
                            fontScale=text_para["fontScale"], color=(0, 255, 0),
                            thickness=text_para["thickness"], lineType=text_para["lineType"])
                cv2.putText(img=cur_image_rgb, text=cur_text,
                            org=(group_out_dict['0'][key][1][0][0], group_out_dict['0'][key][1][0][1] - 20),
                            fontFace=text_para["fontFace"],
                            fontScale=text_para["fontScale"], color=(0, 255, 0),
                            thickness=text_para["thickness"], lineType=text_para["lineType"])
    # get the group number information and also finish the 3.2 task
    group_person_number = 0
    for key in group_dict.keys():
        group_person_number += len(group_dict[key][1])
        if group_dict[key][0]:
            for cord in group_dict[key][1]:
                cur_text = f"{str(key)}-f"
                cv2.putText(img=cur_image_rgb, text=cur_text, org=(cord[0], cord[1] - 20),
                            fontFace=text_para["fontFace"],
                            fontScale=text_para["fontScale"], color=(0, 255, 0),
                            thickness=text_para["thickness"], lineType=text_para["lineType"])

    # finish task 3.3
    for key in task_3_3_dict.keys():
        cur_text = task_3_3_dict[key][1]
        cv2.putText(img=cur_image_rgb, text=cur_text, org=(task_3_3_dict[key][0][0], task_3_3_dict[key][0][1] - 20),
                    fontFace=text_para["fontFace"],
                    fontScale=text_para["fontScale"], color=(255, 0, 0),
                    thickness=text_para["thickness"], lineType=text_para["lineType"])
    individual_person_number = cur_people_count - group_person_number
    # write the task 2.1/3.1 in the format
    cur_text = f"{individual_person_number} people walk alone"
    cv2.putText(img=cur_image_rgb, text=cur_text, org=(0, 60), fontFace=text_para["fontFace"],
                fontScale=text_para["fontScale"], color=text_para["color"], thickness=text_para["thickness"],
                lineType=text_para["lineType"])
    cur_text = f"{group_person_number} people walk in groups"
    cv2.putText(img=cur_image_rgb, text=cur_text, org=(0, 90), fontFace=text_para["fontFace"],
                fontScale=text_para["fontScale"], color=text_para["color"], thickness=text_para["thickness"],
                lineType=text_para["lineType"])
    # save images
    cv2.imwrite(filename=f"./image_output/{files[index - 1]}", img=cur_image_rgb)

video = cv2.VideoCapture("W:\COMP\9517\project\out.mp4")
video_cap(video)
