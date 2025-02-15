# -*- coding: UTF-8 -*-
import re, os, time, uuid, shortuuid, random, hashlib, zlib, base64, qrcode, datetime
from io import BytesIO
from flask import request
from flask_paginate import Pagination
from .captcha.xtcaptcha import Captcha
from .lqredis import SiteRedis
from .encrypt.RC4_CLS import Rc4
from constants import SITE_CONFIG_CACHE


def create_order_num():
    """生成流水订单号"""
    res_id = ''.join(list(str(int(time.time()*1000 + random.choice(range(10000, 99999))))[2:])[::-1])
    crr_date = datetime.datetime.now().strftime('%Y%m%d')
    perf_counter = str(int(time.perf_counter()*10000))
    return res_id + crr_date + perf_counter

def create_secret_key():
    """生成唯一的秘钥"""
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, shortuuid.uuid()))

def generate_filename():
    """生成文件名"""
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    res = '%s%s' % (filename_prefix, str(random.randrange(1, 10000)))
    return res

def get_content_md5(content):
    """计算内容MD5"""
    myhash = hashlib.md5()
    while True:
        b = content[0:4096]
        if not b:
            break
        content = content[4096:]
        myhash.update(b)
    return myhash.hexdigest()

def get_file_md5(file_name):
    """计算文件md5值"""
    if not isinstance(file_name, bytes):
        file_name = file_name.encode()
    if not os.path.exists(file_name):
        return False, '文件不存在!'
    m = hashlib.md5()
    with open(file_name, 'rb') as fobj:
        while True:
            f = fobj.read(4096)
            if not f:
                break
            m.update(f)
    return True, m.hexdigest()

def get_file_sha1(fineName, block_size=4 * 1024):
    """文件sha1"""
    if not isinstance(fineName, bytes):
        fineName = fineName.encode()
    if not os.path.exists(fineName):
        return False, '文件不存在!'
    sha1 = hashlib.sha1()
    with open(fineName, 'rb') as f:
        while True:
            data = f.read(block_size)
            if not data:
                break
            sha1.update(data)
    retsha1 = base64.b64encode(sha1.digest())
    return True, retsha1

def check_telephone(telephone):
    """检测手机号"""
    if not telephone or not telephone.strip():
        return False, u'手机号不能为空！'
    if len(telephone.strip()) != 11:
        return False, u'手机号为11位哦！'
    p2 = re.compile('^1[3578]\d{9}$|^147\d{8}$')
    if not p2.match(telephone.strip()):
        return False, u'手机号格式不对！'
    return True, telephone.strip()

