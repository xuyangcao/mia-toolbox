import SimpleITK as sitk 
import pydicom 
import numpy as np 
from skimage.morphology import closing, square, opening, rectangle
import copy
import os 
import cv2

def resize_volume(ds, mask_volume):
    # 将图像的物理分辨率调整为0.21x0.21x0.21, 由于第三个维度已经是0.21了，因此只需要对前两个维度rsize一下即可，后期保存为nii.gz
    pixel_space = ds.PixelSpacing #['0.07', '0.21']
    slice_space = ds.SpacingBetweenSlices #0.52
    img_volume = ds.pixel_array #318 565 718

    print('pixel_space: ', pixel_space)
    print('slice_space: ', slice_space)

    depth, width, height = img_volume.shape
    fx = float(slice_space) / float(pixel_space[1])
    fy = float(pixel_space[0]) / float(pixel_space[1])

    new_img_volume = np.zeros((round(depth*fx), round(width*fy), height))
    for i in range(height):
        temp = img_volume[:, :, i]
        temp = cv2.resize(temp, (0, 0), fx=fy, fy=fx)
        new_img_volume[:, :, i] = temp

    # 对mask图像调整为和原始图像相同的维度
    new_mask_volume = np.zeros_like(new_img_volume, new_img_volume.dtype)
    
    for i in range(mask_volume.shape[2]):
        temp = cv2.resize(mask_volume[:, :, i], (new_img_volume.shape[1], new_img_volume.shape[0]))
        new_mask_volume[:, :, i] = temp

    
    # 对mask图像做一些形态学的开闭运算
    #for i in range(new_mask_volume.shape[1]):
    #    # cv2.imshow('before', new_mask_volume[:, i, :]*255)
    #    se = rectangle(3, 5)
    #    temp = closing(new_mask_volume[:, i, :], se)
    #    temp = opening(temp, square(2))
    #    # cv2.imshow('after', temp*255)
    #    # if np.sum(temp) != 0:
    #    #     cv2.waitKey(0)
    #    new_mask_volume[:, i, :] = temp
    #for i in range(new_mask_volume.shape[2]):
    #    se = rectangle(5, 3)
    #    temp = closing(new_mask_volume[:, :, i], se)
    #    temp = opening(temp, square(2))
    #    new_mask_volume[:, :, i] = temp             

    #img = sitk.GetImageFromArray(new_img_volume)
    #sitk.WriteImage(img, './haha.nii.gz')
    #img = sitk.GetImageFromArray(new_mask_volume)
    #sitk.WriteImage(img, './haha_mask.nii.gz')

    return new_img_volume, new_mask_volume


def main():
    '''
    遍历所有的图像, 执行volume的resize操作.
    '''
    img_path = '../image/'
    label_path = '../label/'
    save_img_path = './resized_data_1vs1/'
    save_label_path = './resized_label_1vs1/'

    if not os.path.exists(save_img_path):
        os.makedirs(save_img_path)
    if not os.path.exists(save_label_path):
        os.makedirs(save_label_path)
    filenames = [filename for filename in os.listdir(label_path) if filename.endswith('dcm')]
    filenames.sort()

    for num, filename in enumerate(filenames):
        print('processing==== %d/%d ===='%(num+1, len(filenames)))
        
        ds = pydicom.dcmread(os.path.join(img_path, filename))
        label = sitk.ReadImage(os.path.join(label_path, filename))
        label_volume = sitk.GetArrayFromImage(label)
        label_volume = label_volume.astype(np.uint8)

        img_volume, label_volume = resize_volume(ds, label_volume)

        img = sitk.GetImageFromArray(img_volume.astype(np.uint8))
        sitk.WriteImage(img, os.path.join(save_img_path, filename))
        img = sitk.GetImageFromArray(label_volume.astype(np.uint8))
        sitk.WriteImage(img, os.path.join(save_label_path, filename))

        #return 

    print('done!')
if __name__ == '__main__':
    main()
