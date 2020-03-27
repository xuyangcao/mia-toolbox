import os
import random


def gen_train_val_test_list(file_path, save_path, len_patient_id=4, ratio_train=0.6, ratio_val=0.1, ratio_test=0.3, seed=2020):
    '''Generate training, validation and testing dataset.

    Args:
    ----

        file_path: str 
            file path containing all the available data.

        save_path: str
            path to save train.list, val.list and test.list

        len_patient_id: int, default: 4
            length of the patient ID (file name)

        ratio_train: float, default: 0.6
            ratio of the training dataset.

        ratio_val: float, default: 0.1
            ratio of the validation dataset. 

        ratio_test: float, default: 0.3
            ratio of the testing dataset.

        seed: int, default: 2020

    Return:
    ------ 

        None.
    
    Example:
    -------

        ```
            file_path = './data/image/' 
            save_path = './'
            gen_train_val_test_list(file_path, save_path)

        ```
    '''

    # 1. init parameters
    random.seed(seed)
    if not os.path.exists(file_path):
        raise(RuntimeError('file_path: {} doesn\'t exists!'.format(file_path)))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    train_list = 'train.list.3d'
    train_list = os.path.join(save_path, train_list)
    val_list = 'val.list.3d'
    val_list = os.path.join(save_path, val_list)
    test_list = 'test.list.3d'
    test_list = os.path.join(save_path, test_list)

    # 2. get filenames list according to patients
    filenames = [filename for filename in os.listdir(file_path)]
    filenames.sort()
    patient_id = [filename[:len_patient_id] for filename in filenames]
    patient_id = set(patient_id)
    patient_id = list(patient_id)
    patient_id.sort()
    random.shuffle(patient_id)
    #print(len(patient_id)) # 107

    # 3. split train, val and test data
    num_train_patients = round(len(patient_id) * ratio_train)
    num_val_patients = round(len(patient_id) * ratio_val)
    num_test_patients = len(patient_id) - num_train_patients - num_val_patients
    #print('num_train: {}\t num_val: {}\t num_test: {}'.format(num_train_patients, num_val_patients, num_test_patients))
    train_id = patient_id[:num_train_patients]
    val_id = patient_id[num_train_patients:num_train_patients+num_val_patients]
    test_id = patient_id[num_train_patients+num_val_patients:]
    print('num_train: {}\t num_val: {}\t num_test: {}'.format(len(train_id), len(val_id), len(test_id)))
    #print('val_patients: ', val_id)

    # 4. write filenames into each dataset
    # train
    with open(train_list, 'w') as f:
        for filename in filenames:
            if filename[:len_patient_id] in train_id:
                f.write(filename+'\n')
    # val 
    with open(val_list, 'w') as f:
        for filename in filenames:
            if filename[:len_patient_id] in val_id:
                f.write(filename+'\n')
    # text
    with open(test_list, 'w') as f:
        for filename in filenames:
            if filename[:len_patient_id] in test_id:
                f.write(filename+'\n')

    print('==> gen dataset done!')

if __name__ == '__main__':
    file_path = './resized_data_1vs1/'
    save_path = './lists'
    gen_train_val_test_list(file_path, save_path)
