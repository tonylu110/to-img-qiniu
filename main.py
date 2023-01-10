import os
from datetime import datetime

from qiniu import Auth, put_file, etag


def search_pic(localdir):
    for dir_path, _, files_list in os.walk(localdir):
        for file in files_list:
            if file.split(".")[-1] in ["jpg", "JPG", "png", "PNG", "jpeg", "JPEG"]:
                yield os.path.join(dir_path, file)


def upload_pic(q, file_name):
    base_url = "your base url"
    bucket_name = 'your bucket name'
    key = datetime.now().strftime("%Y%m%d%H%M%S%f") + "." + file_name.split(".")[-1]
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_file(token, key, file_name, version='v2')
    try:
        assert ret['key'] == key
        assert ret['hash'] == etag(file_name)
        print(os.path.join(base_url, key))
    except:
        print(file_name + "----error----")


if __name__ == '__main__':
    access_key = 'your access key'
    secret_key = 'your secret key'
    q = Auth(access_key, secret_key)
    # 需要批量上传图片的文件夹的本地路径
    localdir = './img/mp'
    files = search_pic(localdir)
    for file in files:
        upload_pic(q, file)
