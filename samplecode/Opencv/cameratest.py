# -*- coding: utf-8 -*-
import numpy as np
import cv2


def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def camera_capture():
    USE_GPU = 1

    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        cv2.namedWindow("Camera Test", cv2.WINDOW_AUTOSIZE)

        img_gpu_src = cv2.cuda_GpuMat() 
        img_gpu_dst = cv2.cuda_GpuMat()

        while cv2.getWindowProperty("Camera Test", 0) >= 0:
            
            ##image processing WITH CUDA
            if USE_GPU == 1:        
                ret, img = cap.read()
                img_gpu_src.upload(img)
                img_gpu_dst = cv2.cuda.cvtColor(img_gpu_src, cv2.COLOR_BGR2GRAY)
                img_dst = img_gpu_dst.download()
            
            #image processing WITHOUT CUDA
            else:  
                ret, img = cap.read()
                img_dst = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow("Camera Test", img_dst)

            keyCode = cv2.waitKey(30) & 0xFF
            #Stop processing at ESC key
            if keyCode == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Couldn't open camera!")


if __name__ == "__main__":
    camera_capture()
