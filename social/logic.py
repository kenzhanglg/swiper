import datetime

from django.core.cache import cache

from common import keys, errors
from social.models import Swipe
from social.models import Friend
from swiper import config
from user.models import User


def like(user, sid):
    Swipe.like(user.id, sid)
    # 判断对方是否喜欢我们
    if Swipe.has_like(sid):
        # 建立好友关系
        Friend.make_friends(user.id, sid)
        return {'match': True}
    else:
        return {'match': False}


def superlike(user, sid):
    Swipe.superlike(user.id, sid)
    # 判断对方是否喜欢我们
    if Swipe.has_like(sid):
        # 建立好友关系
        Friend.make_friends(user.id, sid)
        return {'match': True}
    else:
        return {'match': False}


def get_recmd_list(user):
    # 取出已经滑过的人
    # 结果是一个数据集
    swiped = Swipe.objects.filter(uid=user.id).only('sid')
    swiped_list = [sw.id for sw in swiped]

    # 排除自己
    swiped_list.append(user.id)

    # 根据自己的条件去筛选
    # 年龄、城市
    curr_year = datetime.datetime.now().year
    max_birth_year = curr_year - user.profile.min_dating_age
    min_birth_year = curr_year - user.profile.max_dating_age
    # 排除已经滑过的人  exclude 排除
    # 不要一次性把全部都返回，一次返回前20个
    users = User.objects.filter(location=user.profile.location,
                                birth_year__range=(min_birth_year,
                                                   max_birth_year),
                                sex=user.profile.dating_sex,
                                ).exclude(id__in=swiped_list)[:20]
    return users


def get_liked_me(user):
    swipe = Swipe.objects.filter(sid=user.id, mark__in=['like', 'superlike']).only('uid')
    liked_me_list = [sw.id for sw in swipe]
    users = User.objects.filter(id__in=liked_me_list)
    return users


def rewind(user):
    now = datetime.datetime.now()
    key = keys.REWIND_KEY % (user.id, now.date())
    # 拿不到就用默认值代替
    rewind_times = cache.get(key, 0)
    # 取出的次数和最大允许返回次数做对比
    if rewind_times < config.REWIND_TIMES:
        # 执行返回操作
        # 删除Swipe中的记录，如果有好友关系，也需要取消
        record = Swipe.objects.filter(uid=user.id).latest(field_name='swipe_time')
        uid1, uid2 = (user.id, record.id) if user.id < record.id else (record.id, user.id)
        Friend.objects.filter(uid1=uid1, uid2=uid2).delete()
        record.delete()

        # 更新缓存
        rewind_times += 1
        timeout = 24*60*60 - (now.hour*3600 + now.minute * 60 + now.second)
        cache.set(key, rewind_times, timeout)
        return True
    else:
        return errors.ExceedRewindTimes

