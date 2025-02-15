# -*- coding:utf-8 -*-
from views.cms_views import bp as cms_bp
from views.api_views import bp as api_bp
from views.front_views import bp as front_bp
from views.common_views import bp as common_bp
from views.common_views.common_view import img_cap

from views.cms_views.cms_view import CmsIndexView, SystemConfigView, AccessLogView, ProductView, UserView
from views.cms_views.cms_login import CmsLogin, CmsLoginOut
from views.cms_views.cms_user import CmsUserView, CmsUserCenterView

from views.api_views import api_view
from views.front_views.front_view import FrontIndex, AppView, InstallView, AppInatallView, IOSView, DashboardView, DashboardMobileView, DetailView, MbDetailView

CMS_VIEWS = [
    CmsIndexView, CmsLogin, CmsLoginOut, CmsUserView, CmsUserCenterView, SystemConfigView, AccessLogView, ProductView, UserView
]

API_VIEWS = [
]

FRONT_VIEWS = [
    FrontIndex, AppView, InstallView, AppInatallView, IOSView, DashboardView, DashboardMobileView, DetailView, MbDetailView
]

for view_cls in CMS_VIEWS:
    if not hasattr(view_cls, 'add_url_rules'):
        continue
    if not getattr(view_cls, 'add_url_rules'):
        continue
    for rule in view_cls.add_url_rules:
        try:
            cms_bp.add_url_rule(rule[0], view_func=view_cls.as_view(rule[1]))
        except Exception as e:
            print(f'{view_cls.__name__}  error:', e)
            exit()

for view_cls in API_VIEWS:
    if not hasattr(view_cls, 'add_url_rules'):
        continue
    if not getattr(view_cls, 'add_url_rules'):
        continue
    for rule in view_cls.add_url_rules:
        try:
            api_bp.add_url_rule(rule[0], view_func=view_cls.as_view(rule[1]))
        except Exception as e:
            print(f'{view_cls.__name__}  error:', e)
            exit()

for view_cls in FRONT_VIEWS:
    if not hasattr(view_cls, 'add_url_rules'):
        continue
    if not getattr(view_cls, 'add_url_rules'):
        continue
    for rule in view_cls.add_url_rules:
        try:
            front_bp.add_url_rule(rule[0], view_func=view_cls.as_view(rule[1]))
        except Exception as e:
            print(f'{view_cls.__name__}  error:', e)
            exit()

