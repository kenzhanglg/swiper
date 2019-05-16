import os

from django.conf import settings

from common import keys
from lib.qiniu import upload_qiniu
from worker import celery_app


@celery_app.task
def handler_avatar_upload(uid, avatar):
    filename = keys.AVATAR_KEY % uid
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    with open(filepath, mode='wb+') as fp:
        # 生成器返回文件的块。如果multiple_chunks()是
        # True，您应该在循环中使用此方法而不是read()。
        # 在实践中，通常最简单的方法就是一直使用chunks()。循环chunks()
        # 而不是使用read()确保大文件不会压倒系统的内存。
        for chunk in avatar.chunks():
            fp.write(chunk)
    # 上传到七牛云
    upload_qiniu(uid, filepath)
