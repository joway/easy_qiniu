import os
import sys
from easy_qiniu import SevenCow

#可获取文件夹内全部文件名(包括子文件夹)
def get_all_files(DirectoryPath):
    filenamesList = []
    for dirpath, dirnames, filenames in os.walk(DirectoryPath):
        """
        dirpath：当前遍历文件夹全名
        dirnames：当前文件夹内子文件夹名
        filenames：当前文件夹下文件名列表(不包括子文件夹里的文件)
        """
        for filename in filenames:
            filenamesList.append(dirpath + '/' + filename)#全名
    return filenamesList


#生成网站根目录形式的文件名
def get_root_filename(fullname):
    dir_path = sys.path[0]
    return fullname[len(sys.path[0]) + 1:len(fullname)].replace('\\','/')

#生成{目标文件名:源文件名,...}形式的字典
def get_filenames_dict(filenamesList=[]):
    filenames_dict = {}
    for filename in filenamesList:
        filenames_dict[get_root_filename(filename)] = filename
    return filenames_dict

#上传，根据返回值判断是否成功
def upload_into_qiniu(access_key,secret_key,bucket_name,director_path=sys.path[0]):
    try:
        sc = SevenCow(access_key,secret_key)
        sc.delete_files(bucket_name,sc.list_file_names(bucket_name)[0])
        sc.upload_files(bucket_name,get_filenames_dict(get_all_files(director_path)))
    except:
        return False
    else:
        return True

access_key = ''
secret_key = ''
bucket_name = 'conoha'
if(upload_into_qiniu(access_key,secret_key,bucket_name)):
    print('Bak Successful')
else:
    print('Bak Error')
