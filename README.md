# easy_qiniu

基于七牛官方API封装成 SevenCow 类，便于日常调用。

##Requirements

- Python 3
- qiniu
	- pip install qiniu
- requests
	- pip install requests 



##Usage

###1. upload_all_files_to_qiniu.py

- 在文件中修改 access_key、secret_key、bucket_name和director_path(本地文件夹(不设置默认为当前文件夹)）即可把所有文件上传至对应七牛仓库。




### 2. easy_qiniu.py ：SevenCow 类

	#登陆
	sc = SevenCow(access_key,secret_key)
	
	#上传
	sc.upload_files(bucket_name,filedict)
	
	#下载
	sc.download_files(bucket_url,filedict)
	
	#获取文件信息
	sc.get_file_info(bucket_name,filelist)

	
	#复制
	sc.copy_files(source_bucket,target_bucket,pathdict)
	
	#移动
	sc.move_files(source_bucket,target_bucket,pathdict)
	
	#删除
	sc.delete_files(bucket_name,filelist)
	
	#列出
	sc.list_file_names(bucket_name)
	
	#获取网络文件至七牛
	sc.fetch_files_from_net_to_qiniu(bucket_name,net_pathdict)
	
	#更新镜像
	sc.update_image_source(bucket_name,pathlist)


	#参数样例:
	
	access_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	secret_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
	bucket_name = 'test'
	bucket_url = '7xlgp1.com1.z0.glb.clouddn.com'
	filedict = {'1.jpg':'D://1.jpg'}
	filelist = ['1.jpg']
	source_bucket = 'images'
	target_bucket = 'test'
	pathdict = {'1.jpg':'path.jpg'}
	pathlist = ['1.jpg']
	net_pathdict = {'00000.jpg':'http://ww4.sinaimg.cn/bmiddle/708485bfgw1evlyks7y41j20ic5607wh.jpg'}
