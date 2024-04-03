# -*- coding: utf-8 -*-
from . import dbModel
from constants import SITE_CONFIG_CACHE, FRONT_CONFIG_CACHE


class SiteConfigModel(dbModel):
    """网站配置"""
    __tablename__ = 'site_config_table'
    uuid = dbModel.UUIDField()
    project_name = dbModel.StringField('项目名', nullable=False)
    secret_key = dbModel.StringField('项目秘钥', nullable=False)
    cms_prefix = dbModel.StringField('CMS登录目录', nullable=False)
    max_filesize = dbModel.IntegerField('项目最大文件限制/KB')
    cms_text = dbModel.StringField('后台名称')
    cms_icon = dbModel.StringField('后台ICON图标')
    front_domain = dbModel.StringField('网站前端域名', nullable=False)
    cms_domain = dbModel.StringField('网站后台域名', nullable=False)

    robots = dbModel.StringField('Robots文件')
    baidu_resou_link = dbModel.StringField('百度资源API链接')
    ip_black = dbModel.StringField('ip黑名单')

    # 网站功能
    site_statu = dbModel.BooleanField('网站状态', default=0, true_text='已开启', false_text='已关闭')
    cms_captcha = dbModel.BooleanField('CMS登录图片验证码', default=0, true_text='已开启', false_text='已关闭')
    cms_log_save_time = dbModel.IntegerField('CMS操作日志保存时间/天')
    front_log_save_time = dbModel.IntegerField('前端日志保存时间/天')

    ios_package = dbModel.StringField('IOS安装包')
    android_link = dbModel.StringField('安装包链接')
    spare_link = dbModel.StringField('备用链接')
    ios_version = dbModel.StringField('IOS版本号')
    android_version = dbModel.StringField('android版本号')

    ipa_package = dbModel.StringField('IPA软件包路径')
    standby_link = dbModel.StringField('备用链接')
    white_ips= dbModel.StringField('白名单ip')

    customerService_link = dbModel.StringField('客服链接')
    xz_android_link = dbModel.StringField('android下载链接')

    pc_qrcode = dbModel.StringField('PC二维码')
    pc_link1 = dbModel.StringField('PC链接1')
    pc_link2 = dbModel.StringField('PC链接2')
    pc_link3 = dbModel.StringField('PC链接3')
    pc_link4 = dbModel.StringField('PC链接4')
    pc_link5 = dbModel.StringField('PC链接5')

    @classmethod
    def update_site_config(cls, config={}):
        if not config:
            config = cls.find_one({}) or {}
        SITE_CONFIG_CACHE.__dict__.update(config)

class ProductModel(dbModel):
    __tablename__ = 'product_table'
    uuid = dbModel.UUIDField()
    name = dbModel.StringField('name', nullable=False)
    url = dbModel.StringField('url', nullable=False)
    activity = dbModel.StringField('activity')
    img = dbModel.StringField('img')
    detailImg = dbModel.StringField('detailImg')
    message = dbModel.StringField('message')
    until = dbModel.DateTimeField('until')  
    date = dbModel.StringField('time')
 
    @classmethod
    def update_product(cls, config={}):
        if not config:
            config = cls.find_one({}) or {}
        SITE_CONFIG_CACHE.__dict__.update(config)

class AccessLogModel(dbModel):
    """网站配置"""
    __tablename__ = 'access_log_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('account')
    ip_address = dbModel.StringField('ip_address')
    request_url = dbModel.StringField('request_url')
    request_method = dbModel.StringField('request_method')
    device_type = dbModel.StringField('device_type')
    status = dbModel.StringField('status')
    time = dbModel.DateTimeField('time')

class IpBlackModel(dbModel):
    """网站配置"""
    __tablename__ = 'ip_black_table'
    uuid = dbModel.UUIDField()
    ip = dbModel.StringField('ip')
    description = dbModel.StringField("description")
    time = dbModel.DateTimeField('time')

class AccountBlackModel(dbModel):
    """网站配置"""
    __tablename__ = 'account_black_table'
    uuid = dbModel.UUIDField()
    account = dbModel.StringField('account')
    description = dbModel.StringField("description")
    time = dbModel.DateTimeField('time')

class SystemWhiteModel(dbModel):
    """网站配置"""
    __tablename__ = 'system_white_table'
    uuid = dbModel.UUIDField()
    ip = dbModel.StringField('ip')
    description = dbModel.StringField("description")
    time = dbModel.DateTimeField('time')

