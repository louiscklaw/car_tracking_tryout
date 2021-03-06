#!/usr/bin/env python3

"""car tracking with python and opencv

To run:
    with cam:
        python VehicleCounting.py -vid 0
    with video file:
        python VehicleCounting.py -vid <video_filename>

TODO:
    * For module TODOs    * customizable settings file

Ref/source:
    https://github.com/SaoYan/VehicleCounting
    https://link.springer.com/article/10.1007/s11760-016-1038-7

Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""


import cv2
import sys
import copy
import numpy as np

import logging


# NOTE: custom import

from res.const import *
from res.run_settings import *
from res.run_logging import *

# NOTE: init_logging
init_logging()


# NOTE: global space settings
display_video_window = run_settings.display_video_window

# customize_offset_height=53+40
customize_offset_height = 0
offset_height = 24 + customize_offset_height


class video_properties():
    height = 0
    width = 0


def help():
    print("--------------------------------------------------------------------------")
    print("Uasge:")
    print("python ./VehicleCounting.py -vid { <video filename> | 0 }")
    print("Example:")
    print("to use video file: python ./VehicleCounting.py -vid test.mp4")
    print("to use camera: python ./VehicleCounting.py -vid 0")
    print("--------------------------------------------------------------------------\n")


def vehicle_location(detect_zone, W, L):
    '''''''''''''''''''''
    W: width of each lane
    L: width of the DVL
    '''''''''''''''''''''
    tmp_conv = list()
    tmp_1 = np.ones((L, W), dtype=np.float32)
    for c in range(detect_zone.shape[1] - W):
        conv_region = np.float32(detect_zone[0:L, c:c + W])
        S = np.sum(np.multiply(conv_region, tmp_1))
        tmp_conv.append(S)
    temp = np.array(tmp_conv)
    cv2.normalize(temp, temp, 0., 1., cv2.NORM_MINMAX)
    tmp_conv = temp.tolist()
    return tmp_conv


def dispHist(hist, histSize):
    maxVal = np.amax(np.array(hist))
    minVal = np.amin(np.array(hist))
    histDisp = np.zeros((histSize, histSize), dtype=np.uint8)
    hpt = int(0.9 * histSize)
    if int(maxVal) != 0:
        for h in range(histSize):
            binVal = hist[h]
            intensity = int(binVal * hpt / maxVal)
            cv2.line(histDisp, (h, histSize), (h, histSize - intensity), (255))
    return histDisp


def step_2_vehicle_detection(mask):
    # step 2: vehicle detection (morphology operation)
    objects = np.copy(mask)

    cross_element = cv2.getStructuringElement(cv2.MORPH_CROSS, (7, 7))
    disk_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

    objects = cv2.dilate(objects, cross_element)
    objects = cv2.dilate(objects, disk_element)

    return objects


def step_3_vehicle_location(objects, frame, height, width_DVL, width_lane):
    # step 3: vehicle location
    detect_zone = np.copy(objects[height - offset_height - width_DVL:height - offset_height, 0:frame.shape[1]])
    tmp_conv = vehicle_location(detect_zone, width_lane, width_DVL)
    return tmp_conv


def open_video_source(videoFilename):
    try:
        logging.info(STATUS.OPENING_VIDEO)

        if videoFilename == "0":
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(videoFilename)

        return cap

    except Exception as e:
        logging.error(ERRORS.OPEN_VIDEO_SOURCE)


def get_video_properties(cap):
    try:
        logging.info(STATUS.GETTING_PROPERTIES_FROM_SOURCE)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height

    except Exception as e:
        logging.error(ERRORS.GETTING_PROPERTIES_FROM_SOURCE)


def detect_peaks(tmp_conv):
    # NOTE: settings
    T_HDist = run_settings.T_HDist
    T_s = run_settings.T_s

    # NOTE: init variables
    num = 0
    space = 20

    peak_idx_current = list()

    # detect all the peak candidates
    for i in range(len(tmp_conv)):
        if i < space:
            continue
        elif i > len(tmp_conv) - space:  # // only compare with former elements
            if (tmp_conv[i] > T_s) & (tmp_conv[i] > tmp_conv[i - space]):
                if len(peak_idx_current) == 0:
                    peak_idx_current.append(i)
                    num = num + 1
                elif abs(i - peak_idx_current[num - 1]) > T_HDist:
                    peak_idx_current.append(i)
                    num = num + 1
        else:  # compare with both former and latter elements
            if (tmp_conv[i] > T_s) & (tmp_conv[i] > tmp_conv[i - space]) & (tmp_conv[i] > tmp_conv[i + space - 1]):
                if len(peak_idx_current) == 0:
                    peak_idx_current.append(i)
                    num = num + 1
                elif abs(i - peak_idx_current[num - 1]) > T_HDist:
                    peak_idx_current.append(i)
                    num = num + 1

    return num, peak_idx_current


def test_counting(cap, peak_idx_current, peak_idx_last):
    min_value = 10000
    T_VDist = run_settings.T_VDist
    add_num = 0

    # counting
    if int(cap.get(cv2.CAP_PROP_POS_FRAMES)) == 1:  # 1st frame
        add_num = len(peak_idx_current)
    else:  # eliminate repeat counting
        for i in range(len(peak_idx_current)):
            for j in range(len(peak_idx_last)):
                if abs(peak_idx_current[i] - peak_idx_last[j]) < min_value:
                    min_value = abs(peak_idx_current[i] - peak_idx_last[j])
            if min_value > T_VDist:
                add_num = add_num + 1
            min_value = 10000
    return add_num


def draw_on_video(frame, height, width, tmp_conv, peak_idx_current, objects, cap, add_num, total_num):
    # output part

    width_DVL = run_settings.width_DVL

    # draw double virtual lines
    cv2.line(frame, (0, height - offset_height), (width - 1, height - offset_height), (0, 0, 255), 2)
    cv2.line(frame, (0, height - offset_height - width_DVL), (width - 1, height - offset_height - width_DVL), (0, 0, 255), 2)

    # draw hulls
    # draw vehicle location hist
    histDisp = dispHist(tmp_conv, len(tmp_conv))
    for i in range(len(peak_idx_current)):
        cv2.line(histDisp, (peak_idx_current[i], 0), (peak_idx_current[i], histDisp.shape[0] - 1), (0), 2)



    # find contours
    __, contours, __ = cv2.findContours(objects, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hulls = list()
    for i in range(len(contours)):
        hulls.append(cv2.convexHull(contours[i]))

    # drawing = np.zeros(objects.shape, dtype=np.uint8)
    # cv2.drawContours(drawing, hulls, -1, (255))

    # write the frame number on the current frame
    numFrame = str(cap.get(cv2.CAP_PROP_POS_FRAMES))
    cv2.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv2.putText(frame, numFrame, (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    # write counting results on the current frame
    counting = "+" + str(add_num) + "   " + str(total_num)
    cv2.rectangle(frame, (10, 22), (100, 40), (255, 255, 255), -1)
    cv2.putText(frame, counting, (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    # show
    if display_video_window:
        cv2.imshow("Frame", frame)
        cv2.imshow("Vehicle Detection", objects)
        # cv2.imshow("Contours", drawing)
        cv2.imshow("Vehicle Location", histDisp)


def processVideo(videoFilename):
    # NOTE: get settings
    width_lane = run_settings.width_lane
    width_DVL = run_settings.width_DVL

    T_VDist = run_settings.T_VDist

    # NOTE: init value
    total_num = 0

    peak_idx_last = list()

    cap = open_video_source(videoFilename)
    video_properties.width, video_properties.height = get_video_properties(cap)

    # read input data & process
    # press'q' for quitting

    # background subtractor
    pMOG = cv2.bgsegm.createBackgroundSubtractorMOG()

    total_number_of_frame = 0

    while True:
        ret, frame = cap.read()
        total_number_of_frame+=1

        if not ret:
            print("Unable to read next frame.")
            print("Exiting...")
            break

        # step 1: background subtraction
        mask = pMOG.apply(frame)

        objects = step_2_vehicle_detection(mask)

        height = video_properties.height
        width = video_properties.width

        tmp_conv = step_3_vehicle_location(objects, frame, height, width_DVL, width_lane)

        # step 4: vehicle counting

        num, peak_idx_current = detect_peaks(tmp_conv)

        add_num = test_counting(cap, peak_idx_current, peak_idx_last)

        total_num = total_num + add_num

        draw_on_video(frame, height, width, tmp_conv, peak_idx_current, objects, cap, add_num, total_num)

        # re-initialization
        add_num = 0
        peak_idx_last = copy.deepcopy(peak_idx_current)
        peak_idx_current = list()

        c = cv2.waitKey(run_settings.pause_between_screen)
        if c >= 0:
            if chr(c) == 'q':
                break
            else:
                continue
        else:
            continue
    print("total number of vehicles: " + str(total_num))
    cap.release()


def main():


    # check for the input parameter correctness
    if len(sys.argv) != 3:
        # print help information
        help()

        print("Incorret input list")
        print("exiting...")
        return

    # run algorithm
    if sys.argv[1] == "-vid":
        if display_video_window:
            # create GUI windows
            cv2.namedWindow("Vehicle Detection")
            # cv2.namedWindow("Contours")
            cv2.namedWindow("Vehicle Location")
            cv2.namedWindow("Frame")

        processVideo(sys.argv[2])

        # destroy GUI windows
        cv2.destroyAllWindows()

    else:
        print("Please, check the input parameters.")
        print("exiting...")
        return

    sys.exit(EXITS.CLEAR_EXIT)

if __name__ == "__main__":
    main()
