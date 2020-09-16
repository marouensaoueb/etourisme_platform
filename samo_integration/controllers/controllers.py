# -*- coding: utf-8 -*-
from odoo import http


# class SamoIntegration(http.Controller):
#     @http.route('/samo_integration/samo_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"
#
#     @http.route('/samo_integration/samo_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('samo_integration.listing', {
#             'root': '/samo_integration/samo_integration',
#             'objects': http.request.env['samo_integration.samo_integration'].search([]),
#         })
#
#     @http.route('/samo_integration/samo_integration/objects/<model("samo_integration.samo_integration"):obj>/',
#                 auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('samo_integration.object', {
#             'object': obj
#         })
