# -*- coding: utf-8 -*-
from odoo import http

# class CtmFacturation(http.Controller):
#     @http.route('/ctm_facturation/ctm_facturation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctm_facturation/ctm_facturation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctm_facturation.listing', {
#             'root': '/ctm_facturation/ctm_facturation',
#             'objects': http.request.env['ctm_facturation.ctm_facturation'].search([]),
#         })

#     @http.route('/ctm_facturation/ctm_facturation/objects/<model("ctm_facturation.ctm_facturation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctm_facturation.object', {
#             'object': obj
#         })