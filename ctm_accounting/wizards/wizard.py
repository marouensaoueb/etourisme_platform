# -*- coding: utf-8 -*-
import datetime
import logging
from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SiYoussef(models.Model):
    _name = 'early.booking'
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    type_reduction = fields.Char('Type de Reduction ')
    taux = fields.Float('Taux de reduction ', digits=(10, 3))
    creaton_from = fields.Date('debut de Creation')
    creation_to = fields.Date('Fin de Creation')
    checkin_from = fields.Date('Debut de Checkin')
    checkin_to = fields.Date('Fin de Checkin')

    # pr_payer = fields.Selection(selection=[('50%', '50%'), ('100%', '100%')], string="pourcentage à payer")

    def appliquer_early_booking(self):
        domain = []
        domain.append(('hotel_id', '=', self.hotel_id.id))
        domain.append(('creation_date', '>=', self.creaton_from))
        domain.append(('creation_date', '<=', self.creation_to))
        domain.append(('chekin', '>=', self.checkin_from))
        domain.append(('chekin', '<=', self.checkin_to))
        rec = self.env['ctm.reservation.list'].search(domain)
        sum = 0
        for line in rec:
            sum = sum + line.brut
        sum_ap = sum * (100 - self.taux) / 100
        self.env['etat.early.booking'].create({
            'type_reduction': self.type_reduction,
            'hotel_id': self.hotel_id.id,
            'taux': self.taux,
            'creaton_from': self.creaton_from,
            'creation_to': self.creation_to,
            'checkin_from': self.checkin_from,
            'checkin_to': self.checkin_to,
            'montant_total': sum,
            'montant_apayer': sum_ap,
        })
        return {

            'type': 'ir.actions.act_window',

            'name': 'Etat booking',

            'view_mode': 'tree,form,pivot',

            'res_model': 'etat.early.booking',


            'target': 'current',

        }

    @api.multi
    def correct_ages(self):
        # for x in self.env['rooming.list'].search([]):
        #     date_naiss = x.datenaiss
        #     years = relativedelta(x.checkin,
        #                               x.datenaiss).years
        #     months = relativedelta(x.checkin,
        #                                x.datenaiss).months
        #
        #     age = years + (months/12)
        #     x.write({
        #             'age': age
        #         })
        # for y in self.env['ctm.reservation.list'].search([]):
        #     recs = self.env['rooming.list'].search([('num_reser', '=', y.reservation_number)])
        #     for x in recs:
        #         x.write({
        #             'reservation_list_id': y.id
        #         })
        for k in self.env['ctm.reservation.list'].search([('chekin','>=','01/11/2018')]):
            little_list = self.env['rooming.list'].search([('num_reser', '=', k.reservation_number)])
            k.bebe = 0
            k.pax_adult = 0
            k.pax_enfant = 0
            for y in little_list:
                contract_id = self.env['contract.contract'].search(
                    [('hotel', '=', k.hotel_id.id), ('date_start', '<=', k.chekin),
                     ('date_end', '>=', k.chekin)])

                if len(contract_id) ==1 :
                    if 2 <= y.age < contract_id.min_adult_age:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < contract_id.min_enf_age:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1
                elif len(contract_id) >1:
                    contract_id = contract_id[0]
                    if 2 <= y.age < contract_id.min_adult_age:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < contract_id.min_enf_age:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1
                else:
                    if 2 <= y.age < 12:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < 2:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1




class EatatEarlyBooking(models.Model):
    _name = 'etat.early.booking'
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    type_reduction = fields.Char('Type de Reduction ')
    taux = fields.Float('Taux de reduction ', digits=(10, 3))
    creaton_from = fields.Date('debut de Creation')
    creation_to = fields.Date('Fin de Creation')
    checkin_from = fields.Date('Debut de Checkin')
    checkin_to = fields.Date('Fin de Checkin')
    montant_total = fields.Float('Montant Total ', digits=(10, 3))
    montant_apayer = fields.Float('Montant à payer ', digits=(10, 3))
