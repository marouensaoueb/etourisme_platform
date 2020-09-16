# -*- coding: utf-8 -*-
from odoo import http

# class ProgrammeDeFideliteNovostar(http.Controller):
#     @http.route('/programme_de_fidelite_novostar/programme_de_fidelite_novostar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/programme_de_fidelite_novostar/programme_de_fidelite_novostar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('programme_de_fidelite_novostar.listing', {
#             'root': '/programme_de_fidelite_novostar/programme_de_fidelite_novostar',
#             'objects': http.request.env['programme_de_fidelite_novostar.programme_de_fidelite_novostar'].search([]),
#         })

#     @http.route('/programme_de_fidelite_novostar/programme_de_fidelite_novostar/objects/<model("programme_de_fidelite_novostar.programme_de_fidelite_novostar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('programme_de_fidelite_novostar.object', {
#             'object': obj
#         })