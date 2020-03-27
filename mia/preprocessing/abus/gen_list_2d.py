import os

def read_csv(filename):
    with open(filename, 'r') as f:
        filenames = f.readlines()
    filenames = [item.replace('\n', '') for item in filenames]
    filenames = [filename[:9] for filename in filenames]
    filenames = set(filenames)
    return filenames

def write_csv(save_name, filenames_src, filename_pool):
    with open(save_name, 'w') as f:
        for idx, filename in enumerate(filename_pool):
            if filename[:9] in filenames_src:
                f.write(filename+'\n')

if __name__ == "__main__":
    image_path = './image_2d/'
    filename_pool = os.listdir(image_path)

    train_list_src = './lists/train.list.3d'
    save_train_name = './lists/train.list'
    train_name_src = read_csv(train_list_src)
    write_csv(save_train_name, train_name_src, filename_pool)

    val_list_src = './lists/val.list.3d'
    save_val_name = './lists/val.list'
    val_name_src = read_csv(val_list_src)
    write_csv(save_val_name, val_name_src, filename_pool)

    test_list_src = './lists/test.list.3d'
    save_test_name = './lists/test.list'
    test_name_src = read_csv(test_list_src)
    write_csv(save_test_name, test_name_src, filename_pool)

    print('done!')
