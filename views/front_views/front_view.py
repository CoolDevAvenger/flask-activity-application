# -*- coding: utf-8 -*-
from flask import render_template, views, request, current_app
from . import bp
from ..view_func import front_risk_control
from common_utils.utils_funcs import generate_qrcode, is_wap
from constants import SITE_CONFIG_CACHE
from models.cms_table import SiteConfigModel, ProductModel, AccessLogModel, IpBlackModel, AccountBlackModel
from urllib.parse import urlparse
import random
from common_utils import xtjson
from common_utils.utils_funcs import graph_captcha, checkcap, get_ip
from datetime import datetime

@bp.before_request
def site_before_request():
    statu, res = front_risk_control()
    if not statu:
        return res



class FrontIndex(views.MethodView):
    add_url_rules = [['/', 'front_index']]

    def get(self):
        context = {}
        context['configData'] = SITE_CONFIG_CACHE
        context['PROJECT_NAME'] = current_app.config.get('PROJECT_NAME')
        if current_app.config.get('PROJECT_NAME') == 'project_tk88':
            ios_package = 'itms-services://?action=download-manifest&url=https://tk888.app/assets/app/ipa.plist'
            linkAppText = 'TK88 link dẫn tải xuống'
            linkApp = '/app_install'
        elif current_app.config.get('PROJECT_NAME') == 'project_ws':
            ios_package = 'itms-services://?action=download-manifest&url=https://ws905.com/assets/app/ipa.plist'
            linkAppText = '强盛集团下载链接'
            linkApp = '/app_install'
            context['linkApp'] = linkApp
            context['linkAppText'] = linkAppText
            context['ios_package'] = ios_package
            return render_template('project_ws/index.html', **context)
        else:
            ios_package = 'itms-services://?action=download-manifest&url=https://sodo66.app/assets/app/ipa.plist'
            linkAppText = 'SODO66 link dẫn tải xuống'
            linkApp = '/app_install'
        context['linkApp'] = linkApp
        context['linkAppText'] = linkAppText
        context['ios_package'] = ios_package
        return render_template('project_tk88/index.html', **context)



class AppView(views.MethodView):
    add_url_rules = [['/app', 'app_view']]

    def get(self):
        context = {}
        context['project_name'] = current_app.config.get('PROJECT_NAME')
        context['config_data'] = SiteConfigModel.find_one({}) or {}
        if context.get('project_name') == 'project_sodo':
            title = 'SODO link dẫn tải xuống'
            xinRen = 'sodo66'
        elif context.get('project_name') == 'project_ws':
            title = '强盛集团下载链接'
            xinRen = 'ws905'
        else:
            xinRen = 'TK88'
            title = 'TK88 link dẫn tải xuống'
        context['title'] = title
        context['xinRen'] = xinRen
        return render_template('project_tk88/app.html', **context)



class AppInatallView(views.MethodView):
    add_url_rules = [['/app_install', 'app_install']]

    def get(self):
        context = {}
        context['project_name'] = current_app.config.get('PROJECT_NAME')
        if context.get('project_name') == 'project_sodo':
            title = 'SODO link dẫn tải xuống'
            appNameText = 'SODO link'
            appIcon = '/assets/images/logo.png'
            appIosLink = '/assets/linkApk/sodo66link.mobileconfig'
            appApkLink = '/assets/linkApk/sodo66link.apk'
            apkNmae = 'sodo66link.apk'
            xinRen = 'sodo66'
        elif context.get('project_name') == 'project_ws':
            title = '强盛集团下载链接'
            appNameText = '强盛集团下载'
            appIcon = '/assets/images/logo.png'
            appIosLink = '/assets/linkApk/sodo66link.mobileconfig'
            appApkLink = '/assets/linkApk/sodo66link.apk'
            apkNmae = 'sodo66link.apk'
            xinRen = 'sodo66'
        else:
            xinRen = 'TK88'
            title = 'TK88 link dẫn tải xuống'
            appNameText = 'TK88 link dẫn tải xuống'
            apkNmae = 'TK88link.apk'
            appIcon = '/assets/images/logo.png'
            appIosLink = '/assets/linkApk/TK88link.mobileconfig'
            appApkLink = '/assets/linkApk/TK88link.apk'
        context['title'] = title
        context['xinRen'] = xinRen
        context['apkNmae'] = apkNmae
        context['appIcon'] = appIcon
        context['appIosLink'] = appIosLink
        context['appApkLink'] = appApkLink
        context['appNameText'] = appNameText
        return render_template('project_tk88/install_app.html', **context)



