import os 
import shutil
import argparse 
import tqdm

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=100, choices=(100, 300, 885, 1770, 4428, 8856))
    parser.add_argument('--src_image_path', type=str, default='../image/')
    parser.add_argument('--src_label_path', type=str, default='../label/')
    parser.add_argument('--save_data_path', type=str, default='../selected_data/')
    parser.add_argument('--list_path', type=str, default='./')
    parser.add_argument('--mode', type=str, default='train', choices=('train', 'val', 'test'))

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # init args
    args = get_args()
    
    # set src and dst path
    if args.mode == 'train':
        list_file = args.list_path + 'train.' + str(args.num) + '.labeled'
        save_image_path = args.save_data_path + 'image_' + str(args.num)
        save_label_path = args.save_data_path + 'label_' + str(args.num)
    elif args.mode == 'val':
        list_file = args.list_path + 'val.list'
        save_image_path = args.save_data_path + 'val_image'
        save_label_path = args.save_data_path + 'val_label'
    elif args.mode == 'test':
        list_file = args.list_path + 'test.list'
        save_image_path = args.save_data_path + 'test_image'
        save_label_path = args.save_data_path + 'test_label'
    if args.mode == 'train' and args.num == 8856:
        list_file = args.list_path + 'train.list'

    if not os.path.exists(save_image_path):
        os.makedirs(save_image_path)
    if not os.path.exists(save_label_path):
        os.makedirs(save_label_path)

    # read all filenames in list files
    with open(list_file, 'r') as f:
        list_filenames = f.readlines()
    list_filenames = [item.replace('\n', '') for item in list_filenames]

    # copy image and label
    for filename in tqdm.tqdm(list_filenames):
        shutil.copy2(os.path.join(args.src_image_path, filename),
                     os.path.join(save_image_path, filename))
        shutil.copy2(os.path.join(args.src_label_path, filename), 
                     os.path.join(save_label_path, filename))

    print('copied {} images from {} to {}'.format(len(list_filenames), args.src_image_path, save_image_path))
    print('copied {} labels from {} to {}'.format(len(list_filenames), args.src_label_path, save_label_path))
