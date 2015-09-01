import unittest

from easy_qiniu import SevenCow


access_key = 'M4uDxjD_Nxm38V1s_eTl2MeMNY0D0XwNIb7eLwln'
secret_key = 'PE1B4vcQ3fgvJsMkYBt_XHfj5F1efgcBNgGMr5IV'
bucket_name = 'test'
bucket_url = '7xlgp1.com1.z0.glb.clouddn.com'
mime_type = 'image/jpeg'
filedict = {'1.jpg':'D://1.jpg'}
filelist = ['1.jpg']
source_bucket = 'images'
target_bucket = 'test'
pathdict = {'1.jpg':'path.jpg'}
pathlist = ['1.jpg']
net_pathdict = {'00000.jpg':'http://ww4.sinaimg.cn/bmiddle/708485bfgw1evlyks7y41j20ic5607wh.jpg'}

class TestSevenCow(unittest.TestCase):

    def setUp(self):
        self.sc = SevenCow(access_key,secret_key)

    def test_init(self):
        self.assertTrue(isinstance(self.sc, SevenCow))

    #def test_upload_files(self):
    #    rets,infos = self.sc.upload_files(bucket_name,filedict)
    #    count = 0
    #    for ret in rets:
    #        self.assertEqual(ret['key'],list(filedict.keys())[count])
    #        count+=1

    #def test_download_files(self):
    #    status_codes = self.sc.download_files(bucket_url,filedict)
    #    count = 0
    #    for status_code in status_codes:
    #        self.assertEqual(status_code,200)
    #        count+=1

    #def test_get_file_info(self):
    #    rets,infos = self.sc.get_file_info(bucket_name,filelist)
    #    for ret in rets:
    #        self.assertEqual(ret['code'],200)

    #def test_copy_files(self):
    #    rets,infos = self.sc.copy_files(source_bucket,target_bucket,pathdict)
    #    self.assertEqual(infos.status_code,200)


    #def test_move_files(self):
    #    rets,infos = self.sc.move_files(source_bucket,target_bucket,pathdict)
    #    self.assertEqual(infos.status_code,200)


    #def test_delete_files(self):
    #    rets,infos = self.sc.delete_files(bucket_name,filelist)
    #    self.assertEqual(infos.status_code,200)
    #    print(infos)


    #def test_list_file_names(self):
    #    file_name_list,eof = self.sc.list_file_names(bucket_name)
    #    self.assertTrue(eof)
    #    for i in file_name_list:
    #        print(i)

    #def test_fetch_files_from_net_to_qiniu(self):
    #    rets,infos =
    #    self.sc.fetch_files_from_net_to_qiniu(bucket_name,net_pathdict)
    #    for info in infos:
    #        self.assertEqual(info.status_code,200)

    def test_update_image_source(self):
        rets,infos = self.sc.update_image_source(bucket_name,pathlist)
        for info in infos:
            self.assertEqual(info.status_code,200)

    #def test_move_files()
if __name__ == '__main__':
    unittest.main()