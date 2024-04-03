# -*- coding: utf-8 -*-
import time

CMS_USER_SESSION_KEY = 'cms_user_session_@13141152099'
FRONT_USER_SESSION_KEY = 'front_user_session_@13141152099'

# 缓存机制
SITE_CONFIG_CACHE = type('SiteConfigCache', (object,), {})()
FRONT_CONFIG_CACHE = type('FrontConfigCache', (object,), {})()
SITE_SETTING_CACHE = type('SiteSettingCache', (object,), {})()

CMS_MENUS_GROUPS = []
FRONT_CATEGORY_CACHE = {}

# 导出文件夹名称
EXPORT_FOLDER = 'export_data'

# 静态文件夹名称
STATIC_FOLDER = 'static'
ASSETS_FOLDER = 'assets'
PUBLIC_FOLDER = 'public'
# 私有目录
PRIVATE_FOLDER = 'private'
# 上传文件夹
UPLOAD_FOLDER = 'upload'
# 备份文件夹
DATA_BACKUP_FOLDER = 'backup'
# 前端栏目文件夹
CATEGORY_TEMPLATES_FOLDER = 'category_templates'
# 图片文件夹名称
IMAGES_FOLDER = 'images'
# 图片类型限制
IMAGES_TYPES = ['.png', '.jpeg', '.jpg', '.svg', 'gif']
# 文件类型格式
FIEL_TYPES = ['.txt', '.xlsx', '.csv', '.word']

class UrlPrefix:
    """URL前缀"""
    FRONT_PREFIX = '/'
    API_PREFIX = '/api'
    COMMON_PREFIX = '/common'
    CMS_PREFIX = '/site_admin'


class PermissionType:
    """权限类型"""
    SUPERADMIN = 'superadmin'
    ACCESS = 'access'
    DELETE = 'delete'
    ADD = 'add'
    EDIT = 'edit'
    EXPORT_DATA = 'exportAata'
    UPLOAD_DATA = 'uploadAata'
    name_arr = (ACCESS, DELETE, ADD, EDIT, EXPORT_DATA, UPLOAD_DATA, SUPERADMIN)
    naem_dict = {
        ACCESS: '访问权限', DELETE: '删除数据权限', ADD: '添加数据权限', EDIT: '编辑数据权限', UPLOAD_DATA: '上传数据权限', EXPORT_DATA: '导出数据权限', SUPERADMIN:'最高管理员'
    }


class OnClick:
    """点击类型"""
    JUMP_HREF = 'jump_href'
    SHOW_IMAGES = 'show_images'
    SHOW_CONTENT = 'show_content'
    name_dict = {
        JUMP_HREF: '跳转链接', SHOW_CONTENT: '显示内容', SHOW_IMAGES: '显示图片',
    }


class ClientType:
    """客户端类型"""
    PC = 'pc'
    WAP = 'wap'
    name_arr = (PC, WAP)
    name_dict = { PC: 'pc端', WAP: '移动端'}


class EventType:
    """事件类型"""
    ACCESS = 'access'
    DELETE = 'delete'
    ADD = 'add'
    EDIT = 'edit'
    OUTLOG = 'outlogin'
    LOGIN_SUCCESS = 'login_success'
    LOGIN_FAILED = 'login_failed'
    EXPORT_DATA = 'export_data'
    UPLOAD_DATA = 'upload_data'
    name_arr = (ACCESS, DELETE, ADD, EDIT, LOGIN_SUCCESS,LOGIN_FAILED, EXPORT_DATA, UPLOAD_DATA, OUTLOG)
    name_dict = {
        ACCESS: '访问页面', DELETE: '删除数据', ADD: '添加数据', EDIT: '编辑数据', LOGIN_SUCCESS: '登录成功', LOGIN_FAILED: '登录失败', EXPORT_DATA: '导出数据', UPLOAD_DATA:'上传数据', OUTLOG:'退出登录',
    }
    class_dict = {
        ACCESS: 'btn-default', DELETE: 'btn-danger', ADD: 'btn-success', EDIT: 'btn-default', LOGIN_SUCCESS: 'btn-success', LOGIN_FAILED: 'btn-danger', UPLOAD_DATA: 'btn-success', OUTLOG:'btn-danger',
    }



class CommentAuditStatu:
    is_audit = 'is_audit'
    not_audit = 'not_audit'
    not_through = 'not_through'
    name_arr = (is_audit, not_audit, not_through)
    name_dict = {is_audit: '已审核', not_audit: '未审核', not_through: '未通过'}
    class_dict = {not_audit: 'btn-info',is_audit: 'btn-success',not_through: 'btn-danger',}


class SpiderType:
    """蜘蛛类型"""
    baidu_spider = 'baidu_spider'
    googlebot = 'googlebot'
    spider_360 = 'spider_360'
    soso_spider = 'soso_spider'
    sogou = 'sogou'
    byte_spider = 'byte_spider'
    name_arr = (baidu_spider, googlebot, spider_360, soso_spider, sogou, byte_spider)
    name_dict = {
        baidu_spider: u'百度蜘蛛', googlebot: u'谷歌蜘蛛', spider_360: u'360蜘蛛', soso_spider: u'SOSO蜘蛛', sogou: u'搜狗蜘蛛', byte_spider: u'字节蜘蛛',
    }
    spider_mark = {
        baidu_spider: ['Baiduspider'], googlebot: ['Googlebot'], spider_360: ['360Spider'], soso_spider: ['Sosospider'], sogou: ['Sogou'], byte_spider: ['Bytespider'],
    }


class ExportStatu:
    """导出状态"""
    successed = 'successed'
    failed = 'failed'
    ongoing = 'ongoing'
    name_arr = (successed, failed, ongoing,)
    name_dict = {
        successed: '导出成功', failed: '导出失败', ongoing: '导出中',
    }
    class_dict = {
        successed: 'btn-success', failed: 'btn-danger', ongoing: 'btn-warning',
    }


class CodingType:
    """编码类型"""
    UTF8 = 'UTF-8'
    GB2312 = 'GB2312'
    GBK = 'GBK'
    GB18030 = 'GB18030'
    name_arr = (UTF8, GB2312, GBK, GB18030,)
    name_dict = {UTF8: 'UTF-8', GB2312: 'GB2312', GBK: 'GBK', GB18030: 'GB18030',}


