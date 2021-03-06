# downsample the whole quickdraw dataset to generate a train/val/test split
import os
# os.mkdir('datasplit')

# num_train = 20000
# num_val = 50
# num_test = 100

per_train = 0.8
per_val = 0.08
per_test = 0.1

with open('./indoor_cat.txt') as f:
    lines = f.readlines()


categories = []
for line in lines:
    line = line.rstrip()
    category = line.replace(' ','_')
    category = category.lower()
    categories.append(category)

with open('datasplit/categories.txt','w') as f:
    f.write('\n'.join(categories))

print('category no.%d' % len(lines))

import numpy as np

data_train = np.array([], dtype=np.uint8).reshape(0, 49152)
label_train = np.array([], dtype=np.uint8)

data_val = np.array([], dtype=np.uint8).reshape(0, 49152)
label_val = np.array([], dtype=np.uint8)

data_test = np.array([], dtype=np.uint8).reshape(0, 49152)
label_test = np.array([], dtype=np.uint8)

print(lines)
for idx, line in enumerate(lines):
    idx = int(idx)
    line  = line.rstrip()
    category = line.replace(' ','_')
    print(category)
    print(os.getcwd())
    file_np = os.path.join(os.getcwd(), '..', '..', 'data', 'penn_station', 'npy', '%s.npy' % category)

    data_category = np.load(file_np)
    # data_category = np.load(file_np).astype(np.int8)
    total_cnt = len(data_category)
    num_train = int(per_train * total_cnt)
    num_val = int(per_val * total_cnt)
    num_test = int(per_test * total_cnt)
    print (num_train, num_val, num_test)
    # generate split

    train_category = data_category[:num_train].reshape(-1, 49152)
    val_category = data_category[num_train:num_train+num_val].reshape(-1, 49152)
    test_category = data_category[num_train+num_val:num_train+num_val+num_test].reshape(-1, 49152)

    print(data_train.shape, train_category.shape)

    # concatenate: TODO: change this to pre-assign to speed up
    data_train = np.concatenate((data_train, train_category), axis=0)
    label_train = np.concatenate((label_train, np.ones((num_train,), dtype=int) * idx), axis=0)

    data_val = np.concatenate((data_val, val_category), axis=0)
    label_val = np.concatenate((label_val, np.ones((num_val,), dtype=int) * idx), axis=0)

    data_test = np.concatenate((data_test, test_category), axis=0)
    label_test = np.concatenate((label_test, np.ones((num_test,), dtype=int) * idx), axis=0)

    print('num_train=%d num_val=%d num_test=%d' % (data_train.shape[0], data_val.shape[0], data_test.shape[0]))

np.savez('datasplit/%s_split.npy' % num_train, data_train=data_train, label_train=label_train, data_val=data_val, label_val=label_val, data_test=data_test, label_test=label_test)

