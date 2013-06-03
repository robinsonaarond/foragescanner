#! /usr/bin/env python

from classificator import getClass
myDB = "/Users/aaronr/Documents/fs_raspberrypi_contents/root/home/fs/Documents/fs.db"
desc = "Del Monte Pineapple Crushed In Its Own Juice"

myvar = getClass(desc,myDB)
print desc,myvar

exit()
