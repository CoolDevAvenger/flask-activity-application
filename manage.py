# -*- coding: utf-8 -*-
import os, click, time
from app_ws import app, ProjectConfig
from common_utils.lqredis import SiteRedis
from common_utils.mongodb.mongo_admin import MongoManage, CONFIG
from models.cms_user import CmsUserModel
from constants import PermissionType


@click.group()
def mainFunc():
    pass


@mainFunc.command()
@click.option('--login_account', '-t')
def init_admin(login_account):
    """ 初始化admin用户 """
    # if not login_account.strip():
    #     print('请输入手机号!')
    #     return '请输入手机号!'
    CmsUserModel.delete_many({})
    user_data = {
        'login_account': login_account.strip(),
        'password': CmsUserModel.encry_password('admin123'),
        'username': 'superadmin',
        'statu': True,
        'permissions': [PermissionType.SUPERADMIN],
        '_current_login': '',
    }
    CmsUserModel.insert_one(user_data)
    print('%s: 用户添加成功!'%login_account)
    return '%s: 用户添加成功!'%login_account


@mainFunc.command()
def init_index():
    """创建索引"""
    # for MCLS in [ZhuDanTable, ImportLogTable, SiteSettingTable, CustomerTable, BettingDataTable]:
    #     indexs = MCLS.index_information()
    #     for k, v in MCLS.fields().items():
    #         if not hasattr(v, 'is_index'):
    #             continue
    #         if not getattr(v, 'is_index'):
    #             continue
    #         if not indexs.get('%s_1' % k) and v.is_index:
    #             print(k, MCLS.create_index(k))


@mainFunc.command()
def remove_project_data():
    """清空整个项目所有数据库内的数据"""
    instruction = input('该操作会清除当前项目下所有的数据,指令（Y/N），回复确认操作Y，其它拒绝操作!')
    if instruction.strip() != 'Y':
        exit()
    for key in SiteRedis.get_keys():
        if key.decode().startswith(ProjectConfig.PROJECT_NAME):
            SiteRedis.dele(key)
    p_db = MongoManage(username=CONFIG.root_username, password=CONFIG.root_password)
    print(p_db.drop_database(ProjectConfig.MONGODB_DB))
    return '操作成功!'


@mainFunc.command()
def update_primary_key():
    """更细项目字段主键"""
    print('更新项目字段主键KEY')
    for _k in SiteRedis.get_keys():
        _k = _k.decode()
        if ProjectConfig.PROJECT_NAME in _k and '_field' in _k:
            SiteRedis.dele(_k)
    import models
    for n in dir(models):
        if n.startswith('__') or n == 'db' or n == 'dbModel' or n == 'MongoBase':
            continue
        n_f = getattr(models, n)
        for c in dir(n_f):
            if c == 'dbModel':
                continue
            MCLS = getattr(n_f, c)
            if not hasattr(MCLS, '__tablename__') or not getattr(MCLS, '__tablename__'):
                continue
            table_name = getattr(MCLS, '__tablename__')
            for db_field, v_Cls in MCLS.fields().items():
                if not hasattr(v_Cls, 'field_type'):
                    continue
                if v_Cls.primary_key:
                    v_dict = MCLS.find_one({}, sort=[[db_field, -1]])
                    if v_dict:
                        kk_v = v_dict.get(db_field) or 0
                        _redis_check_key = '%s_%s_%s_%s_field' % (ProjectConfig.PROJECT_NAME, ProjectConfig.MONGODB_DB, table_name, db_field)
                        SiteRedis.set(_redis_check_key, kk_v)
                        print(table_name, db_field, kk_v)
    print('项目字段主键KEY更新完毕！')


@mainFunc.command()
def update_secret_key():
    import base64
    from models.cms_table import SiteConfigModel
    site_data = SiteConfigModel.find_one({'project_name': app.config.get("PROJECT_NAME")}) or {}
    new_secret_key = base64.b64encode(os.urandom(66)).decode()
    site_data['secret_key'] = new_secret_key
    SiteConfigModel.save(site_data)
    print('success!')

import zipfile
def analyze_ipa_with_plistlib(ipa_path, decompress_folder):
    ipa_file = zipfile.ZipFile(ipa_path)
    ipa_file.extractall(path=decompress_folder)
    ipa_file.close()

def get_mobileprovision(ipa_path):
    project_static_folder = 'static/project_tk88'
    # _path = '/www/project_app' + '/' + project_static_folder + ipa_path
    # print(_path)
    if not os.path.exists(ipa_path):
        return
    decompress_folder = '/www/project_app' + '/' + project_static_folder + '/assets/uncompress/' + str(int(time.time() * 1000))
    if not os.path.exists(decompress_folder):
        os.makedirs(decompress_folder)
    try:
        analyze_ipa_with_plistlib(ipa_path, decompress_folder)
    except Exception as e:
        print(str(e))
        return False
    embedded_file = decompress_folder + '/Payload/DSCaipiao.app/embedded.mobileprovision'
    if not os.path.exists(embedded_file):
        embedded_file = decompress_folder + '/Payload/Live.app/embedded.mobileprovision'
    if os.path.exists(embedded_file):
        mob = '/www/project_app' + '/' + project_static_folder + '/assets/app_install/app/app.mobileprovision'
        if os.path.exists(mob):
            cmd1 = 'rm ' + mob
            os.popen(cmd1)
        cmd = 'mv %s %s' % (embedded_file, mob)
        os.popen(cmd)
    cmd = 'rm -rf ' + decompress_folder
    os.popen(cmd)
    return True

@mainFunc.command()
def edit_apache():
    dataStr = open('/etc/apache2/apache2.conf', 'r').read()
    ttt = '''<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>'''
    nnn = '''
#<Directory /var/www/>
#        Options Indexes FollowSymLinks
#        AllowOverride None
#        Require all granted
#</Directory>    
    '''
    dataStr = dataStr.replace(ttt, nnn)
    with open('/etc/apache2/apache2.conf', 'w') as wf:
        wf.write(dataStr)

@mainFunc.command()
def test1():
    dd = CmsUserModel.find_many({})
    print(dd)

if __name__ == '__main__':
    mainFunc()

