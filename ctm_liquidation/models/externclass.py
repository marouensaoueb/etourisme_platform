# -*- coding: utf-8 -*-


from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import tools


class Camel(models.Model):
    _name = "liquidation.camel"
    _rec_name = "dat"
    _description = "les Ecursion de type Camel"
    _auto = False
    _order = 'date desc'

    dat = fields.Date("Excursion date")
    # excursion_id = fields.Many2one('excursion.excursion', string="Excursion name")
    adulte = fields.Integer('Adulte')
    enfant = fields.Integer('Chd')
    inf = fields.Integer('Inf')
    tour_operateur = fields.Many2one('tour.operator', string='Tour operator')
    booking_number = fields.Many2one('rooming.list', string='Booking number')
    ticket_number = fields.Char('Ticket number ')
    vendeur_id = fields.Many2one('excursion.guide', string='Seller name')
    selling_price = fields.Float('Selling price', digits=(10, 3))
    seller_commission = fields.Float('Seller commission', digits=(10, 3))
    paid_sum = fields.Float('Paid sum', digits=(10, 3))
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    room_nbr = fields.Char('Room Nr.')
    liquidation = fields.Boolean('Liquidation')
    doc_nbr = fields.Char('Document Nr.')

    @api.model_cr
    def init(self):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW liquidation_camel as (
            select id, 
       dat,
            adulte ,
            enfant, 
            inf,
            tour_operateur,
            booking_number,
            ticket_number,
            vendeur_id,
            selling_price
           ,seller_commission,
           paid_sum,
           hotel_id,
           room_nbr,
           liquidation,
           doc_nbr
           from excursion_extra
           where excursion_id = ( select id from excursion_excursion where type_excursion_camel = TRUE ))""")


class QuatreFoisQuatre(models.Model):
    _name = "liquidation.quatre.fois.quatre"
    _rec_name = "dat"
    _description = "les Ecursion de type 4*4 "
    _auto = False
    _order = 'date desc'

    dat = fields.Date("Excursion date")
    # excursion_id = fields.Many2one('excursion.excursion', string="Excursion name")
    adulte = fields.Integer('Adulte')
    enfant = fields.Integer('Chd')
    inf = fields.Integer('Inf')
    tour_operateur = fields.Many2one('tour.operator', string='Tour operator')
    booking_number = fields.Many2one('rooming.list', string='Booking number')
    ticket_number = fields.Char('Ticket number ')
    vendeur_id = fields.Many2one('excursion.guide', string='Seller name')
    selling_price = fields.Float('Selling price', digits=(10, 3))
    seller_commission = fields.Float('Seller commission', digits=(10, 3))
    paid_sum = fields.Float('Paid sum', digits=(10, 3))
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    room_nbr = fields.Char('Room Nr.')
    liquidation = fields.Boolean('Liquidation')
    doc_nbr = fields.Char('Document Nr.')

    @api.model_cr
    def init(self):
        # self._table = account_invoice_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW liquidation_quatre_fois_quatre as (
            select id, 
            dat ,
            adulte ,
            enfant, 
            inf,
            tour_operateur,
            booking_number,
            ticket_number,
            vendeur_id,
            selling_price
           ,seller_commission,
           paid_sum,
           hotel_id,
           room_nbr,
           liquidation,
           doc_nbr
           from excursion_extra
           where excursion_id in ( select id from excursion_excursion where type_excursion_q_f_q = TRUE ))""")
