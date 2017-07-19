// ts_encytp_console.cpp : 定义控制台应用程序的入口点。
//
#include "stdafx.h"

#include "stdio.h"
#include <windows.h>
#include <iostream>
#include <fstream>
#include <time.h>
#include <math.h>
#include <direct.h>  


#define LOBYTE(w)           ((unsigned char)(w))
#define HIBYTE(w)           ((unsigned char)(((unsigned short)(w) >> 8) & 0xFF))
#define MAKEWORD(hi, lo)    (((unsigned short)((unsigned char)(hi))<<8) + (unsigned short)((unsigned char)(lo)))
#define LOWORD(dw)          ((unsigned short)(dw))
#define HIWORD(dw)          ((unsigned short)(((unsigned int)(dw) >> 16) & 0xFFFF))
#define MAKELONG(hi, lo)    (((unsigned int)((unsigned short)(hi))<<16) + (unsigned int)((unsigned short)(lo)))


/* 下面的宏用于解决奇地址读写出错的问题 */
/* 得到一个16的数 */
#define READ_WORD(ptr)          MAKEWORD((*(unsigned char*)(ptr)), (*((unsigned char*)(ptr)+1)))
/* 向某地址中写入一个16的数 */
#define WRITE_WORD(ptr, w)      do{ *(unsigned char*)(ptr) = LOBYTE(w); \
                                    *((unsigned char*)(ptr)+1) = HIBYTE(w); }while(0)

/* 得到一个32的数 */
#define READ_DWORD(ptr)         MAKELONG(READ_WORD((unsigned char*)(ptr)), \
                                          READ_WORD(((unsigned char*)(ptr)+2)))
/* 向某地址中写入一个32的数 */
#define WRITE_DWORD(ptr, dw)    do{ WRITE_WORD((ptr), LOWORD(dw));  \
                                    WRITE_WORD((unsigned char*)(ptr)+2, HIWORD(dw)); }while(0)
static unsigned char XOR_BUFFER[]=
{
	0x9d,0xF3,0x00,0x25,0xef,0x02,0x77,
	0xfd,0xe3,0x39,0xcd,0x02,0x98,0x67,
	0x25,0xDC,0x10,0x95,0x68,0x69,0x49,
	0x56,0x75,0x20,0x85,0x39,0x99,0xDF,
	0xF6,0x7E,0x70,0x95,0xe8,0xCC,0xEF,
	0x40,0x79,0x99,0xd1,0xae,0x76,0x9F,
};
static unsigned char XOR_END[]=
{
	0x39,0xcd,0x02,0x98,0x67,0x25
};
static char* XOR_KEY = "XYTEA";

static unsigned char XOR_BUFFER_GEN[42];

static void gen_key(const char*shorname,unsigned char** ppKEY,unsigned int *keylen)
{
	int xorlen = sizeof(XOR_BUFFER)/sizeof(unsigned char);
	unsigned char*newKey = XOR_BUFFER_GEN;
	//unsigned char*newKey = (unsigned char*)malloc(xorlen);
	memcpy(newKey,XOR_BUFFER,xorlen);
	int buffsize = strlen(shorname);
	unsigned char* buff = (unsigned char* )shorname;
	for(int i=0;i<buffsize;i++)
	{
		if(shorname[i]=='_' && i!=buffsize-1)
		{
			buffsize = strlen(shorname+i+1);
			buff = (unsigned char* )(shorname+i+1);
			break;
		}
	}
	for(int i=0;i<xorlen && i<buffsize;i++)
	{
		newKey[i] = XOR_BUFFER[i]^(buff[i%buffsize]);
	}
	for(int i=xorlen-1,j=0;i>=0 && j<buffsize;i--,j++)
	{
		newKey[i] = XOR_BUFFER[i]^(buff[j%buffsize]);
	}
	* ppKEY = newKey;
	* keylen = xorlen;
}

static void xor_memory__(unsigned char* buff,unsigned int buffsize,unsigned char*KEY,int KEYLEN)
{
	int xorlen = KEYLEN;
	for(int i=0;i<buffsize;i++)
	{
		buff[i] = buff[i]^KEY[i%xorlen];
	}
}

static void xor_memory(unsigned char* buff,unsigned int buffsize,const char*shorname)
{
//	int xorlen = sizeof(XOR_BUFFER)/sizeof(unsigned char);
//	xor_memory__(buff,buffsize,XOR_BUFFER,xorlen);
	unsigned char*key = 0;
	unsigned int keylen = 0;
	gen_key(shorname,&key,&keylen);
	xor_memory__(buff,buffsize,key,keylen);
}

static void xor_memory_end(unsigned char* buff,unsigned int buffsize)
{
	int xorlen = sizeof(XOR_END)/sizeof(unsigned char);
	for(int i=0;i<buffsize;i++)
	{
		buff[i] = buff[i]^XOR_END[i%xorlen];
	}
}

