# by lance liu
import h5py
import os
import nibabel as nib
import numpy as np
import glob
from matplotlib import pyplot as plt

# change the path to your data !!!
n_sample = 124
# sample_path = '../IXI_preprocessed_387/imgs/'
sample_path = '../IXI_train_val_124/'
label_path = '../IXI_train_val_label_124/'
samlpe_ext = '.gz'
label_ext = '.skull.label.nii.gz'

samplepathlist = glob.glob(sample_path+'*'+samlpe_ext)
samplelist = [i.split('/')[-1] for i in samplepathlist]
samplelist

labelpathlist = glob.glob(label_path+'*'+label_ext)
labellist = [i.split('/')[-1] for i in labelpathlist]
labellist

for i in range(n_sample):

    sample_fullpath = os.path.join(sample_path, samplelist[i])
    sample = nib.load(sample_fullpath)
    sample_name = samplelist[i].split('.')[0]

    label_name_ext = sample_name+label_ext
    label_fullpath = os.path.join(label_path, label_name_ext)
    label = nib.load(label_fullpath)
    volume = np.swapaxes(sample.get_fdata(), 0, 2)
    volume = np.fliplr(np.swapaxes(volume, 1, 2))
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
    plt.imshow(volume[:, :, 80])
    plt.imshow(label[:, :, 80])
    label.max(0).max(0).max(0)
    label.min(0).min(0).min(0)

    volume.shape
    label.shape
    save_path = os.path.join('train_hdf5', sample_name+'.h5')

    hf = h5py.File(save_path, 'w')
    hf.create_dataset('raw', data=volume, chunks=True, compression='gzip')
    hf.create_dataset('label', data=label, chunks=True, compression='gzip')
    hf.close()
