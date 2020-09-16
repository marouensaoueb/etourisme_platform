# -*- coding: utf-8 -*-


from odoo import models, fields


class ReportLiquidation(models.Model):
    _name = 'liquidation.report'
    _rec_name = 'sequence_number'

    sequence_number = fields.Char('Reference')
    liquidation_date = fields.Date('Date liquidation')
    creation_user = fields.Many2one('res.users',string="Creation user")
    creation_dat = fields.Date('Creation date')
    guide_id = fields.Many2one('excursion.guide', string='Guide')
    avoir_detail = fields.One2many('excursion.avoir', 'liquidation_report_id', string="Detail avoir")
    ticket_detail = fields.One2many('excursion.reservations', 'liquidation_report_id', string="Liquidation details")
    total_devise = fields.One2many('liquidation.devise.totals', 'liquidation_report_id', string="Totale devises")


class ReservAvoir(models.Model):
    _name = "excursion.avoir"

    avoir_date = fields.Date('Date avoir')
    avoir_amount = fields.Monetary('Montant avoir')
    ticket_id = fields.Many2one('excursion.reservations', string='Ticket')
    liquidation_report_id = fields.Many2one('liquidation.report', string="report")
    currency_id = fields.Many2one('res.currency', string="Currency")


class DevisesTotals(models.Model):
    _name = 'liquidation.devise.totals'

    currency_id = fields.Many2one('res.currency', string="Devise")
    amount = fields.Monetary('Amount')
    liquidation_report_id = fields.Many2one('liquidation.report', string="report")


class ExcInh(models.Model):
    _inherit = 'excursion.reservations'

    liquidation_report_id = fields.Many2one('liquidation.report', string="report")
