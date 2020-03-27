import numpy as np 
import pydicom 
import matplotlib.pyplot as plt 
from skimage.color import label2rgb
import os
import cv2



def main():

    image_path = '../../roi_3d/abus_shift/image/'
    label_path = '../../roi_3d/abus_shift/label'

    label_names = [filename for filename in os.listdir(label_path) if filename.endswith('.dcm')]
    label_names.sort()

    for num, filename in enumerate(label_names):
        print('processing==== %d/%d ====%s'%(num, len(label_names), filename))

        image_ds = pydicom.dcmread(os.path.join(image_path, filename))
        label_ds = pydicom.dcmread(os.path.join(label_path, filename))

        image_volume = image_ds.pixel_array
        label_volume = label_ds.pixel_array


        img = image_volume[:, 30, :]
        label = label_volume[:, 30, :]
        color_img = label2rgb(label, img, bg_label=0)
        cv2.imshow('first', color_img)

        img = image_volume[64, :, :]
        label = label_volume[64, :, :]
        color_img = label2rgb(label, img, bg_label=0)
        cv2.imshow('last', color_img)

        cv2.waitKey(500)

if __name__ == "__main__":
    main()
