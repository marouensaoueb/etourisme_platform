# -*- coding: utf-8 -*-
{
    'name': "succursale_ctm",

    'summary': """
        Controle de gestion pour les succursales CTM""",

    'description': """
        ce module va contenir la resumé de l'activité des agences succursales pour des besoins de calcul de la rentabilité 
        , efficacité , etc... 
    """,

    'author': "Carthage Group by Aouili nizar",
    'website': "http://www.carthage.group",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report_succ_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}