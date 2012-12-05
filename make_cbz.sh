#!/bin/bash

# Compress a bunch of folders downloaded by the python script into nice, happy, cbz
# files.
#
# usage: make_cbz.sh <folder>
#
# Since this script isn't very smart, you should probably omit the trailing slash when
# supplying the folder name.

folder=$1

for x in `seq 1 38`;
do

volume=`printf %02d $x` # Pad the volume number with zeros if needed

zip $folder-$volume.zip $folder/$volume/*;
mv $folder-$volume.zip $folder-$volume.cbz;

done

