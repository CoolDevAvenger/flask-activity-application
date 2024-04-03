# -*- coding: UTF-8 -*-
import time, shortuuid, datetime
from flask import session, request, abort
from constants import SITE_CONFIG_CACHE, SpiderType, ClientType, CMS_USER_SESSION_KEY, SITE_SETTING_CACHE, PermissionType
from models.cms_user import CmsUserModel
from common_utils.utils_funcs import get_ip, is_wap


def current_admin_data_dict():
    uuid = session.get(CMS_USER_SESSION_KEY)
    if not uuid:
        return {}
    user_dict = CmsUserModel.find_one({'uuid': uuid})
    return user_dict

def add_admin_log(event_type, content='', ip='', admin_uuid='', look_over=True, **kwargs):
    if not admin_uuid:
        admin_data = current_admin_data_dict()
        admin_uuid = admin_data.get('uuid')
    log_dict = {
        'ip': ip or get_ip(),
        'referer': str(request.referrer),
        'request_url': str(request.url),
        'user_agent': str(request.user_agent),
        'content': content,
        'event_type': event_type,
        'admin_uuid': admin_uuid,
        'look_over': look_over,
    }
    if kwargs:
        log_dict.update(kwargs)
    return

def get_front_domain():
    if not hasattr(SITE_CONFIG_CACHE, 'front_domain'):
        return False, '网站前端域名未设置!'
    front_domain = getattr(SITE_CONFIG_CACHE, 'front_domain')
    if not front_domain:
        return False, '网站前端域名未设置'
    return True, front_domain

def check_front_site_statu():
    if not hasattr(SITE_CONFIG_CACHE, 'site_statu'):
        return False
    if not getattr(SITE_CONFIG_CACHE, 'site_statu'):
        return False
    return True

def spider_ident():
    ua = str(request.user_agent)
    if ua:
        for k,v in SpiderType.spider_mark.items():
            for u in v:
                if u in ua:
                    return getattr(SpiderType, k)
    return ''

def front_access_log(**kwargs):
    res = spider_ident()
    client_type = ClientType.PC
    if is_wap():
        client_type = ClientType.WAP
    log_dict = {
        'ip': get_ip(),
        'look_over': False,
        'spider_type': res,
        'client_type': client_type,
        'request_url': request.url,
        'user_agent': str(request.user_agent),
        'referer': request.referrer or '',
    }
    if kwargs:
        log_dict.update(kwargs)

def check_black():
    """检测黑名单"""
    if not hasattr(SITE_CONFIG_CACHE, 'ip_black'):
        return
    ip_black = getattr(SITE_CONFIG_CACHE, 'ip_black')
    if not ip_black or not ip_black.strip():
        return
    crr_ip = get_ip()
    for _ip in crr_ip.split():
        if _ip in crr_ip:
            return True
    return


def front_risk_control():
    return True, None



def check_cms_domain():
    crr_user = current_admin_data_dict()

    if hasattr(SITE_SETTING_CACHE, 'white_ips'):
        white_ips = getattr(SITE_SETTING_CACHE, 'white_ips') or ''
        ips = white_ips.replace('\r\n', '\n').split('\n')
        if get_ip() not in ips:
            return False, ''

    if not crr_user:
        return True, ''
    if crr_user and crr_user.get('permissions') == [PermissionType.SUPERADMIN]:
        return True, ''
    if not hasattr(SITE_SETTING_CACHE, 'blacklistIp'):
        return True, ''
    blacklistIp = getattr(SITE_SETTING_CACHE, 'blacklistIp')
    if not blacklistIp:
        return True, ''
    if get_ip() in blacklistIp:
        return True, ''
    session.pop(CMS_USER_SESSION_KEY)
    return False, ''

def cms_risk_control():
    statu, res = check_cms_domain()
    if not statu:
        return abort(404)
