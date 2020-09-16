# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.exceptions import UserError


class VenteExcursionrecap(models.TransientModel):
    _name = 'wizard.venterecap'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def get_report_recap(self):
        # traitement pour devise dollar
        list_ventes_dolar = self.env['excursion.reservations'].search(
            [('dat', '<=', self.date_to), ('dat', '>=', self.date_from), ('state', '=', 'cnf'),
             ('currency_id', '=', 2)])
        tab_exc_dolar = []
        vente_detail_dolar = []
        tot_dolar = 0
        for x in list_ventes_dolar:
            if x.excursion_id not in tab_exc_dolar:
                tab_exc_dolar.append(x.excursion_id)
        for y in tab_exc_dolar:
            somme_vente_dolar = 0
            somme_avoir_dolar = 0
            list_vente_dolar = self.env['excursion.reservations'].search(
                [('dat', '<=', self.date_to), ('dat', '>=', self.date_from), ('state', '=', 'cnf'),
                 ('excursion_id', '=', y.id)])
            for z in list_vente_dolar:
                somme_vente_dolar = somme_vente_dolar + z.selling_price
                somme_avoir_dolar = somme_avoir_dolar + z.avoir_amount
            tot_dolar = tot_dolar + (somme_vente_dolar - somme_avoir_dolar)
            obj_dolar = {
                'excursion_name': y.name,
                'somme_vente': somme_vente_dolar,
                'somme_avoir': somme_avoir_dolar
            }
            vente_detail_dolar.append(obj_dolar)
        # traitement pour devise dinar
        list_ventes_dinar = self.env['excursion.reservations'].search(
            [('dat', '<=', self.date_to), ('dat', '>=', self.date_from), ('state', '=', 'cnf'),
             ('currency_id', '=', 133)])
        tab_exc_dinar = []
        vente_detail_dinar = []
        tot_dinar = 0
        for x in list_ventes_dinar:
            if x.excursion_id not in tab_exc_dinar:
                tab_exc_dinar.append(x.excursion_id)
        for y in tab_exc_dinar:
            somme_vente_dinar = 0
            somme_avoir_dinar = 0
            list_vente_dinar = self.env['excursion.reservations'].search(
                [('dat', '<=', self.date_to), ('dat', '>=', self.date_from), ('state', '=', 'cnf'),
                 ('excursion_id', '=', y.id)])
            for z in list_vente_dinar:
                somme_vente_dinar = somme_vente_dinar + z.selling_price
                somme_avoir_dinar = somme_avoir_dinar + z.avoir_amount
            tot_dinar = tot_dinar + (somme_vente_dinar - somme_avoir_dinar)
            obj1 = {
                'excursion_name': y.name,
                'somme_vente': somme_vente_dinar,
                'somme_avoir': somme_avoir_dinar
            }
            vente_detail_dinar.append(obj1)
        if len(vente_detail_dolar) == 0 and len(vente_detail_dinar) == 0:
            raise UserError('aucune vente pour ces critères')
        return {
            'data': {'total_vente_dolar': tot_dolar,
                     'total_vente_dinar': tot_dinar,
                     'date_from': self.date_from,
                     'date_to': self.date_to,
                     'listevente_dolar': vente_detail_dolar,
                     'listevente_dinar': vente_detail_dinar},
            'type': 'ir.actions.report',
            'report_name': 'excursion.venterecap_excursion',
            'report_type': 'qweb-pdf',
            'name': 'Analyse des vente recap',
        }
