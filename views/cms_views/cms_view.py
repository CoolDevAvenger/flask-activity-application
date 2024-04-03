# -*- coding: utf-8 -*-
import os, shortuuid, zipfile, time
from flask import render_template, request, current_app, jsonify
from .cms_base import CmsFormViewBase
from models.cms_table import SiteConfigModel, AccessLogModel, ProductModel, IpBlackModel, AccountBlackModel, SystemWhiteModel
from models.cms_user import CmsUserModel
from constants import SITE_CONFIG_CACHE
from modules.fileUplaod.ipaSignature import IpaSignatureChwckCls
from datetime import datetime

class CmsIndexView(CmsFormViewBase):
    
    title = 'TK88 APP'
    show_menu = False
    add_url_rules = [['/', 'cms_index']]
    template = 'cms/cms_index.html'

    def view_get(self):
        if current_app.config.get('PROJECT_NAME') == 'project_sodo':
            self.context['title'] = 'SODO APP'
        elif current_app.config.get('PROJECT_NAME') == 'project_ws':
            self.context['title'] = '万盛集团'
        else:
            self.context['title'] = 'TK88 APP'
        return render_template(self.template, **self.context)


class SystemConfigView(CmsFormViewBase):
    title = '系统配置'
    show_menu = False
    add_url_rules = [['/system/', 'system']]
    template = 'cms/systemConfig.html'
    MCLS = SiteConfigModel

    def updatePlist(self, ipaLink, ipaImage, ipaVersion, title, ipaName, file_path):
        fileText = f'''
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
  <dict>
      <key>items</key>
      <array>
        <dict>
           <key>assets</key>
           <array>
             <dict>
               <key>kind</key>
               <string>software-package</string>
               <key>url</key>
               <string>{ipaLink}</string>
             </dict>
             <dict>
               <key>kind</key>
               <string>display-image</string>
               <key>needs-shine</key>
               <integer>0</integer>
               <key>url</key>
               <string>{ipaImage}</string>
             </dict>
             <dict>
               <key>kind</key>
               <string>full-size-image</string>
               <key>needs-shine</key>
               <true/>
               <key>url</key>
               <string>{ipaImage}</string>
             </dict>
           </array>
           <key>metadata</key>
           <dict>
             <key>bundle-identifier</key>
             <string>{ipaName}</string>
             <key>bundle-version</key>
             <string>{ipaVersion}</string>
             <key>kind</key>
             <string>software</string>
             <key>title</key>
             <string>{title}</string>
           </dict>
        </dict>
      </array>
  </dict>
</plist>        
        '''
        with open(file_path, 'w', encoding='utf8') as wf:
            wf.write(fileText)

    def analyze_ipa_with_plistlib(self, ipa_path, decompress_folder):
        ipa_file = zipfile.ZipFile(ipa_path)
        ipa_file.extractall(path=decompress_folder)
        ipa_file.close()

    def get_mobileprovision(self, ipa_path):
        _path = current_app.root_path + '/' + self.project_static_folder + ipa_path
        if not os.path.exists(_path):
            return self.xtjson.json_params_error('检测失败！文件不存在！')
        decompress_folder = current_app.root_path + '/' + self.project_static_folder + '/assets/uncompress/' + str(int(time.time() * 1000))
        if not os.path.exists(decompress_folder):
            os.makedirs(decompress_folder)
        try:
            self.analyze_ipa_with_plistlib(_path, decompress_folder)
        except Exception as e:
            print('error1:', str(e))
            return False

        fileList = IpaSignatureChwckCls().listFiles(decompress_folder)

        embedded_file, info_file = '', ''
        for f in fileList:
            if f.endswith('.app/Info.plist'):
                info_file = f
            if f.endswith('.app/embedded.mobileprovision'):
                embedded_file = f

        if not embedded_file or not info_file:
            return False, '分析文件失败！'

        if os.path.exists(embedded_file):
            mob = current_app.root_path + '/' + self.project_static_folder + '/assets/app_install/app/app.mobileprovision'
            if os.path.exists(mob):
                cmd1 = 'rm ' + mob
                os.popen(cmd1)
            cmd = 'mv %s %s' % (embedded_file, mob)
            os.popen(cmd)
        cmd = 'rm -rf ' + decompress_folder
        os.popen(cmd)
        return True

    def view_get(self):
        self.context['title'] = self.title
        self.context['configData'] = SITE_CONFIG_CACHE
        return render_template(self.template, **self.context)

    def post_other_way(self):
        if self.action == 'uplaodIosPackage':
            fileobj = request.files.get('upload')
            if not fileobj:
                return self.xtjson.json_params_error()
            fname, fext = os.path.splitext(fileobj.filename)
            folder = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app/'
            if not os.path.exists(folder):
                os.makedirs(folder)

            _uuid = shortuuid.uuid()
            filename = folder + _uuid + fext
            fileobj.save(filename)
            _path = filename.replace(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME'), '')
            return self.xtjson.json_result(message=_path)
        if self.action == 'uplaodAndroidPackage':
            fileobj = request.files.get('upload')
            if not fileobj:
                return self.xtjson.json_params_error()
            fname, fext = os.path.splitext(fileobj.filename)
            folder = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/android/'
            if not os.path.exists(folder):
                os.makedirs(folder)

            _uuid = shortuuid.uuid()
            filename = folder + _uuid + fext
            fileobj.save(filename)
            _path = filename.replace(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME'), '')
            return self.xtjson.json_result(message=_path)
        if self.action == 'updateConfig':
            ios_package = self.request_data.get('ios_package')
            android_link = self.request_data.get('android_link')
            spare_link = self.request_data.get('spare_link')
            ios_version = self.request_data.get('ios_version')
            android_version = self.request_data.get('android_version')

            white_ips = self.request_data.get('white_ips')
            ipa_package = self.request_data.get('ipa_package')
            standby_link = self.request_data.get('standby_link')

            if ios_package and ios_package.startswith('http://'):
                return self.xtjson.json_params_error('.ipa软件包链接必须开启https！')

            _c = self.MCLS.find_one() or {}
            low_ios_package = _c.get('ios_package') or ''
            low_ipa_package = _c.get('ipa_package') or ''

            _c['ios_package'] = ios_package
            _c['android_link'] = android_link
            _c['spare_link'] = spare_link
            _c['ios_version'] = ios_version
            _c['android_version'] = android_version

            _c['white_ips'] = white_ips or ''
            _c['ipa_package'] = ipa_package or ''
            _c['standby_link'] = standby_link or ''

            self.MCLS.save(_c)
            self.MCLS.update_site_config()

            android_path = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/android'
            if os.path.exists(android_path):
                for ad in os.listdir(android_path):
                    if ad in android_link:
                        continue
                    cmd = 'rm ' + android_path + '/' + ad
                    os.system(cmd)

            if ios_package and ios_package != low_ios_package:
                if current_app.config.get('PROJECT_NAME') == 'project_tk88':
                    domain = 'tk888.app'
                    ipaName = 'com.fuzhou.vnsxv3.app'
                    title = 'TK88'
                elif current_app.config.get('PROJECT_NAME') == 'project_ws':
                    domain = 'ws905.com'
                    ipaName = 'com.beijing.youfutongxiang.sxlb'
                    title = '万盛集团'
                else:
                    domain = 'sodo66.app'
                    ipaName = 'com.fuzhou.meiquan.vnsxv1'
                    title = 'Số Đỏ Casino'

                if ios_package.startswith('https://'):
                    ipaLink = ios_package
                else:
                    ipaLink = 'https://' + domain + ios_package
                ipaImage = 'https://%s/assets/images/logo.png' % domain
                ipaVersion = ios_version
                file_path = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app/ipa.plist'
                self.updatePlist(ipaLink, ipaImage, ipaVersion, title, ipaName, file_path)

                for d in os.listdir(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app'):
                    if d in ios_package:
                        continue
                    if d.endswith('.ipa'):
                        cmd = 'rm ' + current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app/' + d
                        os.system(cmd)

            if low_ipa_package != ipa_package and ipa_package:
                if current_app.config.get('PROJECT_NAME') == 'project_tk88':
                    domain = 'tk888.app'
                    ipaName = 'com.live.vnsxv3.app'
                    title = 'TK66 APP'
                    ipaImage = 'https://%s/assets/app_install/images/logo-mb.0bb78b8.png' % domain
                elif current_app.config.get('PROJECT_NAME') == 'project_ws':
                    domain = 'ws905.com'
                    ipaName = 'com.beijing.youfutongxiang.sxlb'
                    title = '万盛集团'
                    ipaImage = 'https://%s/assets/app_install/images/logo.png' % domain
                else:
                    domain = 'sodo66.app'
                    ipaName = 'com.live.vnsxv1.app'
                    title = 'TikTok Live'
                    ipaImage = 'https://%s/assets/app_install/images/TIKTOKLIVE-LOGO-72.png' % domain

                if ios_package.startswith('https://'):
                    ipaLink = ipa_package
                else:
                    ipaLink = 'https://' + domain + ipa_package
                ipaVersion = ios_version

                file_path = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app_install/ipa.plist'
                self.updatePlist(ipaLink, ipaImage, ipaVersion, title, ipaName, file_path)

                for d in os.listdir(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app_install/app'):
                    if d in ipa_package:
                        continue
                    if d.endswith('.ipa'):
                        cmd = 'rm ' + current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app_install/app/' + d
                        os.system(cmd)

            return self.xtjson.json_result(message='数据更新成功！')
        if self.action == 'uploadApp':
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            if not fext.endswith('ipa'):
                return self.xtjson.json_params_error('文件格式错误，只支持.ipa文件上传！')

            folder = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/app_install/app/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            _uuid = shortuuid.uuid()
            fileobj.save(folder + str(_uuid) + '.ipa')

            cmd = 'chmod 777 ' + folder + str(_uuid) + '.ipa'
            os.system(cmd)

            app_path = '/assets/app_install/app/' + str(_uuid) + '.ipa'
            self.MCLS.update_site_config()
            res = self.get_mobileprovision(app_path)
            return self.xtjson.json_result(message=app_path)
        if self.action == 'check_ipa_signature':
            ipa_path = self.request_data.get('ipa_path')
            if not ipa_path:
                return self.xtjson.json_params_error('检测失败！缺少文件路径！')
            _path = current_app.root_path + '/' + self.project_static_folder + ipa_path
            if not os.path.exists(_path):
                return self.xtjson.json_params_error('检测失败！文件不存在！')
            decompress_folder = current_app.root_path + '/' + self.project_static_folder + '/assets/uncompress/' + str(int(time.time() * 1000))
            if not os.path.exists(decompress_folder):
                os.makedirs(decompress_folder)
            state, res = IpaSignatureChwckCls().main(ipa_path=_path, decompress_folder=decompress_folder)
            cmd = 'rm -rf ' + decompress_folder
            os.popen(cmd)
            if state:
                return self.xtjson.json_result(message=res)
            return self.xtjson.json_params_error(res)
        if self.action == 'checkMobileprovision':
            pass

class ProductView(CmsFormViewBase):
    title = '产品'
    show_menu = False
    add_url_rules = [['/product/', 'product']]
    template = 'cms/product.html'
    MCLS = ProductModel

    def view_get(self):
        documents = self.MCLS.find_all()
        data = [doc for doc in documents]

        self.context['title'] = self.title
        self.context['configData'] = SITE_CONFIG_CACHE
        self.context['products'] = data
        return render_template(self.template, **self.context)
    
    def post_other_way(self):
        if self.action == 'uploadProductImg':
            fileobj = request.files.get('upload')
            if not fileobj:
                return self.xtjson.json_params_error()
            fname, fext = os.path.splitext(fileobj.filename)
            folder = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/product/'
            if not os.path.exists(folder):
                os.makedirs(folder)

            _uuid = shortuuid.uuid()
            filename = folder + _uuid + fext
            fileobj.save(filename)
            _path = filename.replace(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME'), '')
            return self.xtjson.json_result(message=_path)
        
        if self.action == 'uploadProductDetailImg':
            fileobj = request.files.get('upload')
            if not fileobj:
                return self.xtjson.json_params_error()
            fname, fext = os.path.splitext(fileobj.filename)
            folder = current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME') + '/assets/product/'
            if not os.path.exists(folder):
                os.makedirs(folder)

            _uuid = shortuuid.uuid()
            filename = folder + _uuid + fext
            fileobj.save(filename)
            _path = filename.replace(current_app.static_folder + '/' + current_app.config.get('PROJECT_NAME'), '')
            return self.xtjson.json_result(message=_path)
        
        if  self.action == 'updateProduct':
            name = self.request_data.get('name')
            url = self.request_data.get('url')
            img = self.request_data.get('img')
            detailImg = self.request_data.get('detailImg')
            message = self.request_data.get('message')
            until = self.request_data.get('until')
            date = self.request_data.get('date')

            print(detailImg)
            _c = {}

            _c['name'] = name or ''
            _c['url'] = url or ''
            _c['img'] = "/static/" + current_app.config.get('PROJECT_NAME') + img or ''
            _c['detailImg'] = "/static/" + current_app.config.get('PROJECT_NAME') + detailImg or ''
            _c['message'] = message or ''
            _c['until'] = until
            _c['date'] = date or ''

            self.MCLS.save(_c)
            self.MCLS.update_product()

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'deleteProduct':
            uuid = self.request_data.get('uuid')

            self.MCLS.delete_one({"uuid": uuid})

            return self.xtjson.json_result(message='数据更新成功！')
    
class AccessLogView(CmsFormViewBase):
    title = '访问日志'
    show_menu = False
    add_url_rules = [['/log/', 'access_log']]
    template = 'cms/accessLog.html'
    MCLS = AccessLogModel

    def view_get(self):
        documents = self.MCLS.find_all()
        data = [doc for doc in documents]

        self.context['title'] = self.title
        self.context['configData'] = SITE_CONFIG_CACHE
        self.context['logs'] = data
        return render_template(self.template, **self.context)
    
class UserView(CmsFormViewBase):
    title = '网站用户'
    show_menu = False
    add_url_rules = [['/user/', 'user']]
    template = 'cms/user.html'
    # MCLS = AccessLogModel

    def view_get(self):
        ipBlackDocument = IpBlackModel.find_all()
        ipBlackList = [doc for doc in ipBlackDocument]

        accountBlackDocument = AccountBlackModel.find_all()
        accountBlackList = [doc for doc in accountBlackDocument]

        systemWhiteDocument = SystemWhiteModel.find_all()
        systemWhiteList = [doc for doc in systemWhiteDocument]

        cmsUserDocument = CmsUserModel.find_all()
        cmsUserList = [doc for doc in cmsUserDocument]

        self.context['title'] = self.title
        self.context['configData'] = SITE_CONFIG_CACHE
        self.context['ipBlackList'] = ipBlackList
        self.context['accountBlackList'] = accountBlackList
        self.context['systemWhiteList'] = systemWhiteList
        self.context['userList'] = cmsUserList
        return render_template(self.template, **self.context)
    
    def post_other_way(self):
        if  self.action == 'createIpBlack':
            ip = self.request_data.get('ip')
            description = self.request_data.get('description')
            date = self.request_data.get('date')

            _c = {}

            _c['ip'] = ip or ''
            _c['description'] = description or ''
            _c['date'] = date or ''

            IpBlackModel.insert_one(_c)

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'deleteIpBlack':
            uuid = self.request_data.get('uuid')

            IpBlackModel.delete_one({"uuid": uuid})

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'createAccountBlack':
            accout = self.request_data.get('account')
            description = self.request_data.get('description')
            date = self.request_data.get('date')

            _c = {}

            _c['account'] = accout or ''
            _c['description'] = description or ''
            _c['date'] = date or ''

            AccountBlackModel.insert_one(_c)

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'deleteAccountBlack':
            uuid = self.request_data.get('uuid')

            AccountBlackModel.delete_one({"uuid": uuid})

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'createSystemWhite':
            ip = self.request_data.get('ip')
            description = self.request_data.get('description')
            date = self.request_data.get('date')

            _c = {}

            _c['ip'] = ip or ''
            _c['description'] = description or ''
            _c['date'] = date or ''

            SystemWhiteModel.insert_one(_c)

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'deleteSystemWhite':
            uuid = self.request_data.get('uuid')

            SystemWhiteModel.delete_one({"uuid": uuid})

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'createUser':
            account = self.request_data.get('account')
            name = self.request_data.get('name')
            permission = self.request_data.get('permission')
            date = self.request_data.get('date')

            _c = {}

            _c['login_account'] = account or ''
            _c['username'] = name or ''
            _c['permissions'] = [permission] or []
            _c['password'] = "admin"
            _c['create_time'] = datetime.utcnow()

            CmsUserModel.insert_one(_c)

            return self.xtjson.json_result(message='数据更新成功！')
        
        if  self.action == 'deleteUser':
            account = self.request_data.get('account')

            CmsUserModel.delete_one({"login_account": account})

            return self.xtjson.json_result(message='数据更新成功！')