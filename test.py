from easy_qiniu import *


access_key='xxx'
secret_key='xxx'
bucket_name='test'
mime_type='image/jpeg'

#登陆
session = login_qiniu(access_key,secret_key)

#上传
upload_files(session,bucket_name,{'1.jpg':'d://1.jpg'},mime_type)

#下载
download_files('7xlgp1.com1.z0.glb.clouddn.com',{'1.jpg':'C://1.jpg'})

#获取文件信息
info = get_file_info(session,bucket_name,['1.jpg'])
print(info)

#复制
copy_files(session,bucket_name,bucket_name,pathdict={'1.jpg':'copy.jpg'})

#移动
move_files(session,bucket_name,bucket_name,pathdict={'1.jpg':'move.jpg'})

#删除
delete_files(session,bucket_name,['move.jpg'])

#列出
list = list_file_names(session,bucket_name)
print(list)

#Success
print('Successful!')