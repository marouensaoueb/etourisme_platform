# -*- coding: utf-8 -*-
from odoo import http

# class SuccursaleCtm(http.Controller):
#     @http.route('/succursale_ctm/succursale_ctm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/succursale_ctm/succursale_ctm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('succursale_ctm.listing', {
#             'root': '/succursale_ctm/succursale_ctm',
#             'objects': http.request.env['succursale_ctm.succursale_ctm'].search([]),
#         })

#     @http.route('/succursale_ctm/succursale_ctm/objects/<model("succursale_ctm.succursale_ctm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('succursale_ctm.object', {
#             'object': obj
#         })