from django.db import models


# Create your models here.
class Swipe(models.Model):
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike'),
    )
    uid = models.IntegerField(verbose_name='用户自身id', )
    sid = models.IntegerField(verbose_name='被滑的陌生人id', )
    mark = models.CharField(verbose_name='滑动类型',
                            max_length=20, choices=MARK)
    swipe_time = models.DateTimeField(verbose_name='滑动的时间', auto_now_add=True)

    class Meta:
        db_table = 'Swipe'

    # 喜欢
    @classmethod
    def like(cls, uid, sid):
        Swipe.objects.create(uid=uid, sid=sid, mark='like')

    # 超级喜欢
    @classmethod
    def superlike(cls, uid, sid):
        Swipe.objects.create(uid=uid, sid=sid, mark='superlike')

    # 不喜欢
    @classmethod
    def dislike(cls, uid, sid):
        Swipe.objects.create(uid=uid, sid=sid, mark='dislike')

    # 判断是否喜欢某人
    @classmethod
    def has_like(cls, sid):
        return Swipe.objects.filter(uid=sid, mark__in=['like', 'superlike']).exists()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid, sid):
        # 调整uid 和sid 的大小， 调整顺序
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        Friend.objects.create(uid1=uid1, uid2=uid2)

