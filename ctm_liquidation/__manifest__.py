# -*- coding: utf-8 -*-
{
    'name': "ctm_liquidation",

    'summary': """
        liquidation for CTM""",

    'description': """
         Functionnalities :
         _calcul des commissions
         -calcul des salaires
    """,

    'author': "Ctm voyages",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ctm_accounting', 'excursion', 'ctm_fleet'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/wizards.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/thalasso.xml',

        'reports/report_templates.xml',
        'reports/liquidation_report_interface.xml',
        'reports/liquidation_report_sequence.xml',
        'reports/report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
