import os
from tqdm import tqdm
import argparse 
import numpy as np 
from numpy.random import shuffle
import random 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labeled_num', '-L', type=int, default=100)
    parser.add_argument('--patient_num', '-S', type=int, default=None)
    parser.add_argument('--file', '-F', type=str, default='./lists/train.list')
    parser.add_argument('--seed', type=int, default=2020)
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    random.seed(args.seed)

    # read all filenames in list files
    with open(args.file, 'r') as f:
        filenames = f.readlines()
    filenames = [item.replace('\n', '') for item in filenames]
    filenames.sort()
    random.shuffle(filenames)
    print('total filenames: {}'.format(len(filenames)))
    #print('==== filenames[:4]', filenames[:4])

    # select patient, if None, all patients are selected
    patient_ID = [filename[:4] for filename in filenames]
    set_patient_ID = set(patient_ID)
    print('total {} patients'.format(len(set_patient_ID)))
    selected_patient_ID = list(set_patient_ID)
    selected_patient_ID.sort()
    selected_patient_ID = selected_patient_ID[:args.patient_num]
    #selected_patient_ID = list(set_patient_ID)[:args.patient_num]
    print('select {} pathents'.format(len(selected_patient_ID)))
    print('selected pathent IDs:\n', selected_patient_ID)
    print('-'*100)
    #print('===== selected_patient_ID[:4]', selected_patient_ID[:4])

    # select slices from the above selected patients 
    selected_filenames = [filename for filename in filenames if filename[:4] in selected_patient_ID] 
    random.shuffle(selected_filenames)
    labeled_filenames = selected_filenames[:args.labeled_num]
    unlabeled_filenames = selected_filenames[args.labeled_num:]
    print('labeled_slice_no:{}, unlabeled_slice_no:{}'.format(len(labeled_filenames), len(unlabeled_filenames)))
    print('selected slices:\n', labeled_filenames)

    with open('train.'+str(args.labeled_num)+'.labeled', 'w') as f:
        for filename in labeled_filenames:
            f.write(filename+'\n')
    with open('train.'+str(args.labeled_num)+'.unlabeled', 'w') as f:
        for filename in unlabeled_filenames:
            f.write(filename+'\n')

    labeled_patients = [filename[:4] for filename in labeled_filenames]
    labeled_patients = set(labeled_patients)
    print('\nthese labeled slices were acturally selected from {} patients!'.format(len(labeled_patients)))

    print('done!')



if __name__ == "__main__":
    main()
