# -*- coding: utf-8 -*-
from odoo import http

# class OdooItoExternalIntegration(http.Controller):
#     @http.route('/odoo_ito_external_integration/odoo_ito_external_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_ito_external_integration/odoo_ito_external_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_ito_external_integration.listing', {
#             'root': '/odoo_ito_external_integration/odoo_ito_external_integration',
#             'objects': http.request.env['odoo_ito_external_integration.odoo_ito_external_integration'].search([]),
#         })

#     @http.route('/odoo_ito_external_integration/odoo_ito_external_integration/objects/<model("odoo_ito_external_integration.odoo_ito_external_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_ito_external_integration.object', {
#             'object': obj
#         })