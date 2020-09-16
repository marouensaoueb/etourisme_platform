# -*- coding: utf-8 -*-
from odoo import http


class MyController(http.Controller):
    @http.route('/ctm_fleet/hello', auth='user', type='json')
    def hello(self):
        return {
            'html': """
                <div>
                   
                    <h1>hello, world</h1>
                </div> """
        }
