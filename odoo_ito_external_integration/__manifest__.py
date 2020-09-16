# -*- coding: utf-8 -*-
{
    'name': "odoo_ito_external_integration",

    'summary': """
        Provide external independed integration between ito and odoo system""",

    'description': """
        Using pyodbc as a library to connect to MS Sql server we create some requests to import 
        the rooming list ocassionnally from ITO system
    """,

    'author': "Carthage tourism and mice by Aouili nizar",
    'website': "http://www.ctmvoyages.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ctm_accounting','excursion'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
