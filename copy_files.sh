for filename in *.xml
do
  cp "$filename" /mnt/trove.storage.fu-berlin.de/ohd-av/bas_packages/adg/"${filename%.*}"/"$filename"
done
