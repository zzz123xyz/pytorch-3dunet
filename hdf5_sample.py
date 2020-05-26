# by lance liu
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
brain_mask_path = ''
try:
    opts, args = getopt.getopt(argv[1:], "hi:o:", ["sample=", "brain_mask="])
except getopt.GetoptError:
    print(argv[0]+' -i input_path -o output_path')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(argv[0]+'-i input_path -o output_path')
        sys.exit()
    elif opt in ("-i", "--input"):
        input_path = arg
    elif opt in ("-o", "--output"):
        ouput_path = arg
print('input_path is "' + input_path)
print('ouput_path is "' + ouput_path)
# change the path to your data !!!


# sample_path = '../IXI_preprocessed_387/imgs/'
sample_path = input_path+'/'
samlpe_ext = '.gz'
# ipdb.set_trace()  # BREAKPOINT
samplepathlist = glob.glob(sample_path+'*'+samlpe_ext)
n_sample = len(samplepathlist)
samplelist = [i.split('/')[-1] for i in samplepathlist]
samplelist

for i in range(n_sample):

    sample_fullpath = os.path.join(sample_path, samplelist[i])
    sample = nib.load(sample_fullpath)
    sample_name = samplelist[i].split('.')[0]

    volume = np.swapaxes(sample.get_fdata(), 0, 2)
    volume = np.fliplr(np.swapaxes(volume, 1, 2))

    volume = volume.astype(np.float32)
    volume.dtype
    # plt.imshow(volume[:, :, 80])

    volume.shape
    save_path = os.path.join(ouput_path+'/', sample_name+'.h5')

    # ipdb.set_trace()  # BREAKPOINT
    hf = h5py.File(save_path, 'w')
    hf.create_dataset('raw', data=volume, chunks=True, compression='gzip')
    hf.close()