static int encypt_file(const char*name,const char*shorname)
{
	FILE* find_file;
	//fopen_s(&find_file,name,"w+b");	
	find_file = fopen(name,"r+b");	
	if(find_file==NULL)
	{
		printf("file: %s encypt false\n", shorname);
		return -1;
	}
	fseek(find_file, 0, SEEK_SET);
	fseek(find_file, 0, SEEK_END);
	unsigned long filesize = ftell(find_file);		
	fseek(find_file, 0, SEEK_SET);
	unsigned char *p_tmp= (unsigned char *)malloc(filesize);
	fread(p_tmp,1,filesize,find_file);	
	fseek(find_file, 0, SEEK_SET);

	
	unsigned char PEND[20];

	int lena = strlen(XOR_KEY);
	int lenb = strlen(shorname);
	if(lena+lenb>20) lenb = 20-lena;	
	int lennn = lena+lenb;

	

	unsigned char *p_end= PEND;
	memset(p_end,0x00,lennn);
	memcpy(p_end,XOR_KEY,lena);
	memcpy(p_end+lena,shorname,lenb);
	xor_memory_end(p_end,lennn);
	//判断如果已经有加密不处理
	int ready = 1;
	for(int i=1;i<=lennn;i++)
	{
		if(p_end[lennn-i]!=p_tmp[filesize-i])
		{
			ready = 0;
			break;
		}
	}	
	if(ready==0)
	{
		xor_memory(p_tmp,filesize,shorname);
		fwrite(p_tmp,1,filesize,find_file);
		fwrite(p_end,1,lennn,find_file);
		fflush(find_file);
	}
	fclose(find_file);
	free(p_tmp);
	printf("file: %s encypt succ\n", shorname);
	return 1;
}
static int dencypt_file(const char*name,const char*shorname)
{	
	FILE* find_file;
	//find_file=fopen(name,"w+b");	
	fopen_s(&find_file,name,"r+b");	
	if(find_file==NULL)
	{
		printf("file: %s deencypt false\n", shorname);
		return -1;
	}
	fseek(find_file, 0, SEEK_END);
	unsigned long filesize = ftell(find_file);
	fseek(find_file, 0, SEEK_SET);
	unsigned char *p_tmp= (unsigned char *)malloc(filesize);
	fread(p_tmp,1,filesize,find_file);	
	fseek(find_file, 0, SEEK_SET);

	unsigned char PEND[20];
	int lena = strlen(XOR_KEY);
	int lenb = strlen(shorname);
	if(lena+lenb>20) lenb = 20-lena;	
	int lennn = lena+lenb;	

	unsigned char *p_end= PEND;
	memset(p_end,0x00,lennn);
	memcpy(p_end,XOR_KEY,lena);
	memcpy(p_end+lena,shorname,lenb);
	xor_memory_end(p_end,lennn);
	//判断如果已经有加密不处理
	for(int i=1;i<=lennn;i++)
	{
		if(p_end[lennn-i]!=p_tmp[filesize-i])
		{
			fclose(find_file);
			free(p_tmp);
			return 0;
		}
	}
	fclose(find_file);
	fopen_s(&find_file,name,"w+b");	
	xor_memory(p_tmp,filesize-lennn,shorname);
	fwrite(p_tmp,1,filesize-lennn,find_file);
	//find_file.SetLength(filesize-lennn);
	fclose(find_file);
	free(p_tmp);
	printf("file: %s deencypt succ\n", shorname);
	return 1;
}
struct PNG_INFO
{	
	char a;
	char b;
	char c;
	char d;
	unsigned char*data;
	unsigned int datasz;
	unsigned int crc32;
	unsigned int cksize;
};
static PNG_INFO get_png_chuck(unsigned char*buff,int skip)
{
	PNG_INFO info;
	info.datasz = READ_DWORD(buff);
	info.data = (buff+8);
	info.crc32 = READ_DWORD(buff+8+info.datasz);
	info.a = (char)(*(buff+4));
	info.b = (char)(*(buff+5));
	info.c = (char)(*(buff+6));
	info.d = (char)(*(buff+7));
	info.cksize = info.datasz + 12;
	return info;
}
static int encypt_file_png(const char*name,const char*shorname)
{
	FILE* find_file;
	//fopen_s(&find_file,name,"w+b");	
	find_file = fopen(name,"r+b");	
	if(find_file==NULL)
	{
		return -1;
	}
	fseek(find_file, 0, SEEK_SET);
	fseek(find_file, 0, SEEK_END);
	unsigned long filesize = ftell(find_file);		
	fseek(find_file, 0, SEEK_SET);
	unsigned char *p_tmp= (unsigned char *)malloc(filesize);
	fread(p_tmp,1,filesize,find_file);	
	fseek(find_file, 0, SEEK_SET);
    fclose(find_file);
	unsigned char* pHead = (unsigned char*)p_tmp;
    if (   pHead[0] == 0x89
        && pHead[1] == 0x50
        && pHead[2] == 0x4E
        && pHead[3] == 0x47
        && pHead[4] == 0x0D
        && pHead[5] == 0x0A
        && pHead[6] == 0x1A
        && pHead[7] == 0x0A)
    {
		pHead = pHead+8;
		unsigned long skip = 8;
		int id=1;
		while(skip<filesize)
		{
			PNG_INFO info = get_png_chuck(pHead,0);
			pHead = pHead + info.cksize;
			skip = skip + info.cksize;			
			//printf("==%d==--%c%c%c%c--%d\n",id,info.a,info.b,info.c,info.d,info.datasz);
			id = id + 1;
			if(info.a=='P' && info.b=='L' &&info.c=='T' &&info.d=='E')
			{
				xor_memory(info.data,info.datasz,shorname);
			}
			if(info.a=='I' && info.b=='D' &&info.c=='A' &&info.d=='T')
			{
				if(info.datasz<39)
				{
					xor_memory(info.data,info.datasz,shorname);
				}
				else
				{
					xor_memory(info.data,39,shorname);
				}
				break;
			}			
		}
    }
	else
	{
		free(p_tmp);
		return 0;
	}
	find_file = fopen(name,"w+b");	
	if(find_file==NULL)
	{
		return -1;
	}
	fseek(find_file, 0, SEEK_SET);
	unsigned char flag[4]={0x99,0x46,0xB8,0x0D};
	fwrite(flag,1,4,find_file);	
	fwrite(p_tmp,1,filesize,find_file);	
    fclose(find_file);
	free(p_tmp);

	printf("file: %s encypt_png succ\n", shorname);
	
	return 1;
}

