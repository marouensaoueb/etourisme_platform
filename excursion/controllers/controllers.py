# -*- coding: utf-8 -*-
from odoo import http

# class Excursion(http.Controller):
#     @http.route('/excursion/excursion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/excursion/excursion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('excursion.listing', {
#             'root': '/excursion/excursion',
#             'objects': http.request.env['excursion.excursion'].search([]),
#         })

#     @http.route('/excursion/excursion/objects/<model("excursion.excursion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('excursion.object', {
#             'object': obj
#         })