import pydicom 
import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt 
import SimpleITK as sitk 
from _extract_roi import extract_roi_3d

def main():
    '''
    遍历图像，提取ROI，保存图像
    '''
    image_path = '../image'
    label_path = '../label'

    save_image_path = './roi_img_shift'
    save_label_path = './roi_label_shift'

    if not os.path.exists(save_image_path):
        os.makedirs(save_image_path)
        os.makedirs(save_label_path)
    
    label_names = [filename for filename in os.listdir(label_path) if filename.endswith('.dcm')]
    label_names.sort()

    for num, filename in enumerate(label_names):
        print('processing==== %d/%d ====%s'%(num, len(label_names), filename))

        image_ds = pydicom.dcmread(os.path.join(image_path, filename))
        label_ds = pydicom.dcmread(os.path.join(label_path, filename))

        image_volume = image_ds.pixel_array
        label_volume = label_ds.pixel_array

        new_label_volume, new_image_volume = extract_roi_3d(label_volume, image_volume, shape=(128, 64, 128), mode='shift')
        print('{} ===> {}'.format(label_volume.shape, new_label_volume.shape))

        image_img = sitk.GetImageFromArray(new_image_volume)
        sitk.WriteImage(image_img, os.path.join(save_image_path, filename))
        label_img = sitk.GetImageFromArray(new_label_volume)
        sitk.WriteImage(label_img, os.path.join(save_label_path, filename))

        # change tag information
        #image_ds.NumberOfFrames = str(new_image_volume.shape[0])
        #image_ds.Rows = new_image_volume.shape[1]
        #image_ds.Columns = new_image_volume.shape[2]
        #label_ds.NumberOfFrames = str(new_label_volume.shape[0])
        #label_ds.Rows = new_label_volume.shape[1]
        #label_ds.Columns = new_label_volume.shape[2]

        ## save image data information
        #image_ds.PixelData = new_image_volume.tobytes()
        #label_ds.PixelData = new_label_volume.tobytes()

        ## save image
        #image_ds.save_as(os.path.join(save_image_path, filename))
        #label_ds.save_as(os.path.join(save_label_path, filename))

if __name__ == '__main__':
    main()


    #image_path = '../image/0001_RLAT.dcm'
    #label_path = '../label/0001_RLAT.dcm'

    #image_ds = pydicom.dcmread(image_path)
    #label_ds = pydicom.dcmread(label_path)
    #image_volume = image_ds.pixel_array
    #label_volume = label_ds.pixel_array

    #print(image_volume.shape)
    #new_label, new_image = extract_roi_3d(label_volume, image_volume, shape=(128, 64, 128), mode='shift')
    #print(new_label.shape)

    #label_img = sitk.GetImageFromArray(new_label_volume)
    #sitk.WriteImage(label_img, './label.dcm')
    #image_img = sitk.GetImageFromArray(new_image_volume)
    #sitk.WriteImage(image_img, './image.dcm')
