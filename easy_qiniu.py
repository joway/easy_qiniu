from qiniu import  Auth
from qiniu import put_file
from qiniu import BucketManager
from qiniu import build_batch_stat
from qiniu import build_batch_copy
from qiniu import build_batch_move
from qiniu import build_batch_delete
from qiniu import etag

import requests
import mimetypes


#class SevenCowException(Exception):
#    def __init__(self,status_code,content):
#        self.url = url
#        self.status_code = status_code
#        self.content = content
#        Exception.__init__(self, content)

class SevenCow(object):
    def __init__(self, access_key,secret_key):
        self.__access_key = access_key
        self.__secret_key = secret_key
        #使用access_key,secret_key登陆七牛，得到Auth类型返回值，以它作为后续操作凭证
        self.__auth = Auth(access_key, secret_key)

        

    # 上传本地文件(断点续上传、分块并行上传)
    def upload_files(self,bucket_name='',filedict={},
                     mime_type='',params={'x:a': 'a'}):
        """Args:
        bucket_name:'bucket_name'
        filedict: {'key':'localfile',...}
        mime_type: mime_type
        params: eg {'x:var': 'var'} 
        """

        """
        params用法:
        params={'x:price':'price','x:location':'location'}

        html文件中:
            <form method="post" action="http://upload.qiniu.com/" enctype="multipart/form-data">
                <input name="key" type="hidden" value="sunflower.jpg">
                <input name="x:location" type="hidden" value="Shanghai">
                <input name="x:price" type="hidden" value="1500.00">
                <input name="token" type="hidden" value="...">
                <input name="file" type="file" />
            </form>

        之后用户点击input按钮后，传给http://upload.qiniu.com的请求报文就会变成:

            name=sunflower.jpg&hash=Fn6qeQi4VDLQ347NiRm- \
            RlQx_4O2&location=Shanghai&price=1500.00

        然后七牛接受到后会将此作为回调请求的Body调用callbackUrl指定的回调服务器。
        """
        # 上传本地文件(断点续上传、分块并行上传)
        rets = []
        infos = []
        for key in filedict.keys():
            #上传策略仅指定空间名和上传后的文件名，其他参数为默认值
            token = self.__auth.upload_token(bucket_name, key)
            progress_handler = lambda progress, total: progress
            if(mime_type == ''):
                ret,info = put_file(token, key, filedict[key], params ,mime_type=mimetypes.guess_type(key)[0], progress_handler=progress_handler)
            else:
                ret,info = put_file(token, key, filedict[key], params ,mime_type=mime_type, progress_handler=progress_handler)
            #assert ret['key'] == key
            rets.append(ret)
            infos.append(info)
        return rets,infos


    def download_files(self,url='',filedict={}):
        """Args:
        url: 'url'
        filedict: {'key':'localfile',...}
        """
        if(url[0:4].upper() != 'HTTP'):
            url = 'http://' + url
        status_codes = []
        for fkey in filedict.keys():
            with open(filedict[fkey], "wb") as file:
                r = requests.get(url + '/' + fkey,timeout=5)
                status_codes.append(r.status_code)
                file.write(r.content)
        return status_codes


    # 获取文件信息
    def get_file_info(self,bucket_name,keys=[]):
        """Args:
        bucket_name:'bucket_name'
        keys:  ['fileName1','fileName2']
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_stat(bucket_name, keys)
        ret, info = bucket.batch(ops)
        return ret,info


    # 复制文件
    def copy_files(self,source_bucket,target_bucket,pathdict={}):
        """Args:
        source_bucket： 'source_bucket'
        target_bucket:  'target_bucket'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_copy(source_bucket, pathdict, target_bucket)
        ret, info = bucket.batch(ops)
        return ret,info


    # 移动文件
    def move_files(self,source_bucket,target_bucket,pathdict={}):
        """Args:
        source_bucket： 'source_bucket'
        target_bucket:  'target_bucket'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_move(source_bucket, pathdict, target_bucket)
        ret, info = bucket.batch(ops)
        return ret,info


    # 删除文件
    def delete_files(self,source_bucket,pathlist=[]):
        """Args:
        source_bucket： 'source_bucket'
        pathlist: ['source_file_name',...]
        """
        bucket = BucketManager(self.__auth)
        ops = build_batch_delete(source_bucket, pathlist)
        ret, info = bucket.batch(ops)
        return ret,info

    # 列出所有文件
    def list_file_names(self,bucket_name, prefix=None, marker=None, limit=None, delimiter=None):
        """
        Args:
            bucket:     空间名
            prefix:     列举前缀
            marker:     列举标识符(首次为None)
            limit:      单次列举个数限制(默认列举全部)
            delimiter:  指定目录分隔符
            
        Returns:
            pathlist: ['file_name',...]
        """
        file_name_list = []
        bucket = BucketManager(self.__auth)
        marker = None
        eof = False
        while eof is False:
            ret, eof, info = bucket.list(bucket_name, prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                file_name_list.append(item['key'])
        return file_name_list,eof

    # 抓取资源
    def fetch_files_from_net_to_qiniu(self,bucket_name,pathdict={}):
        """Args:
        bucket_name： 'bucket_name'
        pathdict: {'source_file_name':'target_file_name',...}
        """
        bucket = BucketManager(self.__auth)
        rets=[]
        infos=[]
        for p in pathdict.keys():
            ret, info = bucket.fetch(pathdict[p], bucket_name,p)
            rets.append(ret)
            infos.append(info)
        return rets,infos

    # 更新镜像资源
    def update_image_source(self,bucket_name,pathlist=[]):
        """Args:
        bucket_name： 'bucket_name'
        pathlist: ['file_name',...]
        !需要提前对仓库设置镜像源!
        """

        bucket = BucketManager(self.__auth)
        rets=[]
        infos=[]
        for p in pathlist:
            ret, info = bucket.prefetch(bucket_name, p)
            rets.append(ret)
            infos.append(info)
        return rets,infos