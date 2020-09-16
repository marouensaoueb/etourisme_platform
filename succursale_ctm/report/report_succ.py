# -*- coding: utf-8 -*-

import logging

from odoo import models, fields

# Get the logger
_logger = logging.getLogger(__name__)


class WizardReturnReports(models.Model):
    _name = 'wizard.succ_report'

    report_type = fields.Selection(selection=[('1', 'Rapport succursale'), ('2', 'Rapport succursale par produit')])

    def get_report(self):
        cam = 0
        mg = 0
        tpl = []
        obj = {

        }
        tpl.append(obj)
        return {
            'data': {'cam': 0, 'mg': 0, 'tpl': tpl},
            'type': 'ir.actions.report',
            'report_name': 'succursale_ctm.succ_report',
            'report_type': 'qweb-pdf',
            'name': 'succursale_ctm.succ_report',
        }