static int deencypt_file_png(const char*name,const char*shorname)
{
	FILE* find_file;
	//fopen_s(&find_file,name,"w+b");	
	find_file = fopen(name,"r+b");	
	if(find_file==NULL)
	{
		return -1;
	}
	fseek(find_file, 0, SEEK_SET);
	fseek(find_file, 0, SEEK_END);
	unsigned long filesize = ftell(find_file);		
	fseek(find_file, 0, SEEK_SET);
	unsigned char *p_tmp= (unsigned char *)malloc(filesize);
	fread(p_tmp,1,filesize,find_file);	
	fseek(find_file, 0, SEEK_SET);
    fclose(find_file);
	//fwrite("\0x99\0x46\0xB8\0x0D",1,4,find_file);
	if(filesize<12)
	{
		return 0;
	}
	unsigned char* pHead = (unsigned char*)p_tmp;
    if (
		pHead[0] == 0x99
        && pHead[1] == 0x46
        && pHead[2] == 0xB8
        && pHead[3] == 0x0D

		&& pHead[4] == 0x89
        && pHead[5] == 0x50
        && pHead[6] == 0x4E
        && pHead[7] == 0x47
        && pHead[8] == 0x0D
        && pHead[9] == 0x0A
        && pHead[10] == 0x1A
        && pHead[11] == 0x0A)
    {
		pHead = pHead+12;
		unsigned long skip = 8;
		int id=1;
		while(skip<filesize)
		{
			PNG_INFO info = get_png_chuck(pHead,0);
			pHead = pHead + info.cksize;
			skip = skip + info.cksize;			
			//printf("==%d==--%c%c%c%c--%d\n",id,info.a,info.b,info.c,info.d,info.datasz);
			id = id + 1;
			if(info.a=='P' && info.b=='L' &&info.c=='T' &&info.d=='E')
			{
				xor_memory(info.data,info.datasz,shorname);
			}
			if(info.a=='I' && info.b=='D' &&info.c=='A' &&info.d=='T')
			{
				if(info.datasz<39)
				{
					xor_memory(info.data,info.datasz,shorname);
				}
				else
				{
					xor_memory(info.data,39,shorname);
				}
				break;
			}			
		}

    }
	else
	{
		free(p_tmp);
		return 0;
	}

	find_file = fopen(name,"w+b");	
	if(find_file==NULL)
	{
		return -1;
	}
	fseek(find_file, 0, SEEK_SET);
	fwrite(p_tmp+4,1,filesize-4,find_file);	
    fclose(find_file);
	free(p_tmp);

	printf("file: %s deencypt_png succ\n", shorname);

	
	return 1;
}

//argv[0]:folderPath argv[1]:fileName argv[2]:isEncyp
int _tmain(int argc, _TCHAR* argv[])
{	
	if(argc < 3)return 0;

	bool isEncyp = atoi(argv[3]);
	std::string folderPath = argv[1];
	std::string fileName = argv[2];
	std::string filePath = folderPath;
				filePath += "\\";
				filePath += fileName;
				
	if (isEncyp)
	{
		encypt_file_png(filePath.c_str(),fileName.c_str());
		encypt_file(filePath.c_str(),fileName.c_str());

		//encypt_file_png("E:/SVN/ET/code/client/出包工具/res/PLOT/talk_hero1002.png","talk_hero1002.png");
	} else
	{
		dencypt_file(filePath.c_str(),fileName.c_str());
		deencypt_file_png(filePath.c_str(),fileName.c_str());
		//deencypt_file_png("E:/SVN/ET/code/client/出包工具/res/PLOT/talk_hero1002.png","talk_hero1002.png");
	}
	return 0;
}

