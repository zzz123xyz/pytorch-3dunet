$TARGET_PATH='G:\New Research\IXI-T1\'
$REF_PATH='Y:\MRI_segmentation\IXI_FullBrainSuite_cortex_tca_mask\'
$Ref_extension = '.cortex.tca.mask.nii.gz'
$EXE = 'C:\Program Files\BrainSuite19a\bin\cortical_extraction.cmd'


#echo $TARGET_PATH

#$FILE = (Get-Item ($TARGET_PATH+"IXI425-IOP-0988-T1.nii.gz")).FullName
#echo $FILE

#$t = (Split-Path -Path $FILE -Leaf).Split(".")[0]
#echo $t

foreach($f in (Get-ChildItem -Path ($TARGET_PATH+"*.nii.gz") -Name))
{   #echo $f
    $Basename = (Split-Path -Path $f -Leaf).Split(".")[0]
    $Ref_name = $Basename+$Ref_extension
    if(Test-Path ($REF_PATH+'*') -PathType Leaf -Include $Ref_name)
    {echo true}
    else
    {
    echo false
    echo "compute the tca mask"
    .$EXE ($TARGET_PATH+$f)
    }
    #echo $Ref_name

    #if( )
}

# FILE in `ls *-PD.nii.gz`; do BF=`basename $FILE -PD.nii.gz`;
#   if Test-Path $REF_PATH$BF.cortex.tca.mask.nii.gz;
