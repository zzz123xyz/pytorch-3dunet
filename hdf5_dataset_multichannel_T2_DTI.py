# hdf5_data_multichannel.py
# --- details --- (option)
# create hdf5 data multichannel with coregistration (w prefix) for training

# --- version ---- (option)
# sample_path
# label_path
# hdf5_path
# sample_ext
# label_ext
# --- Input ---

# --- output ----

# --- ref ---

# --- note ---(option)

# by Lance Liu


import h5py
import os
import nibabel as nib
import numpy as np
import glob
from matplotlib import pyplot as plt

# n_sample = 35
n_sample = (25, 35)
# sample_path = '../IXI_preprocessed_387/imgs/'
sample_path = ['../IXI_train_val_124/',
               '../IXI_T2_train_val_124/',
               '../IXI_PD_train_val_124/']
label_path = '../IXI_train_val_label_124/'
hdf5_path = 'resources/train_val_t1t2pd_hdf5'
sample_ext = '.nii'
label_ext = '.skull.label.nii'

samplelist = []
for sample_path_single in sample_path:
    samplepathlist = glob.glob(sample_path_single+'w*'+sample_ext)
    samplelist.append([i.split('/')[-1] for i in samplepathlist])

labelpathlist = glob.glob(label_path+'w*'+label_ext)
labellist = [i.split('/')[-1] for i in labelpathlist]
labellist

# for i in range(n_sample):
for i in range(*n_sample):

    # assert samplelist[0][i][:-10] == samplelist[1][i][:-10] == samplelist[2][i][:-10], \
    #     "only processed "+str(i)+" samples, error occurs: " + \
    #     samplelist[0][i]+" does not exist in all modalities"

    sample_name = labellist[i].split('.')[0]
    volume = []
    for jj in range(len(sample_path)):
        sample_fullpath = os.path.join(sample_path[jj], samplelist[jj][i])
        sample = nib.load(sample_fullpath)
        # volume1 = np.swapaxes(sample.get_fdata(), 0, 2)
        # volume1 = np.fliplr(np.swapaxes(volume1, 1, 2))
        # volume.append(volume1)
        sample = sample.get_fdata()
        volume.append(sample)
    volume = np.stack(volume)

    label_name_ext = labellist[i]
    label_fullpath = os.path.join(label_path, label_name_ext)
    label = nib.load(label_fullpath)
    label = label.get_fdata()
    label[label == 16] = 1
    label[label == 17] = 2
    label[label == 18] = 3
    label[label == 19] = 4
    type(label)

    volume = volume.astype(np.float32)
    label = label.astype(np.int32)
    label.dtype
    volume.dtype
    plt.imshow(volume[1, :, :, 80])
    plt.imshow(label[:, :, 80])
    label.max(0).max(0).max(0)
    label.min(0).min(0).min(0)

    volume.shape
    label.shape
    save_path = os.path.join(hdf5_path, sample_name+'.h5')

    hf = h5py.File(save_path, 'w')
    hf.create_dataset('raw', data=volume, chunks=True, compression='gzip')
    hf.create_dataset('label', data=label, chunks=True, compression='gzip')
    hf.close()
