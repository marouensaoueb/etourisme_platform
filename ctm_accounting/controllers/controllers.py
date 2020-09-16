# -*- coding: utf-8 -*-
from odoo import http

# class CtmAccounting(http.Controller):
#     @http.route('/ctm_accounting/ctm_accounting/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctm_accounting/ctm_accounting/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctm_accounting.listing', {
#             'root': '/ctm_accounting/ctm_accounting',
#             'objects': http.request.env['ctm_accounting.ctm_accounting'].search([]),
#         })

#     @http.route('/ctm_accounting/ctm_accounting/objects/<model("ctm_accounting.ctm_accounting"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctm_accounting.object', {
#             'object': obj
#         })