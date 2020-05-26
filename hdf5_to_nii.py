# this the code converts the hdf5 to nii for multi channel results of prediction
import h5py
import os
import nibabel as nib
import numpy as np
import glob
# from matplotlib import pyplot as plt
import sys
import getopt
# import ipdb

argv = sys.argv
sample_fullpath = ''
try:
    opts, args = getopt.getopt(argv[1:], "hi:n:", ["sample=", "number="])
except getopt.GetoptError:
    print(argv[0]+' -i input_path')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(argv[0]+'-i input_path')
        sys.exit()
    elif opt in ("-i", "--input"):
        input_path = arg
        print('input_path is "' + input_path)
    elif opt in ("-n", "--number"):
        n_sample = arg
        print('number of samples to process is ' + n_sample)


# sample path and name (change these accordingly)
# # sample_path = 'resources/val_hdf5/'
# # sample_path = 'resources/val_hdf5_from_124/'
# # sample_path = 'resources/train_val_t1t2pd_hdf5/'
# # sample_path = 'resources/val_hdf5_from_124_unnorm/'
#
# input_path = 'resources/val_hdf5_full_head_round_from_124'
# n_sample = 10

sample_path = input_path+'/'

samlpe_suffix = '_predictions.h5'
samlpe_ext = '.nii.gz'
samplepathlist = glob.glob(sample_path+'*'+samlpe_suffix)
samplelist = [i.split('/')[-1] for i in samplepathlist]
# ipdb.set_trace()
n_sample = int(n_sample)
samplelist = samplelist[:n_sample]

for i in range(len(samplelist)):

    sample_fullpath = os.path.join(sample_path, samplelist[i])
    datahdf5 = h5py.File(sample_fullpath, 'r')
    datahdf5 = datahdf5['predictions']

    n_channels = datahdf5.shape[0]
    sample_name = samplelist[i].split('.')[0]
    # ipdb.set_trace()
    for j in range(n_channels):
        data = np.squeeze(datahdf5[j, :, :, :])
        img = nib.Nifti1Image(data, np.eye(4))
        img.header.get_xyzt_units()
        nib.save(img, os.path.join(sample_path, sample_name+'_s' + str(j)
                                   + samlpe_ext))
    ind = np.argmax(datahdf5, 0)
    ind = ind.astype(np.single)
    label_output = nib.Nifti1Image(ind, np.eye(4))
    label_output.header.get_xyzt_units()
    nib.save(label_output, os.path.join(sample_path, sample_name+'_join' + samlpe_ext))