class InstallView(views.MethodView):
    add_url_rules = [['/install', 'install_view']]

    def get(self):
        context = {}
        context['project_name'] = current_app.config.get('PROJECT_NAME')
        if current_app.config.get('PROJECT_NAME') == 'project_tk88':
            return render_template('project_tk88/install.html', **context)
        return render_template('project_tk88/install_sodo.html', **context)



class FrontView(views.MethodView):
    add_url_rules = [['/', 'front_index'], ['/pc.html', 'front_pc_index']]

    def get(self):
        context = {}
        ios_package = ''
        if hasattr(SITE_CONFIG_CACHE, 'ios_package'):
            ios_package = SITE_CONFIG_CACHE.ios_package or ''

        customerService_link = ''
        if hasattr(SITE_CONFIG_CACHE, 'customerService_link'):
            customerService_link = SITE_CONFIG_CACHE.customerService_link or ''

        android_link = ''
        if hasattr(SITE_CONFIG_CACHE, 'android_link'):
            android_link = SITE_CONFIG_CACHE.android_link or ''

        spare_link = ''
        if hasattr(SITE_CONFIG_CACHE, 'spare_link'):
            spare_link = SITE_CONFIG_CACHE.spare_link or ''

        pc_qrcode = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_qrcode'):
            pc_qrcode = SITE_CONFIG_CACHE.pc_qrcode or ''

        pc_link1 = ''
        pc_link_host1 = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_link1'):
            pc_link1 = SITE_CONFIG_CACHE.pc_link1 or ''
            pc_link_host1 = urlparse(pc_link1).hostname
            if pc_link_host1.count('.') > 1:
                pc_link_host1 = '.'.join(list(pc_link_host1.split('.')[-2:]))


        pc_link2 = ''
        pc_link_host2 = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_link2'):
            pc_link2 = SITE_CONFIG_CACHE.pc_link2 or ''
            pc_link_host2 = urlparse(pc_link2).hostname
            if pc_link_host2.count('.') > 1:
                pc_link_host2 = '.'.join(list(pc_link_host2.split('.')[-2:]))

        pc_link3 = ''
        pc_link_host3 = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_link3'):
            pc_link3 = SITE_CONFIG_CACHE.pc_link3 or ''
            pc_link_host3 = urlparse(pc_link3).hostname
            if pc_link_host3.count('.') > 1:
                pc_link_host3 = '.'.join(list(pc_link_host3.split('.')[-2:]))

        pc_link4 = ''
        pc_link_host4 = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_link4'):
            pc_link4 = SITE_CONFIG_CACHE.pc_link4 or ''
            pc_link_host4 = urlparse(pc_link4).hostname
            if pc_link_host4.count('.') > 1:
                pc_link_host4 = '.'.join(list(pc_link_host4.split('.')[-2:]))

        pc_link5 = ''
        pc_link_host5 = ''
        if hasattr(SITE_CONFIG_CACHE, 'pc_link5'):
            pc_link5 = SITE_CONFIG_CACHE.pc_link5 or ''
            pc_link_host5 = urlparse(pc_link5).hostname
            if pc_link_host5.count('.') > 1:
                pc_link_host5 = '.'.join(list(pc_link_host5.split('.')[-2:]))

        if ios_package:
            ios_package = 'itms-services://?action=download-manifest&url=https://tk883.app/assets/app/ipa.plist'
        else:
            ios_package = spare_link

        if is_wap():
            context['android_link'] = android_link
            context['customerService_link'] = customerService_link
            context['ios_package'] = ios_package
            template = 'project_ck88/index.html'
        else:
            android_link = generate_qrcode(android_link)
            ios_package = generate_qrcode(ios_package)

            context['customerService_link'] = customerService_link
            context['android_link'] = android_link
            context['ios_package'] = ios_package
            context['pc_qrcode'] = pc_qrcode
            context['pc_link1'] = pc_link1
            context['pc_link_host1'] = pc_link_host1
            context['pc_link2'] = pc_link2
            context['pc_link_host2'] = pc_link_host2
            context['pc_link3'] = pc_link3
            context['pc_link_host3'] = pc_link_host3
            context['pc_link4'] = pc_link4
            context['pc_link_host4'] = pc_link_host4
            context['pc_link5'] = pc_link5
            context['pc_link_host5'] = pc_link_host5
            template = 'project_ck88/pc/index.html'

        return render_template(template, **context)

    def post(self):
        action = request.form.get('action')
        if action == 'getRandomLink':
            pc_link1 = ''
            pc_link_host1 = ''
            if hasattr(SITE_CONFIG_CACHE, 'pc_link1'):
                pc_link1 = SITE_CONFIG_CACHE.pc_link1 or ''
                pc_link_host1 = urlparse(pc_link1).hostname
                if pc_link_host1.count('.') > 1:
                    pc_link_host1 = '.'.join(list(pc_link_host1.split('.')[-2:]))

            pc_link2 = ''
            pc_link_host2 = ''
            if hasattr(SITE_CONFIG_CACHE, 'pc_link2'):
                pc_link2 = SITE_CONFIG_CACHE.pc_link2 or ''
                pc_link_host2 = urlparse(pc_link2).hostname
                if pc_link_host2.count('.') > 1:
                    pc_link_host2 = '.'.join(list(pc_link_host2.split('.')[-2:]))

            pc_link3 = ''
            pc_link_host3 = ''
            if hasattr(SITE_CONFIG_CACHE, 'pc_link3'):
                pc_link3 = SITE_CONFIG_CACHE.pc_link3 or ''
                pc_link_host3 = urlparse(pc_link3).hostname
                if pc_link_host3.count('.') > 1:
                    pc_link_host3 = '.'.join(list(pc_link_host3.split('.')[-2:]))

            pc_link4 = ''
            pc_link_host4 = ''
            if hasattr(SITE_CONFIG_CACHE, 'pc_link4'):
                pc_link4 = SITE_CONFIG_CACHE.pc_link4 or ''
                pc_link_host4 = urlparse(pc_link4).hostname
                if pc_link_host4.count('.') > 1:
                    pc_link_host4 = '.'.join(list(pc_link_host4.split('.')[-2:]))

            pc_link5 = ''
            pc_link_host5 = ''
            if hasattr(SITE_CONFIG_CACHE, 'pc_link5'):
                pc_link5 = SITE_CONFIG_CACHE.pc_link5 or ''
                pc_link_host5 = urlparse(pc_link5).hostname
                if pc_link_host5.count('.') > 1:
                    pc_link_host5 = '.'.join(list(pc_link_host5.split('.')[-2:]))

            links = [
                {
                    'link': pc_link1,
                    'link_host': pc_link_host1,
                },{
                    'link': pc_link2,
                    'link_host': pc_link_host2,
                },{
                    'link': pc_link3,
                    'link_host': pc_link_host3,
                },{
                    'link': pc_link4,
                    'link_host': pc_link_host4,
                },{
                    'link': pc_link5,
                    'link_host': pc_link_host5,
                }
            ]
            random.shuffle(links)

            return xtjson.json_result(data={'links': links})


