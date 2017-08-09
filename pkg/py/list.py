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
def zip_file_dir(path, outfile):
	compression = zipfile.ZIP_DEFLATED
	start = path.rfind(os.sep) + 1
	z = zipfile.ZipFile(outfile, mode="w", compression=compression)
	try:
		z.write(path, path[start:])
		z.close()
	except:
		if z:
			z.close()
#print "sys.arg ",len(sys.argv)
def md5_file(name):
    m = md5()
    a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

def is_cmp(infile,end):
	return re.match(".+"+end+"$",infile)

def copy_dir(src,dst):
	cmd = "cp -r -f "+src + "/*	"+ dst
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

def list_file(srcdir):
	alldir=[]
	allfile=[]
	plen=len(srcdir)
	for parent,dirnames,filenames in os.walk(srcdir):
		for dirname in dirnames:
			srcpath = os.path.join(parent,dirname)
			alldir.append(srcpath[plen+1:len(srcpath)])
		for filename in filenames:
			srcpath = os.path.join(parent,filename)
			tp=(srcpath[plen+1:len(srcpath)],md5_file(srcpath),int(os.path.getsize(srcpath)))
			allfile.append(tp)
			#print(srcpath)
			#print(dstpath)
	#print("dirs: ",alldir)
	#print("file: ",allfile)
	return alldir,allfile

def filter_file(srcdir,endlist):
	for parent,dirnames,filenames in os.walk(srcdir):
		for filename in filenames:
			srcpath = parent+"/"+filename
			for end in endlist:
				if re.match(".+"+end+"$",srcpath):
					os.remove(srcpath)

def rm_dir(dir):
	if os.path.isdir(dir):
		print "remove ",dir
		os.system("rm /-r "+dir)
def rm_file(f):
	if os.path.isfile(f):
		os.remove(f)

def stringlize_json(dirlist,filelist):
	# buf = "--dirct=" + str(len(dirlist)) + "\n"
	# buf = buf + "--filect=" + str(len(filelist)) + "\n"
	buf = ""
	buf = buf + "{\n" 
	buf = buf + "\t\"appdir\":\"" + (appdir) + "\",\n"
	buf = buf + "\t\"appname\":\"" + (appname) + "\",\n"
	buf = buf + "\t\"appver\":\"" + (appver) + "\",\n" 
	buf = buf + "\t\"mainver\":" + str(mainver) + ",\n" 
	buf = buf + "\t\"version\":" + str(version) + ",\n" 
	buf = buf + "\t\"dirs\":[\n"
	delim = ""
	for dname in dirlist:
		item='\t\t"%s"'%(dname)
		buf=buf+delim+item
		delim=",\n"
	buf = buf+"\n\t],\n"

	buf = buf+"\t\"files\":[\n"
	delim = ""
	for tp in filelist:
		nm = tp[0]
		md = tp[1]
		sz = tp[2]
		item='\t\t["%s","%s",%d,%d]'%(nm,md,sz,version)
		buf = buf+delim+item
		delim=",\n"
	buf = buf+"\n\t]\n"
	buf = buf+"}\n\n"
	buf=re.sub(r'\\',r'/',buf)
	return buf

def stringlize(dirlist,filelist):
	buf = "--dirct=" + str(len(dirlist)) + "\n"
	buf = buf + "--filect=" + str(len(filelist)) + "\n"
	buf = buf + "local list = {\n" 
	buf = buf + "\tappdir = \"" + (appdir) + "\",\n"
	buf = buf + "\tappname = \"" + (appname) + "\",\n"
	buf = buf + "\tappver = \"" + (appver) + "\",\n" 
	buf = buf + "\tmainver = " + str(mainver) + "\",\n" 
	buf = buf + "\tversion = " + str(version) + ",\n" 
	buf = buf + "\tdirs = {\n"
	for dname in dirlist:
		item='\t\t"%s",\n'%(dname)
		buf=buf+item
	buf = buf+"\t},\n"

	buf = buf+"\tfiles = {\n"
	for tp in filelist:
		nm = tp[0]
		md = tp[1]
		sz = tp[2]
		item='\t\t{"%s","%s",%d,%d},\n'%(nm,md,sz,version)
		buf = buf+item
	buf = buf+"\t},\n" 
	buf = buf+"}\n\n" 
	buf = buf+"return list"
	buf=re.sub(r'\\',r'/',buf)
	return buf

def list_dir(srcdir,__mainver,__version):
	global appdir
	global appname
	global appver
	global mainver
	global version
	appdir="ddz"
	appname="ddz"
	appver="1.0"
	mainver = __mainver
	version = __version
	os.system("echo off")
	filter_file(srcdir,['.db','.svn','.git','.DS_Store'])	
	dirlist,filelist = list_file(srcdir)
	# buff = stringlize(dirlist,filelist)
	buff = stringlize_json(dirlist,filelist)
	print buff
	# outfile = os.getcwd()+"/"+"flist.txt"
	outfile = srcdir+"/"+"flist.data"
	fd = open(outfile,'wb+')
	fd.write(buff)
	fd.close()
	# os.system("7z a -tzip -r -bb0 flist.zip " + outfile)
	zip_file_dir(outfile,"flist.zip")
	os.system("cp flist.zip " + srcdir)
	os.system("rm flist.zip")
	
	

def run():
	global appdir
	global appname
	global appver
	global resver
	global resvercode
	appdir="pdk"
	appname="pdk"
	appver="1.0"
	resver="1.0.0"
	resvercode=100
	os.system("echo off")
	if len(sys.argv)<2:
		print "please input dir"
		return
	srcdir = os.getcwd()+"/"+sys.argv[1]
	list_info(srcdir)
	
#run()
#py cmp.py A B
#'''
