# -*- coding: utf-8 -*-
{
    'name': "ctm_fleet",

    'summary': """
        Parc automobile pour CTM voyages""",

    'description': """
      extention pour Gestion de parc automobile pou une agence de  voyages
    """,

    'author': "CTM voyages by Aouili nizar",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/hacks.xml',
        'reports/report_templates.xml',
        'reports/report.xml',

        'wizards/wizards.xml'


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
