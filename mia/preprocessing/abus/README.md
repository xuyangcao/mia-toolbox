# Preprocessing scrips for ABUS images  


## For the 2D ABUS segmentation task, we performed the following preprocess:

1. resize_data_11.py

> resize the original image with a resolution of 0.21x0.21x0.21

2. gen_2d_images.py
    
> generate 2d images according to the resized image and label

3. gen_train_val_test_3d.py

> generate training, validation and testing datset according to all the labeled image available

4. gen_list_2d.py 

> generate lists of 2d images according to the previous generated lists.

5. split_label_unlabel_data.py

> random select certainty number of labled image for semi-supervised learning

6. select_data_from_list.py

> this script select image and label from train.list for supervised learning using part of the labeled images

## for the 3D ABUS segmentation task, we performed the following preprocess:

1. resize_volume.py

> resize original image into a resolution of 0.52x0.52x0.52 

2. extract_roi_3d.py, _extract_roi.py

> extract ROI of the lesion according to the available label

## utils 

1. show_results_3d.py

> visualization of the croped ROi

2. show_number_of_patients.py

> show how many patients in the dataset

3. change_label_format.py

> change label from dicom to nii.gz
