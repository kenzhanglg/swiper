"""发送短信验证码"""
import random
import requests

from django.core.cache import cache

from swiper import config
from lib.http import render_json
from common import errors
from common import keys
from worker import celery_app


def gen_vcode(size=4):
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    return random.randint(start, end)


@celery_app.task
def send_vcode(phone):
    vcode = gen_vcode()
    # 加验证码加入缓存中
    cache.set(keys.VCODE_KEY % phone, str(vcode), timeout=3*60)
    params = config.YZX_PARAMS.copy()
    params['param'] = vcode
    params['mobile'] = phone
    response = requests.post(url=config.YZX_URL, json=params)

    if response.status_code == 200:
        # 通信正常
        result = response.json()
        print(result['code'])
        if result['code'] != '000000':
            # 短信发送有误
            return False, '短信发送有误'
        else:
            return True, 'OK'
    else:
        # 通信错误
        return render_json(code=errors.SMS_SERVER_ERROR, data='访问短信服务平台异常')
