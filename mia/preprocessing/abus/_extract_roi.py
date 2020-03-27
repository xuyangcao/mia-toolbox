import cv2
import numpy as np

def extract_roi_3d(label, image, shape, mode='shift', check_padding=True):
    r""" extract region of interest of a 3D image according to it's binary label
   
    Parameters:
    ---
    label: 3D of ndarray
        Binary mask of an image

    image: 3D of ndarray
        Image volume of a 3D image

    shape: tuple of 3 ints
        Shape of the output ROI image

    mode: str. Default: 'shift'
        crop mode
        'shift' (default): the ROI center will be shifted if index out of bounds
        'pad': ROI center fixed, the input image will be paded before croping the ROI, 
                in this mode, each ROI will be in the center of the output image. 

    check_padding: bool. Default: True
        if True, the output shape could be larger than input image. 
   
    Returns:
    ---
    new_label: 3D of ndarray
        ROI of the input label 
 
    new_image: 3D of ndarray 
        ROI of the input image
    """

    input_height, input_width, input_depth = label.shape
    output_height, output_width, output_depth = shape 
    assert label.shape == image.shape
    if check_padding:
       label, image =  _check_padding(label, image, shape)
    else:
        if output_height > input_height or output_width > input_width or output_depth > input_depth:
            raise(RuntimeError('output size should no bigger than input size!'))

    # project label according to the last dimention
    temp_label_last = np.max(label, axis=2)
    x, y, bbx_width, bbx_height = cv2.boundingRect(temp_label_last)
    center_x = round(x + bbx_width / 2)
    center_y = round(y + bbx_height / 2)

    # project label according to the first dimention
    temp_label_first = np.max(label, axis=0)
    z, _, bbx_width, _ = cv2.boundingRect(temp_label_first)
    center_z = round(z + bbx_width / 2)

    window_width = round(output_width / 2)
    window_height = round(output_height / 2)
    window_depth = round(output_depth / 2)

    if mode == 'shift':
        # shift the center point if the ROI would out of bounds
        if center_x - window_width < 0:
            center_x += abs(center_x - window_width)

        if center_x + window_width > temp_label_last.shape[1]:
            center_x -= center_x + window_width - temp_label_last.shape[1]    

        if center_y - window_height < 0:
            center_y += abs(center_y - window_height)

        if center_y + window_height > temp_label_last.shape[0]:
            center_y -= center_y +  window_height - temp_label_last.shape[0]

        if center_z - window_depth < 0:
            center_z += abs(center_z - window_depth)

        if center_z + window_depth > temp_label_first.shape[1]:
            center_z -= center_z + window_depth - temp_label_first.shape[1]

        x_start = 0 if center_x - window_width < 0 else center_x - window_width
        y_start = 0 if center_y - window_height < 0 else center_y - window_height 
        z_start = 0 if center_z - window_depth < 0 else center_z - window_depth 

        new_label = label[y_start:y_start+output_height, x_start:x_start+output_width, z_start:z_start+output_depth]
        new_image = image[y_start:y_start+output_height, x_start:x_start+output_width, z_start:z_start+output_depth]

        return new_label, new_image

    if mode == 'pad':
        # padding original image to make ROI center of the output image
        x_start = center_x - window_width
        x_left_pad = 0 if x_start > 0 else abs(x_start)
        x_right_pad = 0 if x_start + output_width < temp_label_last.shape[1] else abs(x_start + output_width - temp_label_last.shape[1])

        y_start = center_y - window_height
        y_left_pad = 0 if y_start > 0 else abs(y_start)
        y_right_pad = 0 if y_start + output_height < temp_label_last.shape[0] else abs(y_start + output_height - temp_label_last.shape[0])

        z_start = center_z - window_depth
        z_left_pad = 0 if z_start > 0 else abs(z_start)
        z_right_pad = 0 if z_start + output_depth < temp_label_first.shape[1] else abs(z_start + output_depth - temp_label_first.shape[1])

        padding = x_left_pad + x_right_pad + y_left_pad + y_right_pad + z_left_pad + z_right_pad 
        if padding:
            label = np.pad(label, ((y_left_pad, y_right_pad), (x_left_pad, x_right_pad), (z_left_pad, z_right_pad)), mode='constant', constant_values=0)
            image = np.pad(image, ((y_left_pad, y_right_pad), (x_left_pad, x_right_pad), (z_left_pad, z_right_pad)), mode='constant', constant_values=0)

            new_label, new_image = extract_roi_3d(label, image, shape, mode)
            return new_label, new_image 
        else:
            # get roi image
            new_label = label[y_start:y_start+output_height, x_start:x_start+output_width, z_start:z_start+output_depth]
            new_image = image[y_start:y_start+output_height, x_start:x_start+output_width, z_start:z_start+output_depth]

            return new_label, new_image

def _check_padding(label, image, shape):
    input_height, input_width, input_depth = label.shape
    output_height, output_width, output_depth = shape 

    if output_width > input_width:
        x_pad = round((output_width - input_width) / 2)
    else:
        x_pad = 0

    if output_height > input_height:
        y_pad = round((output_height - input_height) / 2) 
    else:
        y_pad = 0
    
    if output_depth > input_depth:
        z_pad = round((output_depth - input_depth) / 2)
    else:
        z_pad = 0

    if (x_pad + y_pad + z_pad) == 0:
        return label, image
    else:
        #print('x_pad: {}, y_pad: {}, z_pad: {}'.format(x_pad, y_pad, z_pad))
        new_label = np.pad(label, ((y_pad, y_pad), (x_pad, x_pad), (z_pad, z_pad)), mode='constant', constant_values=0) 
        new_image = np.pad(image, ((y_pad, y_pad), (x_pad, x_pad), (z_pad, z_pad)), mode='constant', constant_values=0) 
        return new_label, new_image
