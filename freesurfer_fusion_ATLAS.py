# by lance liu
# fusion the brain labels from freesurfer and head labels from brainsuite and the lesion labels from ATLAS dataset.

import h5py
import os
import nibabel as nib
import numpy as np
from scipy.ndimage import rotate, zoom
import glob
from find_subdict_index import find_subdict_index
from matplotlib import pyplot as plt
from get_ATLAS_metadata import scan_folder, find_in_metadata_table
from label_index_replace import label_index_replace
import ipdb
# setting !!!

# sample_path = '../freesurfer_fusion_data/'
sample_path = 'I:\\MRI_segmentation\\freesurfer_fusion_data\\'
sample_name_list = scan_folder(sample_path)
freesurfer_label_path_list = glob.glob(sample_path+'*aseg-in-rawavg.mgz')
brainsuite_head_label_path_list = glob.glob(sample_path+'*skull.label.nii.gz')
lesion_path_list = glob.glob('J:\\New Research\\ATLAS_R1.1\\**\\'+'*LesionSmooth*', recursive=True)
metadata_path = "J:\\New Research\\ATLAS_R1.1\\ATLAS_Meta-Data_Release_1.1_standard_mni_updated.csv"
sample_info = find_in_metadata_table(sample_name_list, metadata_path)

# brainsuite_label_path = '../IXI_join_label/IXI017-Guys-0698-T1_full_brain_round.pvc.frac.nii.gz'
# brainsuite_head_label_path = '../IXI_SegData4Lance_400/IXI017-Guys-0698-T1.skull.label.nii.gz'

output_path = 'I:\\MRI_segmentation\\freesurfer_fusion_data\\'
sample_ext = '_joint_label.nii.gz'
# sample_ext = '.nii'
# label_ext = '.skull.label.nii' #default

# tissue lookup table
inputdict = {
    2:  [260, 129],  # skull
    6:  [6, 7, 8, 45, 46, 47],  # cerebellum
    3:  [24],  # CSF
    7:  [98],  # dura
    8:  [120, 131],  # fat
    4:  [3, 42],  # GM
    10: [123, 152],  # Muscle
    11: [143],  # Vitreous humor
    5:  [2, 41],  # WM
    0:  [0],  # background
    12: [30, 62],  # blood vessel
    13: [16]  # brain-stem
}
# 1 for skin
# 14 for embolic stroke
# 15 for embolic/hemorrhage stroke

inputdict_brainsuite = {
    0: [0],  # background
    1: [16],  # skin
    2: [17],  # skull
    3: [18, 19]  # csf
}

# processing
for one_sample in sample_name_list:
    subjectID = one_sample[:6]
    freesurfer_label_path = [s for s in freesurfer_label_path_list if subjectID in s]
    freesurfer_label_path = freesurfer_label_path[0]
    brainsuite_head_label_path = [s for s in brainsuite_head_label_path_list if subjectID in s]
    brainsuite_head_label_path = brainsuite_head_label_path[0]
    lesion_label_path = [s for s in lesion_path_list if subjectID in s]

    freesurfer_label = nib.load(freesurfer_label_path)
    freesurfer_label_volume = freesurfer_label.get_fdata()
    label_index_freesurfer = np.unique(freesurfer_label_volume)
    print(label_index_freesurfer)
    raw_affine = freesurfer_label.affine

# # test for joint label !!
# brainsuite_label = nib.load(brainsuite_label_path)
# brainsuite_label_volume = brainsuite_label.get_fdata()
# brainsuite_label_volume_rotate = np.swapaxes(brainsuite_label_volume, 0, 2)
# brainsuite_label_volume_rotate2 = np.swapaxes(brainsuite_label_volume_rotate, 0, 1)
# brainsuite_label_volume_flip = np.flipud(brainsuite_label_volume_rotate2)
# label_index_brainsuite_joint = np.unique(brainsuite_label_volume_pad)

# test for only head no brain part !!!
    brainsuite_head_label = nib.load(brainsuite_head_label_path)
    brainsuite_head_label_volume = brainsuite_head_label.get_fdata()
    # brainsuite_head_label_volume_rotate = np.swapaxes(brainsuite_head_label_volume, 0, 2)
    # brainsuite_head_label_volume_rotate2 = np.swapaxes(brainsuite_head_label_volume_rotate, 0, 1)
    # brainsuite_head_label_volume_flip = np.flipud(brainsuite_head_label_volume_rotate2)
    # label_index_brainsuite_head = np.unique(brainsuite_head_label_volume_flip)
    label_index_brainsuite_head = np.unique(brainsuite_head_label_volume)
    print(label_index_brainsuite_head)
    # make new_freesurfer_label_volume
    # new_freesurfer_label_volume = np.zeros(freesurfer_label_volume.shape)
    # for label_index in label_index_freesurfer:
    #     mylabel_value = find_subdict_index(inputdict, label_index, mylabel_value=3)
    #     boolwhich0 = freesurfer_label_volume == label_index
    #     new_freesurfer_label_volume[boolwhich0] = mylabel_value
    new_freesurfer_label_volume = label_index_replace(
        freesurfer_label_volume, inputdict, mylabel_value=3)
    # make new_brainsuite_head_label_volume
    # new_brainsuite_head_label_volume = np.zeros(brainsuite_head_label_volume.shape)
    # for label_index in label_index_brainsuite_head:
    #     mylabel_value = find_subdict_index(inputdict_brainsuite, label_index, mylabel_value=3)
    #     boolwhich1 = brainsuite_head_label_volume == label_index
    #     new_brainsuite_head_label_volume[boolwhich1] = mylabel_value
    new_brainsuite_head_label_volume = label_index_replace(
        brainsuite_head_label_volume, inputdict_brainsuite, mylabel_value=3)
    # combine freesurfer label and brainsuite label
    boolwhich2 = new_freesurfer_label_volume > 0
    # brainsuite_label_volume_flip[boolwhich2] = 0  # test for joint label !!
    # brainsuite_head_label_volume_flip[boolwhich2] = 0
    # label_joint = brainsuite_head_label_volume_flip + new_freesurfer_label_volume
    new_brainsuite_head_label_volume[boolwhich2] = 0
    label_joint = new_brainsuite_head_label_volume + new_freesurfer_label_volume
    # combine joint label with Lesions
    for l in lesion_label_path:
        lesion_label = nib.load(l)
        lesion_label = lesion_label.get_fdata()
        lesion_type = sample_info.loc[sample_info['INDI Subject ID'] == int(subjectID[1:]), [
            'Stroke type']]
        label_index = 14 if lesion_type.values == 'Embolic' else 15
        boolwhich3 = lesion_label > 0
        label_joint[boolwhich3] = label_index

    img = nib.Nifti1Image(label_joint, raw_affine)
    img.header.get_xyzt_units()
    nib.save(img, output_path + os.path.basename(one_sample).split('.')[0]+sample_ext)
