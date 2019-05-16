import os

from django.core.cache import cache
from django.http import HttpResponse
from django.conf import settings

from user.models import User
from lib.http import render_json
from common import errors
from lib.sms import send_vcode
from common import keys
from user.forms import ProfileModelForm
from user.logic import handler_avatar_upload
from worker import celery_app


# Create your views here.
def submit_phonenum(request):
    """提交手机号码"""
    phone = request.POST.get('phone')
    if phone:
        # result, msg = send_vcode(phone)
        # if result:
        #     return render_json(code=0, data=msg)
        # else:
        #     return render_json(code=errors.SMS_ERROR, data=msg)
        send_vcode.delay(phone)
        # print(send_vcode(phone))
        return render_json(data='Ok')
    else:
        raise errors.PhoneNumEmpty()


def submit_vcode(request):
    """提交验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取出vcode
    cache_vcode = cache.get(keys.VCODE_KEY % phone)
    if cache_vcode == vcode:
        user, create = User.objects.get_or_create(phonenum=phone,
                                                  nickname=phone)
        request.session['uid'] = user.id
        print(user.to_dict())
        return render_json(code=0, data=user.to_dict())
    else:
        raise errors.VcodeError()


def get_profile(request):
    """获取个人交友资料"""
    user = User.objects.get(id=request.session['uid'])
    return render_json(code=0, data=user.profile.to_dict())


def edit_profile(request):
    """修改个人交友资料"""
    # location = request.POST.get('location')
    # min_distance = request.POST.get('min_distance')
    # max_distance = request.POST.get('max_distance')
    # min_dating_age = request.POST.get('min_dating_age')
    # max_dating_age = request.POST.get('max_dating_age')
    # dating_sex = request.POST.get('dating_sex')
    # vibration = request.POST.get('vibration')
    # only_matche = request.POST.get('only_matche')
    # auto_play = request.POST.get('auto_play')
    # django form 表单

    # form表单
    form = ProfileModelForm(request.POST)
    # 表单验证
    if form.is_valid():
        profile = form.save(commit=False)
        # 将交友资料的 id 与 用户id 一致 实现 一对一关系
        profile.id = request.session['uid']
        profile.save()
        return render_json(code=0, data=profile.to_dict())
    return render_json(code=errors.ProfileError, data=form.errors)


def upload_avatar(request):
    """头像上传"""
    avatar = request.FILES.get('avatar')
    # print(avatar.name)
    # 保存用户上传的文件到本地
    # 拼出文件路径
    uid = request.session['uid']
    handler_avatar_upload.delay(uid, avatar)
    print(avatar, uid)
    return render_json()
