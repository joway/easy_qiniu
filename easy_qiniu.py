from qiniu import  Auth
from qiniu import put_file
from qiniu import BucketManager
from qiniu import build_batch_stat
from qiniu import build_batch_copy
from qiniu import build_batch_move
from qiniu import build_batch_delete

import requests
import mimetypes


#使用access_key,secret_key登陆七牛，得到Auth类型返回值，以它作为后续操作凭证
def login_qiniu(access_key,secret_key):
    return Auth(access_key, secret_key)

def get_mimetype(filename):
    return mimetypes.guess_type(filename)[0]

# 上传本地文件(断点续上传、分块并行上传)
def upload_files(session,bucket_name='',files={},
                 mime_type='',params = {'x:a': 'a'}
):
    """Args:
    session: Auth
    bucket_name:'bucket_name'
    files: {'key':'localfile',...}
    mime_type: mime_type
    params: eg {'x:a': 'a'}
    """
    # 上传本地文件(断点续上传、分块并行上传)
    for key in files.keys():
        #上传策略仅指定空间名和上传后的文件名，其他参数为默认值
        token = session.upload_token(bucket_name, key)
        progress_handler = lambda progress, total: progress
        if(mime_type==''):
            ret,info= put_file(token, key, files[key], params ,mime_type=get_mimetype(key), progress_handler=progress_handler)
        else:
            ret,info= put_file(token, key, files[key], params ,mime_type=mime_type, progress_handler=progress_handler)
        assert ret['key'] == key



def download_files(url='',files={}):
    """Args:
    url: url
    files: {'key':'localfile',...}
    """
    if(url[0:4].upper()!='HTTP'):
        url='http://'+url
    for fkey in files.keys():
        with open(files[fkey], "wb") as file:
            r = requests.get(url+'/'+fkey,timeout=5)
            assert r.status_code==200
            file.write(r.content)


# 获取文件信息
def get_file_info(session,bucket_name,keys=[]):
    """Args:
    keys:  ['fileName1','fileName2']
    """
    bucket = BucketManager(session)
    ops = build_batch_stat(bucket_name, keys)
    ret, info = bucket.batch(ops)
    if(ret!=None):
        for i in ret:
            assert i['code'] == 200
    return info

# 复制文件
def copy_files(session,source_bucket,target_bucket,pathdict={}):
    """Args:
    pathdict: {'source_file_name':'target_file_name',...}
    """
    bucket = BucketManager(session)
    ops = build_batch_copy(source_bucket, pathdict, target_bucket)
    ret, info = bucket.batch(ops)
    if(ret!=None):
        for i in ret:
            assert i['code'] == 200
    return info


# 移动文件
def move_files(session,source_bucket,target_bucket,pathdict={}):
    """Args:
    pathdict: {'source_file_name':'target_file_name',...}
    """
    bucket = BucketManager(session)
    ops = build_batch_move(source_bucket, pathdict, target_bucket)
    ret, info = bucket.batch(ops)
    if(ret!=None):
        for i in ret:
            assert i['code'] == 200
    return info


# 删除文件
def delete_files(session,source_bucket,pathlist=[]):
    """Args:
    pathlist: ['source_file_name',...]
    """
    bucket = BucketManager(session)
    ops = build_batch_delete(source_bucket, pathlist)
    ret, info = bucket.batch(ops)
    if(ret!=None):
        for i in ret:
            assert i['code'] == 200
    return info

# 列出所有文件
def list_file_names(session,bucket_name, prefix=None, marker=None, limit=None, delimiter=None):
    """
    Args:
        session：   session
        bucket:     空间名
        prefix:     列举前缀
        marker:     列举标识符(首次为None)
        limit:      单次列举个数限制(默认列举全部)
        delimiter:  指定目录分隔符
            
    Returns:
        pathlist: ['file_name',...]
    """
    file_name_list=[]
    bucket = BucketManager(session)
    marker = None
    eof = False
    while eof is False:
        ret, eof, info = bucket.list(bucket_name, prefix=prefix, marker=marker, limit=limit)
        marker = ret.get('marker', None)
        for item in ret['items']:
            file_name_list.append(item['key'])
    assert eof is True
    return file_name_list