# -*- coding: utf-8 -*-
from odoo import http

# class CtmTools(http.Controller):
#     @http.route('/ctm_tools/ctm_tools/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctm_tools/ctm_tools/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctm_tools.listing', {
#             'root': '/ctm_tools/ctm_tools',
#             'objects': http.request.env['ctm_tools.ctm_tools'].search([]),
#         })

#     @http.route('/ctm_tools/ctm_tools/objects/<model("ctm_tools.ctm_tools"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctm_tools.object', {
#             'object': obj
#         })