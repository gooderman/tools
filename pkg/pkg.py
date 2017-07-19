#!/usr/bin/python
# -*- coding: UTF-8 -*-
#compare dir file diff
import os
import sys,re
import string
import codecs
import shutil
import time
import subprocess
import zipfile
from hashlib import md5	
from py.cmp import compare
from py.cmp import rm_dir
from py.cmp import copy_dir
from py.list import list_dir
from py.aaencode import folderEncytp
def zip_file_dir(path, outfile):
	compression = zipfile.ZIP_DEFLATED
	# start = path.rfind(os.sep) + 1
	start = len(path) + 1
	z = zipfile.ZipFile(outfile, mode="w", compression=compression)
	try:
		for dirpath, dirs, files in os.walk(path):
			z.write(dirpath, dirpath[start:])
			print "zip write path ",dirpath[start:]
			for file in files:
				z_path = os.path.join(dirpath, file)
				z.write(z_path, z_path[start:])
				print "zip write file ",z_path[start:]
		
		info = zipfile.ZipInfo('good.txt',date_time=(2017,7,19,20,34,0))
		info.compress_type=zipfile.ZIP_DEFLATED
		info.comment='good'
		info.create_system=0
		z.writestr(info,"good")		
		z.close()
	except:
		if z:
			z.close()
def run():
	if len(sys.argv)<3:
		print "please input dir"
		return
	srcdir = os.path.join(os.getcwd(),sys.argv[1])
	dstdir = os.path.join(os.getcwd(),sys.argv[2])
	outdir = os.path.join(os.getcwd(),sys.argv[2]+"-"+sys.argv[1])
	outzip = sys.argv[2]+"-"+sys.argv[1] + '.zip'
	# compare return diffdir
	diffdir = compare(srcdir,dstdir,outdir)
	# crypto
	# folderEncytp(diffdir+'/')
	# backup
	rm_dir(outdir+"-backup")
	os.mkdir(outdir+"-backup")
	copy_dir(outdir,outdir+"-backup")
	# zip
	# os.system("7z a -tzip -r -bb0 " + outzip + ' ' + diffdir)
	zip_file_dir(diffdir,outzip)

	os.system("rm -r " + diffdir+'/*')
	os.system("cp -f " + outzip +' ' + outdir)
	os.system("rm " + outzip)
	# listinfo
	list_dir(diffdir)
	

run()
#py cmp.py A B
#'''
