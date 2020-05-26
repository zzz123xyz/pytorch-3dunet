# this the code converts the hdf5 to nii for 3d sample only not for multi channel case
import h5py
import os
import nibabel as nib
import numpy as np
import glob
from matplotlib import pyplot as plt
import sys
import getopt
import ipdb

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
        print('number of samples to process is "' + n_sample)

# change the path to your data !!!
# sample path and name (change these accordingly)
# sample_path = 'resources/val_hdf5/'
# sample_path = 'resources/val_hdf5_from_124/'
sample_path = input_path+'/'
samlpe_suffix = '_predictions.h5'
# samlpe_suffix = '.h5'
samlpe_ext = '.nii.gz'
samplepathlist = glob.glob(sample_path+'*'+samlpe_suffix)
samplelist = [i.split('/')[-1] for i in samplepathlist]
samplelist

# ipdb.set_trace()  # BREAKPOINT
for i in range(len(samplelist)):

    sample_fullpath = os.path.join(sample_path, samplelist[i])
    datahdf5 = h5py.File(sample_fullpath, 'r')
    # datahdf5 = datahdf5['predictions']
    datahdf5 = datahdf5['raw']

    n_channels = 1
    sample_name = samplelist[i].split('.')[0]
    for j in range(n_channels):
        data = np.squeeze(datahdf5[:, :, :])
        img = nib.Nifti1Image(data, np.eye(4))
        img.header.get_xyzt_units()
        nib.save(img, os.path.join(sample_path, sample_name+'_s' + str(j)
                                   + samlpe_ext))
