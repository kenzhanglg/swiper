from django.shortcuts import render

# Create your views here.
from common import errors
from lib.http import render_json
from social import logic
from social.models import Swipe


def get_recmd_list(request):
    """获取推荐列表"""
    user = request.user
    users = logic.get_recmd_list(user)
    print(users)
    # users 是一个集合，需要序列化之后返回（字典）
    return render_json(data=[user.to_dict() for user in users])


def like(request):
    """喜欢"""
    sid = int(request.POST.get('sid'))
    user = request.user
    result = logic.like(user, sid)
    return render_json(data=result)


def superlike(requset):
    """超级喜欢"""
    sid = int(requset.POST.get('sid'))
    user = requset.user
    result = logic.superlike(user, sid)
    return render_json(data=result)


def dislike(request):
    """不喜欢"""
    sid = request.POST.get('sid')
    user = request.user
    Swipe.dislike(user.id, sid)
    return render_json(data={'msg': 'ok'})


def rewind(request):
    """反悔 (每天允许返回 3 次)"""
    # 把已经反悔的次数放到缓存中
    user = request.user
    result =logic.rewind(user)
    if result:
        return render_json(data={'rewind': 'Ok'})
    raise errors.ExceedRewindTimes()



def get_like_me_list(request):
    """查看喜欢过我的人"""
    user = request.user
    users = logic.get_liked_me(user)
    return render_json(data=[user.to_dict() for user in users])
