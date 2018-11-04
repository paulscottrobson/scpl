#
#	Remove SNA files
#
rm bootloader.sna ../files/bootloader.sna
#
#	Build SNA file
#
../bin/zasm -buw bootloader.asm -l bootloader.lst -o bootloader.sna
#
#	Copy to files area if successful.
#
if [ -e bootloader.sna ] 
then
	cp bootloader.sna ../files
fi

