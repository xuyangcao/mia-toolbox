import os 

''' show how many patients in the abus dataset '''


label_path = '../../image/'

filenames = os.listdir(label_path)
filenames.sort

patient_ids = [ids[:4] for ids in filenames]
set_patient_ids = set(patient_ids)
print('number of patients: {}'.format(len(set_patient_ids)))