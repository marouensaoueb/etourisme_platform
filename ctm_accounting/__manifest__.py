# -*- coding: utf-8 -*-
{
    'name': "ctm_accounting",

    'summary': """
        Tunisian accounting and tools for CTM""",

    'description': """
        Functionnalities : 
        - valorisation des reservations
        - gestion et generalisation des la liste de fidélité des reservation.
    """,

    'author': "Ctm voyages",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/views.xml',
        'views/templates.xml',
        'views/contract_management.xml',
        'wizards/wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',

    ],
}