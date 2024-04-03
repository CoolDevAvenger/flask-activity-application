# -*- coding: utf-8 -*-
from flask import render_template
from .cms_base import CmsTableViewBase, CmsFormViewBase
from models.cms_user import CmsUserModel
from constants import PermissionType


class CmsUserView(CmsTableViewBase):
    MCLS = CmsUserModel
    title = '管理员列表'
    add_url_rules = [['/cms_user/', 'cms_user']]
    template = 'cms/site_config/admin_list.html'
    permission_map = [PermissionType.ACCESS, PermissionType.ADD, PermissionType.EDIT, PermissionType.DELETE]

    def _get_permission(self, user_cls):
        html = '<div id="permission_div">'
        html += '<table class="table table-bordered table-hover text-center">'
        html += '<thead class="thead-light"><tr>'
        html += '<th>菜单名</th>'
        html += '<th>拥有权重</th>'
        html += '</tr></thead>'
        html += '<tbody>'
        if self.check_superdamin(self.data_dict.get('permissions')):
            html += '<tr>'
            html += '<td>最高权限</td>'
            html += '<td align="left"><span class="btn btn-success btn-xs"><i class="bi-check-circle-fill"></i>&ensp;superAdmin</span></td>'
            html += '</tr>'
        # menu_datas = CmsMenuModel.find_many({}, sort=[['inedx', 1]])
        # for menu_data in menu_datas:
        #     html += '<tr>'
        #     html += '<td>%s</td>' % menu_data.get('text')
        #     html += '<td align="left">'
        #     for per in menu_data.get('permissions'):
        #         if per[0] in self.data_dict.get('permissions') and not user_cls.is_superadmin:
        #             html += f"""<span class="btn btn-success btn-xs" onclick="update_permission('{self.data_dict.get('uuid')}', '{per[0]}')"><i class="bi-check-circle-fill"></i>&ensp;{per[-1]}</span> """
        #         else:
        #             html += f"""<span class="btn btn-default btn-xs" onclick="update_permission('{self.data_dict.get('uuid')}', '{per[0]}')">{per[-1]}</span> """
        #     html += '</td></tr>'
        html += '</tbody>'
        html += '</table></div>'
        return self.xtjson.json_result(message=html)

    def post_data_del(self):
        if self.check_superdamin(self.data_dict.get('permissions')):
            return self.xtjson.json_params_error('最高管理员不可删除!')
        self.MCLS.delete_one(self.data_dict)
        return self.xtjson.json_result()

    def post_add_data(self, data_form):
        if self.MCLS.count({'telephone': data_form.get('telephone')}):
            return self.xtjson.json_params_error('该手机号已注册!')
        data_form['password'] = self.MCLS.encry_password(data_form.get('password'))
        data_form['statu'] = 1
        data_form['permissions'] = []
        data_form['_current_login'] = ''
        self.MCLS.insert_one(data_form)
        return self.xtjson.json_result()

    def post_data_other_way(self):
        user_cls = self.MCLS.query_one({'uuid': self.data_uuid})
        if self.action == '_cat_info':
            html = '<table class="table table-bordered text-center">'
            html += '<tbody style="font-size: 16px;">'
            html += f"""<tr><td colspan="2"><b>管理员用户:{ self.data_dict.get('telephone') }</b></td></tr>"""
            for db_fielld in ['id', 'username', 'telephone', 'statu', '_create_time', '_last_login_time', '_last_login_ip', 'note']:
                v = self.data_dict.get(db_fielld)
                field_cls = self.MCLS.fields().get(db_fielld)
                res = field_cls.transform(v)
                if db_fielld == 'statu':
                    res = '可用' if v else '不可用'
                html += f"""<tr><td><strong>{ field_cls.field_name }</strong>:</td><td align="left">{ res or '' }</td></tr>"""
            html += '</tbody></table>'
            return self.xtjson.json_result(message=html)
        if self.action == '_edit_pwd_html':
            html = f"""
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">新密码：</span>
                    </div>
                    <input type="text" class="form-control" id="new_password" placeholder="输入新密码">
                </div>         
                <div class="input-group mb-3">
                    <div class="input-group-prepend">
                        <span class="input-group-text">确认密码：</span>
                    </div>
                    <input type="text" class="form-control" id="confirm_password" placeholder="输入确认密码">
                </div>
            """
            return self.xtjson.json_result(message=html)
        if self.action == '_edit_pwd':
            new_password = self.request_data.get('new_password', '')
            confirm_password = self.request_data.get('confirm_password', '')
            if not new_password.strip() or not confirm_password.strip():
                return self.xtjson.json_params_error('操作失败!')
            self.data_dict['password'] = self.MCLS.encry_password(new_password.strip())
            self.MCLS.save(self.data_dict)
            return self.xtjson.json_result()
        if self.action == '_edit_permission_html':
            if user_cls.is_superadmin:
                return self.xtjson.json_params_error('最高管理员权限不可修改!')
            return self._get_permission(user_cls)
        if self.action == '_edit_permission':
            if user_cls.is_superadmin:
                return self.xtjson.json_params_error('最高管理员权限不可修改!')
            per = self.request_data.get('p')
            if not per:
                return self.xtjson.json_params_error('操作错误!')
            u_permissions = self.data_dict.get('permissions')
            if per in u_permissions:
                u_permissions.remove(per)
            else:
                u_permissions.append(per)
            self.data_dict['permissions'] = u_permissions
            self.MCLS.save(self.data_dict)
            return self._get_permission(user_cls)


class CmsUserCenterView(CmsFormViewBase):
    show_menu = False
    MCLS = CmsUserModel
    title = '管理员-个人中心'
    add_url_rules = [['/user_center/<string:data_uuid>/', 'user_center']]
    template = 'cms/site_config/admin_center.html'
    permission_map = [PermissionType.ACCESS, PermissionType.EDIT]

    def view_get(self, data_uuid):
        user_data = self.MCLS.find_one({'uuid': data_uuid})
        if not user_data:
            return self.xtjson.json_params_error()
        self.context['title'] = self.title
        self.context['user_data'] = user_data
        return render_template(self.template, **self.context)

    def post_data_other_way(self):
        if self.action == '_edit_user_data':
            for db_field in self.MCLS.edit_field_sort():
                field_cls = self.MCLS.fields().get(db_field)
                v = self.request_data.get(db_field)
                statu, res = field_cls.validate(v)
                if not statu:
                    return self.xtjson.json_params_error(res)
                self.data_from[db_field] = res
            self.data_dict.update(self.data_from)
            self.MCLS.save(self.data_dict)
            return self.xtjson.json_result()
        if self.action == '_edit_user_pwd':
            original_password = self.request_data.get('original_password')
            new_password = self.request_data.get('new_password')
            if not new_password:
                return self.xtjson.json_params_error()
            if not self.MCLS.check_password(self.data_dict.get('password'), original_password.strip()):
                return self.xtjson.json_params_error('原密码错误!')
            self.data_from['password'] = self.MCLS.encry_password(new_password.strip())
            self.data_dict.update(self.data_from)
            self.MCLS.save(self.data_dict)
            return self.xtjson.json_result()

