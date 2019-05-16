import datetime

from django.db import models

from lib.mixins import ModelMixin
# Create your models here.


class User(models.Model):
    """user"""
    SEX = (
        ('female', '女'),
        ('man', '男'),
    )
    phonenum = models.CharField(max_length=32, verbose_name='手机号', unique=True)
    nickname = models.CharField(verbose_name='昵称', max_length=100, unique=True)
    sex = models.CharField(verbose_name='性别', max_length=20,
                           default='female', choices=SEX)
    birth_year = models.IntegerField(verbose_name='出生年', default=2000)
    birth_month = models.IntegerField(verbose_name='出生月', default=1)
    birth_day = models.IntegerField(verbose_name='出生日', default=1)
    avatar = models.CharField(verbose_name='个人形象', max_length=200)
    location = models.CharField(verbose_name='常居地', max_length=64)

    def __str__(self):
        return f"user: {self.nickname}"

    @property
    def age(self):
        today = datetime.datetime.today()
        birthday = datetime.datetime(year=self.birth_year,
                                     month=self.birth_month,
                                     day=self.birth_day)
        return (today - birthday).days // 365

    # 一对一关系
    @property
    def profile(self):
        if not hasattr(self, '_profile'):
            print('exec get profile')
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'age': self.age,
            'avatar': self.avatar,
            'location': self.location,
        }

    class Meta:
        db_table = 'user'


class Profile(models.Model, ModelMixin):
    SEX = (
        ('female', '女'),
        ('man', '男'),
    )
    location = models.CharField(verbose_name='目标城市', max_length=64)
    min_distance = models.IntegerField(verbose_name='最小查找范围', default=1)
    max_distance = models.IntegerField(verbose_name='最大查找范围', default=20)
    min_dating_age = models.IntegerField(verbose_name='最小交友年龄', default=18)
    max_dating_age = models.IntegerField(verbose_name='最大交友年龄', default=50)
    dating_sex = models.CharField(verbose_name='匹配的性别', choices=SEX,
                                  max_length=20, default='female')
    vibration = models.BooleanField(verbose_name='开启震动', default=True)
    only_matche = models.BooleanField(verbose_name='不让为匹配的人看我的相册', default=True)
    auto_play = models.BooleanField(verbose_name='自动播放视频', default=True)

    class _Meta:
        db_table = 'profile'
