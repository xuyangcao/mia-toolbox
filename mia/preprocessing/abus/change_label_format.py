import os 
import SimpleITK as sitk
import tqdm

''' change image from DICOM file to nii.gz format '''

label_path = './image'
save_label_path = './image_nii'

if not os.path.exists(save_label_path):
    os.makedirs(save_label_path)

filenames = os.listdir(label_path)
filenames.sort()

for filename in tqdm.tqdm(filenames):
    img = sitk.ReadImage(os.path.join(label_path, filename))
    sitk.WriteImage(img, os.path.join(save_label_path, filename[:-3]+'nii.gz'))