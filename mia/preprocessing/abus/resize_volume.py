import cv2 
import SimpleITK as sitk 
import pydicom 
import numpy as np 
from skimage.morphology import closing, square, opening, rectangle
import copy
import os 
from tqdm import tqdm

def resize_volume_with_shape(ds, label_volume, width=160):
    # 1. get image and label volume and then resize to (width, width, width)
    img_volume = ds.pixel_array.astype(np.float)
    shape = img_volume.shape #shape for change tags
    # last dimention, resize 0,1 dimention
    new_img_volume = np.zeros((width, width, img_volume.shape[2]), dtype=np.uint8)
    new_label_volume = np.zeros_like(new_img_volume)
    for i in range(img_volume.shape[2]):
        temp = img_volume[:, :, i]
        temp = cv2.resize(temp, (width, width))
        new_img_volume[:, :, i] = temp

        temp = label_volume[:, :, i]
        temp = cv2.resize(temp, (width, width))
        new_label_volume[:, :, i] = temp
    img_volume = new_img_volume
    label_volume = new_label_volume
    # first dimention, resize 1,2 dimention 
    new_img_volume = np.zeros((width, width, width), dtype=np.uint8)
    new_label_volume = np.zeros_like(new_img_volume)
    for i in range(img_volume.shape[0]):
        temp = img_volume[i]
        temp = cv2.resize(temp, (width, width))
        new_img_volume[i] = temp
    
        temp = label_volume[i]
        temp = cv2.resize(temp, (width, width))
        new_label_volume[i] = temp
    img_volume = new_img_volume
    label_volume = new_label_volume

    #2. chagne tags information
    ds.Columns = width
    ds.Rows = width
    ds.NumberOfFrames = width
    # get old tags
    pixel_space = ds.PixelSpacing
    slice_space = ds.SpacingBetweenSlices
    # change tags to new value 
    ds.SpacingBetweenSlices = shape[0] * float(slice_space) / width # 
    pixel_space_x = float(pixel_space[0])
    pixel_space_x = shape[1] * pixel_space_x / width 
    pixel_space_y = float(pixel_space[1])
    pixel_space_y = shape[2] * pixel_space_y / width
    pixel_space = [str(pixel_space_x), str(pixel_space_y)]
    ds.PixelSpacing = pixel_space
    # asign new pixel_data to dstaset
    ds_mask = copy.deepcopy(ds)
    ds_mask.PixelData = label_volume.tobytes()
    ds.PixelData = img_volume.tobytes()

    return ds, ds_mask


def resize_volume(ds, mask_volume, is_origin=True):
    '''
    将原始图像resize为shape大小，为了在itksnap中读取出来的图像是真实物理尺寸，需要修改dcm的tag信息
    Parameter:
    ---
    is_origin: 如果设置为TRUE，则分辨率改为0.5250 * 0.5250 * 0.5250, 这样的图像看起来有点小。默认为True
    '''

    pixel_space = ds.PixelSpacing
    slice_space = ds.SpacingBetweenSlices
    img_volume = ds.pixel_array

    depth, width, height = img_volume.shape

    # 1. 原始图像的冠状面减小维度
    fx = float(pixel_space[1]) / float(slice_space)
    fy = 1

    new_img_volume = np.zeros((depth, width, round(height * fx)), dtype=img_volume.dtype)
    for i in range(width):
        temp = img_volume[:, i, :]
        temp = cv2.resize(temp, (0, 0), fx = fx, fy = fy)
        new_img_volume[:, i, :] = temp
    
    pixel_space = [pixel_space[0], slice_space]
    ds.PixelSpacing = pixel_space
    ds.Columns = new_img_volume.shape[2]
    # ds.PixelData = new_img_volume.tobytes()

    # 2. 原始图像的横断面减小维度,空间分辨率变为0.5250*0.5250*0.5250
    img_volume = new_img_volume
    depth, width, height = img_volume.shape

    fx = 1
    if is_origin:
        fy = float(pixel_space[0]) / float(slice_space)  
    else:
        fy = 0.5

    new_img_volume = np.zeros((depth, round(width*fy), height), img_volume.dtype)
    for i in range(depth):
        temp = img_volume[i]
        temp = cv2.resize(temp, (0, 0), fx = fx, fy = fy)
        new_img_volume[i] = temp

    pixel_space = [str(float(pixel_space[0])/ fy), slice_space]
    ds.PixelSpacing = pixel_space
    ds.Rows = new_img_volume.shape[1]
    ds.PixelData = new_img_volume.tobytes()
    # ds.save_as('haha.dcm')

    # 3. mask图像减小到和原始图像相同的维度
    new_mask_volume = np.zeros((mask_volume.shape[0], mask_volume.shape[1], new_img_volume.shape[2]), dtype=mask_volume.dtype)
    for i in range(mask_volume.shape[1]): # 冠状面
        temp = cv2.resize(mask_volume[:, i, :], (new_img_volume.shape[2], new_img_volume.shape[0]))
        new_mask_volume[:, i, :] = temp
    
    mask_volume = new_mask_volume # 横断面
    new_mask_volume = np.zeros(new_img_volume.shape, mask_volume.dtype)
    for i in range(mask_volume.shape[0]):
        temp = cv2.resize(mask_volume[i], (new_img_volume.shape[2], new_img_volume.shape[1]))
        new_mask_volume[i] = temp

    # 4. 对mask图像做一些形态学的开闭运算,这里不再对label进行处理，因此注释掉了
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
    
    ds_mask = copy.deepcopy(ds)
    ds_mask.PixelData = new_mask_volume.tobytes()

    return ds, ds_mask
    
def main():
    '''
    - 遍历所有的图像, 执行volume的resize操作, 需要image和label都是DICOM格式图像
    - 提供了两种resize方式：一种是不管图像的voxel size，直接将图像变为160x160x160
    - 另一种是根据vixel size，将图像改为0.52x0.52x0.52分辨率的尺寸，resize后的图像尺寸大概为318x76x290
    - 经过测试，发现使用基于patch的分割方式中，第二种方式较好，因此这里使用的是第二种方式。
    '''
    img_path = '../../abus_data/image/'
    label_path = '../../abus_data/label/'
    save_img_path = './image/'
    save_label_path = './label/'

    if not os.path.exists(save_img_path):
        os.makedirs(save_img_path)
    if not os.path.exists(save_label_path):
        os.makedirs(save_label_path)
    # read all labels with .dcm 
    label_names = [filename for filename in os.listdir(label_path) if filename.endswith('.dcm')]

    for num, label_name in tqdm(enumerate(label_names)):
        # idx = label_name.find('.')
        # img_name = label_name[:idx] + '.dcm'
        img_name = label_name
        
        ds = pydicom.dcmread(os.path.join(img_path, img_name))
        label = sitk.ReadImage(os.path.join(label_path, label_name))
        label_volume = sitk.GetArrayFromImage(label)
        label_volume = label_volume.astype(np.uint8)

        img_ds, label_ds = resize_volume(ds, label_volume)
        # read image and label, resize them to a fixed size, and then save them as same name 
        # img_ds, label_ds = resize_volume_with_shape(ds, label_volume)

        # img_name = label_name[:-3] + '.nii.gz'
        img_ds.save_as(os.path.join(save_img_path, img_name))
        label_ds.save_as(os.path.join(save_label_path, img_name))
        
    print('done!')

if __name__ == '__main__':
    main()