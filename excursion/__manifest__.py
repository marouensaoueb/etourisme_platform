# -*- coding: utf-8 -*-
{
    'name': "ctm_Excursion",

    'summary': """
        Module Excursion pour CTM Voyages
        """,

    'description': """
       Gestion les Excursion pour CTM Voyages
    """,

    'author': "CTM Voyages IT group",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'ctm_fleet', 'ctm_accounting', ],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/contract.xml',
        'report/report_tamplates.xml',
        'report/report.xml',
        'wizards/wizards.xml',
        'wizards/affectation.xml',
        'wizards/vente_excursion.xml',
        'views/listeReservation.xml',
        'data/sequences.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
