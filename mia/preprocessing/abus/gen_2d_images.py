import os 
from tqdm import tqdm
import pydicom 
import numpy as np 
from skimage.io import imsave
import SimpleITK as sitk

def main():
    label_path = './resized_label_1vs1/'
    data_path = './resized_data_1vs1/'
    save_data_path = './image_2d/'
    save_label_path = './label_2d/'

    if not os.path.exists(save_data_path):
        os.makedirs(save_data_path)
    if not os.path.exists(save_label_path):
        os.makedirs(save_label_path)

    all_file_names = [file_name for file_name in os.listdir(label_path) if file_name.endswith('dcm')]
    #print(all_file_names)
    print(len(all_file_names))
    
    selected_filenames = []
    for num, file_name in tqdm(enumerate(all_file_names)):
        #print('processing ====%d/%d====='%(num, len(all_file_names)))
        
        img_label = sitk.ReadImage(os.path.join(label_path, file_name))
        img_data  = sitk.ReadImage(os.path.join(data_path, file_name))

        label_volume = sitk.GetArrayFromImage(img_label)
        image_volume = sitk.GetArrayFromImage(img_data)

        for i in range(label_volume.shape[0]):
            temp_label = label_volume[i]
            if np.sum(temp_label) < 10:
               continue 
            else:
                temp_image = image_volume[i]

                idx = file_name.find('.')
                transverse_slice_name = file_name[:idx] + ("_%04d"%i) + ".png"
                selected_filenames.append(transverse_slice_name)

                imsave(os.path.join(save_data_path, transverse_slice_name), temp_image)
                imsave(os.path.join(save_label_path, transverse_slice_name), temp_label*255)

    selected_patients = [filename[:4] for filename in selected_filenames]
    selected_patients = set(selected_patients)
    print('generate {} images from {} patients '.format(len(selected_filenames), len(selected_patients)))

if __name__ == '__main__':
    main()
