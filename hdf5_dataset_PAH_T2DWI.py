# by lance liu
# create hdf5 data multichannel with coregistration (w prefix) for training

import h5py
import os
import nibabel as nib
import numpy as np
from scipy.ndimage import zoom
import glob
# from matplotlib import pyplot as plt
# from nipy.io.api import load_image, save_image
# import ants

sample_in = '../MRI_PAH/PA_test/SE000003_Ax_T2_Flair_20200131164246_5001.nii.gz'
sample_out = '/home/uqlliu10/nas_home/MRI_segmentation/MRI_PAH/PA_test/test1.nii.gz'

# test for nipy !!!
# img = load_image(sample_in)
# save_image(img[::2, ::2, ::2], sample_out)

# test for ants !!!
# img = ants.image_read(sample_in)
# img.shape
# ants.plot(img, nslices=24)
# img_out = ants.resample_image(img, (1, 1, 1), False, 4)
# img_out.shape
# ants.plot(img_out, nslices=24)
# ants.image_write(img_out, sample_out)

# setting !!!
# sample_path = '../IXI_preprocessed_387/imgs/'
# sample_path = ['../IXI_train_val_124/',
#                '../IXI_T2_train_val_124/',
#                '../IXI_PD_train_val_124/'] #default
# sample_path = ['../IXI_coregistered_124/']
# sample_path = ['../IXI_preprocessed_387_rest/']
# sample_path = ['../IXI-T1_processed_581minus387/imgs/']
sample_path = ['../MRI_PAH/PA_test/']

# hdf5_path = 'resources/train_val_t1t2pd_hdf5' # default
# hdf5_path = 'resources/val_hdf5_full_head_round_from_124'  # single channel
# hdf5_path = 'resources/predict_387_rest'  # single channel
# hdf5_path = 'resources/predict_processed_581minus387'  # single channel
hdf5_path = 'resources/PA_test'  # single channel
samlpe_ext = '.nii.gz'
# samlpe_ext = '.nii'
# label_ext = '.skull.label.nii' #default

# processing
samplelist = []
for sample_path_single in sample_path:
    samplepathlist = glob.glob(sample_path_single+'*'+samlpe_ext)  # maybe use ants later !!
    # samplepathlist = glob.glob(sample_path_single+'w*'+samlpe_ext)  # spm proccessed
    samplelist.append([i.split('/')[-1] for i in samplepathlist])

n_sample = len(samplelist[0])

# setting !!! if you want to process only a few samples
# n_sample = 194  # default
# n_sample = (120, 276)  # only run for validation set

for i in range(n_sample):  # default
    # for i in range(*n_sample):  # only run for validation set

    # assert samplelist[0][i][:-10] == samplelist[1][i][:-10] == samplelist[2][i][:-10], \
    #     "only processed "+str(i)+" samples, error occurs: " + \
    #     samplelist[0][i]+" does not exist in all modalities"

    sample_name = samplelist[0][i].split('.')[0]
    # sample_name = samplelist[i].split('.')[0]
    volume = []
    for jj in range(len(sample_path)):
        sample_fullpath = os.path.join(sample_path[jj], samplelist[jj][i])
        sample_nii = nib.load(sample_fullpath)
        # volume1 = np.swapaxes(sample.get_fdata(), 0, 2)
        # volume1 = np.fliplr(np.swapaxes(volume1, 1, 2))
        # volume.append(volume1)
        header = sample_nii.header
        dim1_ratio = header['pixdim'][1]
        dim2_ratio = header['pixdim'][2]
        dim3_ratio = header['pixdim'][3]
        sample = sample_nii.get_fdata()
        sample = zoom(sample, (dim1_ratio, dim2_ratio, dim3_ratio))
        sample.shape
        sample[np.isnan(sample)] = 0

        volume.append(sample)
    volume = np.stack(volume)

    volume = volume.astype(np.float32)
    volume.dtype
    # plt.imshow(volume[0, :, :, 150])

    volume = np.squeeze(volume)
    volume.shape
    save_path = os.path.join(hdf5_path, sample_name+'.h5')

    hf = h5py.File(save_path, 'w')
    hf.create_dataset('raw', data=volume, chunks=True, compression='gzip')
    hf.close()
