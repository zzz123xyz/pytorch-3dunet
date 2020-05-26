#!/usr/bin/env bash
#!/usr/bin/env python
# by Lance liu
# train the model for full_brain_round_singlechannel


echo $HOME
# conda info --envs
# conda activate 3dunet

YAML=resources/train_config_dice_IXI_124_full_brain_round_singlechannel_wiener.yaml
# YAML=resources/train_config_dice_IXI_124_full_brain_round_singlechannel.yaml

# mpirun -np 2 -bind-to none -map-by slot -x NCCL_DEBUG=INFO -x LD_LIBRARY_PATH -x PATH -x HOROVOD_MPI_THREADS_DISABLE=1 --mca btl openib,self,vader train.py --config $YAML
# horovodrun -np 2 -H localhost:2 train.py --config $YAML
python train.py --config $YAML
