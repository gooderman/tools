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
from hashlib import md5
#print "sys.arg ",len(sys.argv)
has_error=False
def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

def is_cmp(infile,end):
	return re.match(".+"+end+"$",infile)

def copy_dir(src,dst):
    cmd = "cp -f -r "+src + "/*	"+ dst
    print cmd
    os.system(cmd)

def cmp_file_md5(src,dst):
	rm = False
	if os.path.isfile(src) and os.path.isfile(dst):
		if md5_file(src)==md5_file(dst):
			rm = True
	if rm:
		os.remove(dst)		
		return True
	return False

def is_empty(dstdir):
	for parent,dirnames,filenames in os.walk(dstdir):
		# print "is_empty__++:",dstdir,len(filenames)
		if len(filenames)>0 :
			return False
		for dirname in dirnames:
			if False==is_empty(os.path.join(parent,dirname)):
				return False		
	return True

def rm_dir(dir):
    if os.path.isdir(dir):
		print "remove ",dir
		os.system("rm -r "+dir)

def cmp_file(srcdir,dstdir):
	prefix = srcdir
	plen = len(srcdir)
	allfile = 0
	rmfile = 0
	for parent,dirnames,filenames in os.walk(srcdir):
		for filename in filenames:
			srcpath = os.path.join(parent,filename)
			dstpath = dstdir+srcpath[plen:len(srcpath)]
			#print(srcpath)
			#print(dstpath)
			allfile=allfile+1
			if cmp_file_md5(srcpath,dstpath):
				rmfile=rmfile+1
	print("srcfile: ",allfile)
	print("samfile: ",rmfile)
	#############################
	allemptydir=[]
	for parent,dirnames,filenames in os.walk(dstdir):	
		for dirname in dirnames:
			ppp=os.path.join(parent,dirname)
			flag = is_empty(ppp)
			if flag :
				allemptydir.append(ppp)
	print "empty dir :",len(allemptydir)
	for rmdir in allemptydir:
		rm_dir(rmdir)
	#############################
	allfile=0
	for parent,dirnames,filenames in os.walk(dstdir):
		for filename in filenames:
			allfile=allfile+1
	print("outfile: ",allfile)
	return allfile

def filter_file(srcdir,endlist):
	for parent,dirnames,filenames in os.walk(srcdir):
		for filename in filenames:
			srcpath = os.path.join(parent,filename)
			for end in endlist:
				if re.match(".+"+end+"$",srcpath):
					os.remove(srcpath)

def compare(srcdir,dstdir,outdir):
	os.system("echo off")
	rm_dir(outdir)
	os.mkdir(outdir)
	copy_dir(dstdir,outdir)
	filter_file(outdir,['.db','.svn','.git','.DS_Store'])
	diffs = cmp_file(srcdir,outdir)
	# if diffs>0:
	# 	print "zip diff"
	# 	if os.path.isfile("diff.zip"):
	# 		os.remove("diff.zip")
	# 	os.system("7z a -tzip -r -bb0 diff.zip " + outdir +"/*.*")
	# 	#os.system("7z l diff.zip")
	# 	print "zip diff File : diff.zip"
	# else:
	# 	print "no diff File"
	return outdir

def run():
	os.system("echo off")
	if len(sys.argv)<3:
		print "please input a,b dir"
		return
	srcdir = os.path.join(os.getcwd(),sys.argv[1])
	dstdir = os.path.join(os.getcwd(),sys.argv[2])
	outdir = os.path.join(os.getcwd(),sys.argv[2]+"-"+sys.argv[1])
	compare(srcdir,dstdir,outdir)
	return outdir

#run()
#py cmp.py A B
#'''