def is_valid_url(url):
    """检测URL"""
    _URL_REGEX = re.compile(
        r"^(?:[a-z0-9\.\-]*)://"  # scheme is validated separately
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    _URL_SCHEMES = ["http", "https", "ftp", "ftps"]
    scheme = url.split("://")[0].lower()
    if scheme not in _URL_SCHEMES:
        return False, '无效的协议!'
    if not _URL_REGEX.match(url):
        return False, '无效的URL!'
    return True, ''

def zlib_encry(a):
    """压缩字符串"""
    aa = zlib.compress(a)
    return base64.b64encode(aa)

def zlib_decry(d):
    """解压字符串"""
    dd = base64.b64decode(d)
    return zlib.decompress(dd)

def encry_md5(data):
    """MD5加密"""
    md5_object = hashlib.md5()
    md5_object.update(data.encode('utf8'))
    md5_result = md5_object.hexdigest()
    return md5_result

def get_file_size(file_path, types='KB'):
    """
    获取文件大小
    :param file_path: 文件类型
    :param types: 文件大小格式（KB, MB, T）
    :return:
    """
    if types == 'MB':
        fsize = os.path.getsize(file_path)
        fsize = fsize / float(1024 * 1024)
        return round(fsize, 3)
    fsize = os.path.getsize(file_path)
    fsize = fsize / 1024
    return round(fsize, 3)

def is_wap():
    """判断是否是移动端"""
    ua = str(request.user_agent).lower()
    for w in ['iphone','android']:
        if w in ua:
            return True
    return False

def check_ip(ip):
    """判断ip"""
    ep = re.compile('(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)')
    if not ep.match(ip.strip()):
        return False, u'ip格式不对！'
    return True, ip.strip()

def get_ip():
    """获取真实ip"""
    ip = request.headers.get('X-Forwarded-For')
    if ip:
        return ip
    ip_list = list(request.access_route)
    return ', '.join(ip_list)

def graph_captcha():
    """图片验证码"""
    text, image = Captcha.gene_code()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    SiteRedis.set(text.lower(), text.lower(), expire=60)
    img = 'data:image/png;base64,%s' % base64.b64encode(out.read()).decode()
    return img

def checkcap(cap):
    """检测图片验证码"""
    if Captcha.check_captcha(cap):
        return True
    return False

def generate_qrcode(data):
    """二维码"""
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    imagel = qr.make_image()
    out = BytesIO()
    imagel.save(out, 'png')
    out.seek(0)
    qr_img = u'data:image/png;base64,%s' % base64.b64encode(out.read()).decode()
    return qr_img

def get_random_time():
    """获取随机时间"""
    crr_date = datetime.datetime.now()
    if crr_date.hour < 6:
        a1 = (crr_date.year, crr_date.month, crr_date.day-1, 6, 0, 0, 0, 0, 0)
        a2 = (crr_date.year, crr_date.month, crr_date.day-1, crr_date.hour, crr_date.minute, crr_date.second, 0, 0, 0)
    else:
        a1 = (crr_date.year, crr_date.month, crr_date.day, 6, 0, 0, 0, 0, 0)
        a2 = (crr_date.year, crr_date.month, crr_date.day, crr_date.hour, crr_date.minute, crr_date.second, 0, 0, 0)
    start = time.mktime(a1)
    end = time.mktime(a2)
    t = random.randint(int(start), int(end))
    date_touple = time.localtime(t)
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", date_touple)
    rand_date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return rand_date


class PagingCLS(object):

    @classmethod
    def by_silce(cls, startendstr):
        if startendstr and '|' not in startendstr:
            raise ValueError(u'区间搜索必须以“|”分割')
        start_str, end_str = startendstr.split("|")
        if start_str.isdigit() or end_str.isdigit():
            if start_str and end_str:
                return int(start_str),int(end_str)
            if start_str and not end_str:
                return int(start_str),None
            return None,int(end_str)
        else:
            if start_str:
                try:
                    start_time = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        start_time = datetime.datetime.strptime(start_str, '%Y-%m-%d')
                    except Exception as e:
                        raise ValueError(u'起始时间转换出错: %s' % str(e))
            else:
                start_time = None
            if end_str:
                try:
                    end_time = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')
                except:
                    try:
                        end_time = datetime.datetime.strptime(end_str, '%Y-%m-%d')
                    except Exception as e:
                        raise ValueError(u'结束时间转换出错: %s' % str(e))
            else:
                end_time = None
            return start_time, end_time

    @classmethod
    def pagination(cls, page, per_page, total, **kwargs):
        return Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4', alignment='center', **kwargs)

    @classmethod
    def ustom_pagination(cls, page, data_count, PAGE_NUM=None):
        # page:当前页面
        # data_count:数据总数
        # PAGE_NUM：每页的显示数据数量
        if not PAGE_NUM:
            PAGE_NUM = 10
        total_page = data_count // PAGE_NUM
        if data_count % PAGE_NUM > 0:
            total_page += 1

        pages = []
        tmp_page = page - 1
        while tmp_page >= 1:
            if tmp_page % 5 == 0:
                break
            pages.append(tmp_page)
            tmp_page -= 1
        tmp_page = page
        while tmp_page <= total_page:
            if tmp_page % 5 == 0:
                pages.append(tmp_page)
                break
            else:
                pages.append(tmp_page)
                tmp_page += 1

        pages.sort()
        return pages, total_page


from project_ws import ProjectConfig
class RC4CLS(object):

    @classmethod
    def encrypt(cls, data):
        try:
            mi = Rc4(ProjectConfig.PROJECT_NAME + '666999').encrypt(data)
            return mi
        except Exception as e:
            return False

    @classmethod
    def decrypt(cls, data):
        try:
            mg = Rc4(ProjectConfig.PROJECT_NAME + '666999').decrypt(data)
            return mg
        except:
            return False
