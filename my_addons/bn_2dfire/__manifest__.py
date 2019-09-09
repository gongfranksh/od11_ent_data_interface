# -*- coding: utf-8 -*-
{
    'name': "bn_2dfire",

    'summary': """
                    二维火系统数据接口
                    """,

    'description': """
                    二维火系统数据接口
    """,

    'author': "weiliang",
#    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'data interface',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product','point_of_sale'],

    # always loaded
    'data': [
        'security/security.xml',
        'data/business_data.xml',
        'data/company_data.xml',
        'data/2dfire_data.xml',
        'data/2dfire_data_branch.xml',
        'data/2dfire_data_api_url.xml',
        'data/user_data.xml',
        'views/views.xml',
        'views/proc_sync_2dfire.xml',
        'views/bn_2dfire_branches.xml',
        'views/bn_2dfire_shops.xml',
        'views/bn_2dire_comm.xml',
        'views/bn_2dire_order.xml',
        'views/templates.xml',
        'views/pos_order_view.xml',
        'views/bn_2dfire_onboarding_templates.xml',
        'views/bn_2dfire_binding_branches_wizard.xml',
        'security/ir.model.access.csv',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}