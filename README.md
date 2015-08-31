# easy_qiniu

基于七牛官方API封装成一些简单的函数，便于日常调用。

##Requirements

- Python 3
- qiniu
	- pip install qiniu
- requests



##Usage

- **upload_all_files_to_qiniu.py**

	-    指定access_key、secret_key、bucket_name和director_path(本地文件夹）即可把所有文件上传至对应七牛仓库。(默认文件夹为当前目录)


##easy_qiniu.py API

### 使用access_key,secret_key登陆七牛，得到Auth类型返回值，以它作为后续操作凭证

	login_qiniu(access_key,secret_key)

### 上传本地文件(断点续上传、分块并行上传)
    """Args:
    session: Auth
    bucket_name:'bucket_name'
    files: {'key':'localfile',...}
    mime_type: mime_type
    params: eg {'x:a': 'a'}
    """

	upload_files(session,bucket_name='',files={},
	                 mime_type = "text/plain",params = {'x:a': 'a'}
	):

### 下载文件

    """Args:
    url: url
    files: {'key':'localfile',...}
    """

	download_files(url='',files={}):

### 获取文件信息
    """Args:
    keys:  ['fileName1','fileName2']
    """

	get_file_info(session,bucket_name,keys=[]):

### 复制文件

    """Args:
    pathdict: {'source_file_name':'target_file_name',...}
    """

	copy_files(session,source_bucket,target_bucket,pathdict={}):

### 移动文件

    """Args:
    pathdict: {'source_file_name':'target_file_name',...}
    """

	move_files(session,source_bucket,target_bucket,pathdict={}):

### 删除文件

    """Args:
    pathlist: ['source_file_name',...]
    """

	delete_files(session,source_bucket,pathlist=[]):

### 列出所有文件

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

	list_file_names(session,bucket_name, prefix=None, marker=None, limit=None, delimiter=None):

