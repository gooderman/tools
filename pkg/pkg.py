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
	outlist=[]
	com_size = 0
	com_max = 1024*1024*8
	outfile_numb = 1
	filesplit = os.path.splitext(outfile)	
	compression = zipfile.ZIP_DEFLATED
	# start = path.rfind(os.sep) + 1 
	start = len(path) + 1
	print filesplit
	print '--------------------------------'
	filename = '%s-%03d%s'%(filesplit[0],outfile_numb,filesplit[1])
	z = zipfile.ZipFile(filename, mode="w", compression=compression)
	outlist.append(filename)
	print filename
	try:
		for dirpath, dirs, files in os.walk(path):
			z.write(dirpath, dirpath[start:])
			print dirpath[start:]
			for file in files:
				z_path = os.path.join(dirpath, file)
				z.write(z_path, z_path[start:])
				info = z.getinfo(z_path[start:])
				com_size += info.compress_size
				# print "zip write file ",z_path[start:],info.compress_size
				if(com_size>=com_max):
					com_size=0
					z.close()
					outfile_numb+=1
					print '--------------------------------'
					filename = '%s-%03d%s'%(filesplit[0],outfile_numb,filesplit[1])
					print filename
					z = zipfile.ZipFile(filename, mode="w", compression=compression)
					outlist.append(filename)
					z.write(dirpath, dirpath[start:])
					print dirpath[start:]
		# z.ZipInfo=info
		z.close()
	except:
		if z:
			z.close()
	return outlist

def run():
	if len(sys.argv)<4:
		print "please input dirPreVer,dirCurrVer,version"
		return
	srcdir = os.path.join(os.getcwd(),sys.argv[1])
	dstdir = os.path.join(os.getcwd(),sys.argv[2])
	outdir = os.path.join(os.getcwd(),sys.argv[2]+"-"+sys.argv[1])
	outzip = sys.argv[2]+"-"+sys.argv[1] + '.zip'
	curver = int(sys.argv[3])
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
	outlist = zip_file_dir(diffdir,outzip)
	os.system("rm -r " + diffdir+'/*')
	for f in outlist:
		os.system("cp -f " + f +' ' + outdir)
		os.system("rm " + f)
	# listinfo
	list_dir(diffdir,curver)
	

run()
#py cmp.py A B
#'''