class IOSView(views.MethodView):
    add_url_rules = [['/ios', 'ios_view']]

    def get(self):
        context = {}
        projcet_name = current_app.config.get('PROJECT_NAME')
        if projcet_name == 'project_tk88':
            context['tzUrl'] = 'https://tk88p.com'
            return render_template('iosHome/tk_ios3.html', **context)
        if projcet_name == 'project_ws':
            context['title'] = '万盛集团'
            context['project_name'] = 'project_ws'
            context['tzUrl'] = 'https://ws991.com'
            context['logo'] = '/assets/images/logo.png'
            context['manifest'] = '/manifest_ws.json'
        if projcet_name == 'project_sodo':
            context['projcet_name'] = 'project_sodo'
            context['title'] = 'SODO66'
            context['tzUrl'] = 'https://sodo.ink'
            context['logo'] = '/static/images/logo2.png'
            context['manifest'] = '/manifest.json'
        return render_template('iosHome/ios.html', **context)


class DashboardView(views.MethodView):
    add_url_rules = [['/dashboard', 'dashboard_view']]

    def get(self):
        context = {}
        projcet_name = current_app.config.get('PROJECT_NAME')

        if projcet_name == 'project_tk88':
            context['tzUrl'] = 'https://tk88p.com'
            return render_template('iosHome/tk_ios3.html', **context)
        if projcet_name == 'project_ws':
            context['title'] = '万盛集团'
            context['project_name'] = 'project_ws'
            context['tzUrl'] = 'https://ws991.com'
            context['logo'] = '/assets/images/logo.png'
            context['manifest'] = '/manifest_ws.json'
        if projcet_name == 'project_sodo':
            context['projcet_name'] = 'project_sodo'
            context['title'] = 'SODO66'
            context['tzUrl'] = 'https://sodo.ink'
            context['logo'] = '/static/images/logo2.png'
            context['manifest'] = '/manifest.json'

        context['data'] = ProductModel.find_all()

        return render_template('dashboard/index.html', **context)
    
