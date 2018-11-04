#
#		Test the boot read/write works
# 
rm bootloader.sna boot_save.img
#
#		Create a dummy boot.img file large enough
#
python3 makerandomimage.py
#
#		Assemble with testing on
#
../bin/zasm -buw test.asm -l bootloader.lst -o bootloader.sna
#
#		Run it
#
if [ -e bootloader.sna ] 
then
	wine ../bin/CSpect.exe -zxnext -cur -brk -exit -r3 bootloader.sna
fi
#
#		Check it was copied in and out successfully.
#
if [ -e boot_save.img ]
then 
	echo Comparing the input and output boot images now.
	cmp boot.img boot_save.img
fi
rm boot.img boot_save.img


