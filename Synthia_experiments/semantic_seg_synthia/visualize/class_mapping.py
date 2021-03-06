





import numpy as np

nan = np.nan

recover_label = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    1,
    0
]
recover_label = np.array(recover_label, dtype='int32')

index_to_label = [
        12,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        -1,
        -1,
        11,
        ]
index_to_label = np.array(index_to_label, dtype='int32')

def index_to_label_func(x):
    return index_to_label[x]

index_to_label_vec_func = np.vectorize(index_to_label_func)

label_to_index = [
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        15,
        0,
        ]
label_to_index = np.array(label_to_index, dtype='int32')

def label_to_index_func(x):
    return label_to_index[x]

index_to_class = [
'Void',
'Sky',
'Building',
'Road',
'Sidewalk',
'Fence',
'Vegetation',
'Pole',
'Car',
'Traffic Sign',
'Pedestrian',
'Bicycle',
'Lanemarking',
'Reserved',
'Reserved',
'Traffic Light']


index_to_color = [
[0,   0,   0],
[128, 128, 128],
[128, 0,   0],
[128, 64,  128],
[0,   0,   192],
[64,  64,  128],
[128, 128, 0],
# [192, 192, 128], # pole
[128, 128, 128], # pole
# [64,  0,   128], # car
[255, 192, 0], # car
[192, 128, 128], # traffic sign
# [255, 0, 0], # traffic sign
[64,  64,  0],
[0,   128, 192],
[0,   172, 0],
[nan, nan, nan],
[nan, nan, nan],
# [0,   128, 128], # traffic light
[0,   255, 255], # traffic light
]
index_to_color = np.array(index_to_color)