class DashboardMobileView(views.MethodView):
    add_url_rules = [['/dashboard/mb', 'mb_view']]

    def get(self):
        context = {}
        projcet_name = current_app.config.get('PROJECT_NAME')

        if projcet_name == 'project_tk88':
            context['tzUrl'] = 'https://tk88p.com'
            return render_template('iosHome/tk_ios3.html', **context)
        if projcet_name == 'project_ws':
            context['title'] = '万盛集团'
            context['project_name'] = 'project_ws'
            context['tzUrl'] = 'https://ws991.com'
            context['logo'] = '/assets/images/logo.png'
            context['manifest'] = '/manifest_ws.json'
        if projcet_name == 'project_sodo':
            context['projcet_name'] = 'project_sodo'
            context['title'] = 'SODO66'
            context['tzUrl'] = 'https://sodo.ink'
            context['logo'] = '/static/images/logo2.png'
            context['manifest'] = '/manifest.json'
        
        context['data'] = ProductModel.find_all()

        return render_template('dashboard/mobile.html', **context)
    
class DetailView(views.MethodView):
    add_url_rules = [['/dashboard/detail', 'detail_view']]

    def get(self):        
        context = {}
        projcet_name = current_app.config.get('PROJECT_NAME')

        if projcet_name == 'project_tk88':
            context['tzUrl'] = 'https://tk88p.com'
            return render_template('iosHome/tk_ios3.html', **context)
        if projcet_name == 'project_ws':
            context['title'] = '万盛集团'
            context['project_name'] = 'project_ws'
            context['tzUrl'] = 'https://ws991.com'
            context['logo'] = '/assets/images/logo.png'
            context['manifest'] = '/manifest_ws.json'
        if projcet_name == 'project_sodo':
            context['projcet_name'] = 'project_sodo'
            context['title'] = 'SODO66'
            context['tzUrl'] = 'https://sodo.ink'
            context['logo'] = '/static/images/logo2.png'
            context['manifest'] = '/manifest.json'
        
        vid = request.args.get('vid')
        product = ProductModel.find_one({"uuid": vid})

        context['product'] = product
        context['img_cap'] = graph_captcha()
        return render_template('dashboard/detail.html', **context)

    def post(self):
        action = request.form.get('action')
        if action == 'submitApply':
            login_account = request.form.get('account')
            graph_captcha = request.form.get('graph_captcha')
            uuid = request.form.get('uuid')

            if not login_account.strip():
                return xtjson.json_params_error('登录失败!')
            if not graph_captcha.strip():
                return xtjson.json_params_error('请输入验证码!')
            if not checkcap(graph_captcha.strip()):
                return xtjson.json_params_error('验证码输入错误！')
            
            product = ProductModel.find_one({"uuid": uuid})
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            request_url = request.url
            request_method = request.method
            user_agent = request.headers.get('User-Agent', '').lower()
            is_mobile = 'mobile' in user_agent
            device_type = 'Mobile' if is_mobile else 'PC'
            status = "pending"

            tempIp = IpBlackModel.find_one({"ip": ip_address})
            if tempIp:
                status = "ip_block"

            tempAccount = AccountBlackModel.find_one({"account": login_account})
            if tempAccount:
                status = "account_block"

            if datetime.now().date() > datetime.strptime(product["until"], "%Y-%m-%d").date():
                status = "processed"

            AccessLogModel.insert_one({
                "activity": product["name"],
                "account": login_account,
                "ip_address": ip_address,
                "request_url": request_url,
                "request_method": request_method,
                "device_type": device_type,
                "status": status,
                "time": datetime.utcnow()
            })

            if tempIp:
                return xtjson.json_params_error('Block IP')
            if tempAccount:
                return xtjson.json_params_error('Block Account')
            if datetime.now().date() > datetime.strptime(product["until"], "%Y-%m-%d").date():
                return xtjson.json_params_error('Activity finished')
            
            return xtjson.json_result()
        return xtjson.json_params_error('操作失败!')
          
class MbDetailView(views.MethodView):
    add_url_rules = [['/dashboard/mbdetail', 'mb_detail_view']]

    def get(self):
        vid = request.args.get('vid')
        context = {}
        projcet_name = current_app.config.get('PROJECT_NAME')

        if projcet_name == 'project_tk88':
            context['tzUrl'] = 'https://tk88p.com'
            return render_template('iosHome/tk_ios3.html', **context)
        if projcet_name == 'project_ws':
            context['title'] = '万盛集团'
            context['project_name'] = 'project_ws'
            context['tzUrl'] = 'https://ws991.com'
            context['logo'] = '/assets/images/logo.png'
            context['manifest'] = '/manifest_ws.json'
        if projcet_name == 'project_sodo':
            context['projcet_name'] = 'project_sodo'
            context['title'] = 'SODO66'
            context['tzUrl'] = 'https://sodo.ink'
            context['logo'] = '/static/images/logo2.png'
            context['manifest'] = '/manifest.json'
        
        vid = request.args.get('vid')
        product = ProductModel.find_one({"uuid": vid})

        context['product'] = product

        return render_template('dashboard/mbdetail.html', **context)

