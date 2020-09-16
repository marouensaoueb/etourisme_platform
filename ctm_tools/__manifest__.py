# -*- coding: utf-8 -*-
{
    'name': "ctm_tools",

    'summary': """
        Short tools for ctm employees""",

    'description': """
        tools in package : 
            * fleet program extention
            * base for excurtion and transport management   
    """,

    'author': "Nizar aouili by Carthage tourism ans Mice",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','ctm_accounting'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/paperwork.xml',
        'views/templates.xml',
        'report/paperwork_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}
