from django.utils.deprecation import MiddlewareMixin

from user.models import User
from common import errors
from lib.http import render_json


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 从session中获取用户id
        # uid = request.session['uid']
        WHITE_URL = ['/api/user/submit/phonenum/',
                     '/api/user/submit/vcode/']
        if request.path in WHITE_URL:
            return
        uid = request.session.get('uid')
        if uid:
            # 获取对象
            try:
                user = User.objects.get(id=uid)
                request.user = user
                return
            except User.DoesNotExist:
                return render_json(code=errors.UserNotExist, data='用户不存在')
        else:
            return render_json(code=errors.LoginRequired, data='请登录')


class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        if isinstance(exception, errors.LogicErr):
            return render_json(code=exception.code,
                               data=exception.data)
        return
