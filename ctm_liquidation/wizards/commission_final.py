# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CommissionfinalReport(models.TransientModel):
    _name = 'wizard.comm_final_report'

    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    guides = fields.Many2many('excursion.guide', string="Represntants")

    @api.constrains('date_from', 'date_to')
    def check_date(self):
        if self.date_from.day != 21 and self.date_from.day != 29 and self.date_to.day != 20:
            raise UserError('Error in date , it myst be between 21 or 29 and 20 ')

    def get_report(self):
        # table encaissement representant
        encaisement = []
        for x in self.guides:
            excursions = self.env['excursion.reservations']

        return {

            'data': {'d1': self.date_from, 'd2': self.date_to},
            'type': 'ir.actions.report',
            'report_name': 'ctm_liquidation.com_final_report',
            'report_type': 'qweb-pdf',
            'name': 'Commissions des reps',
        }



