# _*_ coding:utf-8 _*_
__author__ = 'Sheldon'
__date__ = '2019/1/6 15:39'

from oss2 import Auth, Bucket

from .config_manager import get_conf_attr
from MxOnline.settings import VIDEO_MANAGER

class AliyunOssManager(object):

    def __init__(self, accessKeyId, accessKeySecret, bucketName=None, endPoint=None):
        self.id = accessKeyId
        self.secret = accessKeySecret
        self.bucketName = bucketName
        self.endPoint = endPoint
        self.bucket = None
        self.auth = None

    def _auth(self):
        if not self.auth:
            self.auth = Auth(self.id, self.secret)

    def video_exists(self, videoPath, bucketName=None, endPoint=None):
        self._set_bucket(bucketName,endPoint)
        return self.bucket.object_exists(videoPath)

    def _set_bucket(self, bucketName=None, endPoint=None):
        if bucketName:
            self.bucketName = bucketName
        if endPoint:
            self.endPoint = endPoint
        if not self.auth:
            self._auth()
        self.bucket = Bucket(self.auth, bucket_name=self.bucketName, endpoint=self.endPoint)

    def get_video_url(self, videoPath, expires=3600,bucketName=None, endPoint=None):
        if not self.bucket:
            self._set_bucket(bucketName, endPoint)
        return self.bucket.sign_url(method='GET',key=videoPath, expires=expires)

    def upload_video(self, videoPath):
        pass



videoManager = AliyunOssManager(**get_conf_attr(VIDEO_MANAGER))