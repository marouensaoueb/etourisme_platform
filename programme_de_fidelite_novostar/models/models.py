# -*- coding: utf-8 -*-
import datetime
import logging
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import tools

_logger = logging.getLogger(__name__)

class SubscriptionConf(models.Model):
    _name = 'ctm.subscription.conf'
    _rec_name = 'name'

    num = fields.Integer('Subscription Min')
    name = fields.Char('Subscription name')

class ClientsSbscription(models.Model):
    _name = 'ctm.clients.subscription'

    generated_subscriptions = fields.One2many('ctm.clients.subscription.generated', 'client_sub_id',
                                              string="Generated subscryptions")

    @api.multi
    def generate_subscription(self):
        rooming_list = self.env['rooming.list'].search([])
        result = []
        dates = []
        obj = {}
        cpt = 0
        subs = 0
        max = 0
        for x in rooming_list:
            subs = 0
            max = 0
            dates = []
            hots = []
            cpt = len(self.env['rooming.list'].search([('client_name', '=', x.client_name)]))
            # getting the subscription
            for y in self.env['ctm.subscription.conf'].search([]):
                if cpt >= y.num and y.num >= max:
                    max = y.num
                    subs = y.id
            if len(self.env['ctm.clients.subscription.generated'].search([('client', '=', x.client_name)])) == 0:
                all_x_occ = self.env['rooming.list'].search([('client_name', '=', x.client_name)])
                if len(all_x_occ) > 0:

                    for x_occ in all_x_occ:
                        dates.append(datetime.datetime.strftime(x_occ.checkout, '%Y-%m-%d'))
                        if x_occ.hotel.id not in hots:
                            hots.append(x_occ.hotel.id)
                    kond = self.env['ctm.clients.subscription.generated'].create({
                        'client': x.client_name,
                        'sub': subs,
                        'num': cpt,
                        'check_out': str(dates),
                        'datenaiss': x.datenaiss,
                        'age': x.age,
                        'tour_operator': x.tour_operator,
                        'status': x.status,
                        'client_sub_id': self.id
                    })
                    for ho in hots:
                        if ho:
                            self._cr.execute(
                                "insert into ctm_clients_subscription_generated_rooming_hotels_rel (ctm_clients_subscription_generated_id , rooming_hotels_id) values({0},{1})".format(
                                    kond.id, ho))

class clientsSfghfhjbscription(models.Model):
    _name = 'ctm.clients.subscription.generated'
    _rec_name = 'client'

    client = fields.Char(string="client name")
    sub = fields.Many2one('ctm.subscription.conf', string='Subscription type')
    age = fields.Integer('Age')
    datenaiss = fields.Date('Date naissance')
    check_out = fields.Char('Check In')
    num = fields.Integer('Number of the total reservation')
    hotel = fields.Many2many('rooming.hotels', string='Hotel')
    tour_operator = fields.Char('Tour Opertor')
    client_sub_id = fields.Many2one('ctm.clients.subscription')
    status = fields.Char('Status')