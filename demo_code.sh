#!/usr/bin/env bash
#!/usr/bin/env python

# demo code for segmentation some parts need to manually set
# by Lance liu



echo $HOME
conda info --envs
conda activate intensity_normalization

IMG_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_samples_test
MASK_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_FullBrainSuite_cortex_tca_mask_test
# NORM_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_norm_test
PREP_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_processed_test
OUTPUT_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_out_test
HDF5_DIR=/home/uqlliu10/nas_home/MRI_segmentation/IXI_hdf5_test

# change path to your own file path !!!

# fcm-normalize -i $IMG_DIR -m $MASK_DIR -o $NORM_DIR -v -c t1
# preprocess -i $NORM_DIR -m $MASK_DIR -o $PREP_DIR -r 1 1 1
preprocess -i $IMG_DIR -m $MASK_DIR -o $PREP_DIR -r 1 1 1
coregister -i $PREP_DIR/imgs -o $OUTPUT_DIR -v

conda deactivate
conda activate 3dunet
#
python hdf5_sample.py -i $OUTPUT_DIR -o $HDF5_DIR
python predict.py --config resources/test_config_ce_IXI_test.yaml
# python hdf5_to_nii_3d.py -i $HDF5_DIR
python hdf5_to_nii.py -i $HDF5_DIR
