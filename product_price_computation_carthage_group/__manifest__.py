# -*- coding: utf-8 -*-
{
    'name': "product_price_computation_carthage_group",

    'summary': """
        """,

    'description': """
     
    """,

    'author': "CARTHAGE GROUP",
    'website': "carthage.group",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'application',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ctm_accounting','website','mail','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'datas/accomodations.xml',
        'views/views.xml',
        'views/templates.xml',
        'wizards/wizards.xml',
        'front/main_interfaces.xml',
        'front/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
