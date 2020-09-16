# -*- coding: utf-8 -*-
from odoo import http

# class CtmLiquidation(http.Controller):
#     @http.route('/ctm_liquidation/ctm_liquidation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ctm_liquidation/ctm_liquidation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ctm_liquidation.listing', {
#             'root': '/ctm_liquidation/ctm_liquidation',
#             'objects': http.request.env['ctm_liquidation.ctm_liquidation'].search([]),
#         })

#     @http.route('/ctm_liquidation/ctm_liquidation/objects/<model("ctm_liquidation.ctm_liquidation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ctm_liquidation.object', {
#             'object': obj
#         })