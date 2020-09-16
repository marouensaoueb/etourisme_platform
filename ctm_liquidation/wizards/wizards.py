# -*- coding: utf-8 -*-
import datetime
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CommissionReport(models.TransientModel):
    _name = 'wizard.creport'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def get_report(self):

        liste_com = []
        domain = [('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)]

        # recuperer les liste de données
        rec_chauffeur = self.env['commission.chauffeur'].search(domain)
        rec_guide_commission = self.env['commission.excursion.guide'].search(domain)
        rec_com_excursion_g_hotel = self.env['target.detail'].search(domain)
        rec_com_thalaso_g_hotel = self.env['ctm.commission.thalasso'].search(domain)
        rec_com_lagune_g_hotel = self.env['ctm.commission.lagune'].search(domain)
        rec_com_bella_m_g_hotel = self.env['ctm.commission.bella_marina'].search(domain)
        rec_com_lether_g_hotel = self.env['ctm.commission.lether_shop'].search(domain)
        rec_com_photo_g_hotel = self.env['ctm.commission.photograph'].search(domain)

        # recuperer les chiffre  d'affaire et les commission
        vente_chameaux = 0
        vente_tapis = 0
        vente_4_4 = 0
        vente_jazira = 0
        com_chameaux = 0
        com_tapis = 0
        com_4_4 = 0
        com_jazira = 0
        com_ch_chameaux = 0
        com_ch_tapis = 0
        nbr_shara = 0
        com_ch_sahra = 0
        for a in rec_chauffeur:
            b = a.detail_commission
            for c in b:
                com_ch_chameaux = com_ch_chameaux + c.commission_camel
                com_ch_tapis = com_ch_tapis + c.commission_tapis
                nbr_shara = nbr_shara + c.pax_sahara
                com_ch_sahra = com_ch_sahra + c.commission_sahara
        for x in rec_guide_commission:
            d = x.commission_detail
            for y in d:
                vente_chameaux = vente_chameaux + y.sale_camel
                vente_tapis = vente_tapis + y.sale_tapis
                vente_4_4 = vente_4_4 + y.sale_quad
                vente_jazira = vente_jazira + y.sale_oil + y.oil_oil
                com_chameaux = com_chameaux + y.commission_camel
                com_tapis = com_tapis + y.commission_tapis
                com_4_4 = com_4_4 + y.commission_quatre
                com_jazira = com_jazira + y.commission_aljazira

        chiffre_excursion_g_hotel = rec_com_excursion_g_hotel[0].sale_amount
        com_excursion_g_hotel = rec_com_excursion_g_hotel[0].commission
        chiffre_com_thalaso_g_hotel = rec_com_thalaso_g_hotel[0].sale_number
        comcom_thalaso_g_hotel = rec_com_thalaso_g_hotel[0].commission_net
        chiffre_com_lagune_g_hotel = rec_com_lagune_g_hotel[0].sale_number
        comcom_lagune_g_hotel = rec_com_lagune_g_hotel[0].commission
        chiffre_bella = rec_com_bella_m_g_hotel[0].sale_number
        com_bella_rep = rec_com_bella_m_g_hotel[0].commission
        com_bella_to = rec_com_bella_m_g_hotel[0].commission_to
        chiffre_lether = rec_com_lether_g_hotel[0].sale_number
        com_lether_rep = rec_com_lether_g_hotel[0].commission
        com_lether_to = rec_com_lether_g_hotel[0].commission_to
        chiffre_photo = rec_com_photo_g_hotel[0].sale_number
        com_photo_rep = rec_com_photo_g_hotel[0].commission
        com_photo_to = rec_com_photo_g_hotel[0].commission_to

        # taw el sapen fel liste

        com_obj = {
            'nom': 'Commission Excursion',
            'chiffre_affaire': chiffre_excursion_g_hotel,
            'com_rep': com_excursion_g_hotel,
            'com_to': '',
            'com_chauf': '',

        }
        liste_com.append(com_obj)

        com_obj_1 = {
            'nom': 'Commission Thalasso',
            'chiffre_affaire': chiffre_com_thalaso_g_hotel,
            'com_rep': comcom_thalaso_g_hotel,
            'com_to': '',
            'com_chauf': '',
        }
        liste_com.append(com_obj_1)

        com_obj_2 = {
            'nom': 'Commission Lagune',
            'chiffre_affaire': chiffre_com_lagune_g_hotel,
            'com_rep': comcom_lagune_g_hotel,
            'com_to': '',
            'com_chauf': '',
        }
        liste_com.append(com_obj_2)

        com_obj_3 = {
            'nom': 'Commission Bella Marina',
            'chiffre_affaire': chiffre_bella,
            'com_rep': com_bella_rep,
            'com_to': com_bella_to,
            'com_chauf': '',
        }
        liste_com.append(com_obj_3)

        com_obj_4 = {
            'nom': 'Commission Lether Shop',
            'chiffre_affaire': chiffre_lether,
            'com_rep': com_lether_rep,
            'com_to': com_lether_to,
            'com_chauf': '',
        }
        liste_com.append(com_obj_4)

        com_obj_5 = {
            'nom': 'Commission Photograph',
            'chiffre_affaire': chiffre_photo,
            'com_rep': com_photo_rep,
            'com_to': com_photo_to,
            'com_chauf': '',
        }
        liste_com.append(com_obj_5)

        com_obj_6 = {
            'nom': 'Commission guide excursion Chameaux',
            'chiffre_affaire': vente_chameaux,
            'com_rep': com_chameaux,
            'com_to': '',
            'com_chauf': com_ch_chameaux,
        }
        liste_com.append(com_obj_6)

        com_obj_7 = {
            'nom': 'Commission guide excursion Tapis',
            'chiffre_affaire': vente_tapis,
            'com_rep': com_tapis,
            'com_to': '',
            'com_chauf': com_ch_tapis,
        }
        liste_com.append(com_obj_7)

        com_obj_8 = {
            'nom': 'Commission guide excursion 4*4',
            'chiffre_affaire': vente_4_4,
            'com_rep': com_4_4,
            'com_to': '',
            'com_chauf': '',
        }
        liste_com.append(com_obj_8)

        com_obj_9 = {
            'nom': 'Commission guide excursion Al jazira',
            'chiffre_affaire': vente_jazira,
            'com_rep': com_jazira,
            'com_to': '',
            'com_chauf': '',
        }
        liste_com.append(com_obj_9)

        com_obj_10 = {
            'nom': 'nombre paxe sahra',
            'chiffre_affaire': nbr_shara,
            'com_rep': '',
            'com_to': '',
            'com_chauf': com_ch_sahra,
        }
        liste_com.append(com_obj_10)

        return {

            'data': {'comlist': liste_com},
            'type': 'ir.actions.report',
            'report_name': 'ctm_liquidation.com_report',
            'report_type': 'qweb-pdf',
            'name': 'Etat des Commissions',
        }


class WizardReturnReports(models.TransientModel):
    _name = 'wizard.report'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    to = fields.Many2many('tour.operator', strring="Tour operator")

    def get_reservations(self):
        # bech tejbed listet les arrivées
        rec_guide = self.env['excursion.guide'].search([('id', '=', self._context.get('active_ids'))])
        sum_pax = 0
        sum_pax_adulte = 0
        sum_pax_enfant = 0
        to_l = []
        if self.date_to < self.date_from:
            raise UserError('date to doit etre superieur ou égal à la date from')
        if len(self.env['liquidation.historiquerep'].search(
                [('date_debut', '<=', self.date_from), ('date_fin', '>=', self.date_from),
                 ('representant', 'like', rec_guide.id)])) > 0:
            raise UserError('date debut existante dans une ancienne historique ')

        if not self.to:
            all_to = self.env['tour.operator'].search([])
            for k1 in all_to:
                to_l.append(k1.id)
        else:
            for k2 in self.to:
                to_l.append(k2.id)
        pax = 0
        for k in rec_guide.details_id:
            k.unlink()
        for hotel in rec_guide.hotel_id:
            rec_reservations = self.env['ctm.reservation.list'].search(
                [('hotel_id', '=', hotel.id), ('chekin', '>=', self.date_from), ('chekin', '<=', self.date_to),
                 ('touroperator_id', 'in', to_l)], order='chekin')

            for x in rec_reservations:
                calculate = True
                for detail in x.reservation_detail:
                    if detail.status == "Cancelled":
                        calculate = False

                if calculate:
                    sum_pax_adulte = sum_pax_adulte + x.pax_adult
                    sum_pax_enfant = sum_pax_enfant + x.pax_enfant
                    pax = x.pax_adult + (x.pax_enfant / 2) if x.pax_enfant > 0 else x.pax_adult
                    sum_pax = sum_pax + pax
                    obj = {
                        'guide_id': rec_guide.id,
                        'date': x.chekin,
                        'pax': pax,
                        'hotel_id': hotel.id,
                        'enfants': x.pax_enfant,
                        'adults': x.pax_adult,
                        'bebe': x.bebe,

                    }
                    self.env['guide.hotels.detail'].create(obj)
        l = []
        l.append(rec_guide.id)
        rec = self.env['liquidation.historiquerep'].create({'representant': l})

        rec.hotel_id = rec_guide.hotel_id
        rec.date_debut = self.date_from
        rec.date_fin = self.date_to
        rec.pax = sum_pax
        rec.pax_adulte = sum_pax_adulte
        rec.pax_enfant = sum_pax_enfant
        rec.representant = l
        if not self.to:
            rec.to = []
        else:
            rec.to = to_l


class WizardReturnReports(models.TransientModel):
    _name = 'wizard.target_report'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def get_target_reservations(self):
        # get pax
        # get sale
        # calculate target
        # calculate commission z

        # control saisie
        if self.date_to < self.date_from:
            raise UserError('vérifier les dates')

        total_pax = 0
        total_sell = 0
        pax_won = 0
        rec_guide_target = self.env['etat.guide.target.commision'].search(
            [('id', '=', self._context.get('active_ids'))])
        guide = rec_guide_target.guide
        id = self._context.get('active_ids')[0]
        if len(self.env['target.detail'].search(
                [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_from), ('etat_id', '=', id)])) > 0:
            raise UserError('Dates can not intercept an old records , hotel guide already got paied for that period')
        else:
            rec_reservations = self.env['guide.hotels.detail'].search(
                [('guide_id', '=', guide.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
            for res in rec_reservations:
                total_pax = total_pax + res.pax
            rec_sell = self.env['excursion.reservations'].search(
                [('vendeur_id', '=', guide.id), ('dat', '>=', self.date_from), ('dat', '<=', self.date_to)])
            commission_rent = 0
            for s in rec_sell:
                price = self.env['liquidation.quatrefois'].search(
                    [('date_debut_saison', '<=', s.dat), ('date_fin_saison', '>=', s.dat)]).prix_vente
                if s.excursion_id.type_excursion_q_f_q:
                    total_sell = total_sell + (s.selling_price - price)
                else:
                    if s.excursion_id in self.env['excursion.excursion'].search([('type_excursion_rent', '=', True)]):
                        commission_rent = commission_rent + s.selling_price * 0.05
                    else:
                        total_sell = total_sell + s.selling_price
                    if s.adulte:
                        pax_won = pax_won + 1
                    if s.enfant:
                        pax_won = pax_won + 0.5

            target = total_sell / total_pax
            commission_chameau = 0
            commission_quatrefois = 0

            for ligne in rec_sell:
                if ligne.excursion_id in self.env['excursion.excursion'].search([('type_excursion_camel', '=', True)]):
                    config_chameau = self.env['liquidation.configchameau'].search(
                        [('date_debut_saison', '<=', ligne.dat), ('date_fin_saison', '>=', ligne.dat)])
                    commission_chameau = commission_chameau + config_chameau[0].commission_vendeur
                if ligne.excursion_id in self.env['excursion.excursion'].search([('type_excursion_q_f_q', '=', True)]):
                    commission_quatrefois = commission_quatrefois + 1

            # dolar_rate = self.env['res.currency'].search([('name', '=', 'USD')])
            #
            # target_in_dolar = target / dolar_rate.rate
            # target = target_in_dolar
            baremes = self.env['ctm.liquidation.bareme'].search(
                [('borne_inferieur', '=<', target), ('borne_supperieur', '>', target)])
            commission_excursion = total_sell * baremes[0].pourcentage_commission
            commision = commission_excursion + commission_chameau + commission_quatrefois + commission_rent
            obj = {
                'etat_id': id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'paxe': total_pax,
                'sale_amount': total_sell,
                'paxe_sale': pax_won,
                'target': target,
                'target_rate': baremes.pourcentage_commission,
                'commission': commision
            }
            self.env['target.detail'].create(obj)


class WizardReturnReports(models.TransientModel):
    _name = 'wizard.target_report_thalasso'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def calculate_commission_thalasso(self):
        # control saisie
        if self.date_to < self.date_from:
            raise UserError('vérifier les dates')

        commission_thalasso_guide = 0
        chiffre_affaire_thalasso = 0
        commission_thalasso_to = 0

        rec_guide_target = self.env['etat.guide.target.commision'].search(
            [('id', '=', self._context.get('active_ids'))])
        guide = rec_guide_target.guide
        #
        etat_vente_thalasso = self.env['liquidation.thalasso'].search(
            [('representant', '=', guide.id),
             ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        for etat in etat_vente_thalasso:
            commission_thalasso_guide = commission_thalasso_guide + etat.commission / len(etat.representant)
            chiffre_affaire_thalasso = chiffre_affaire_thalasso + etat.tarif
            commission_thalasso_to = commission_thalasso_to + etat.commission_to

        # liste_reservation_autrecentre = self.env['liquidation.thalasso'].search(
        #     [('centre_thalasso.centre_base', '=', False), ('representant', '=', guide.id),
        #      ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        # liste_config_centrebase = self.env['liquidation.configthalasso'].search(
        #     [('centre_base', '=', True), ('date_debut_saison', '<=', self.date_from),
        #      ('date_fin_saison', '>=', self.date_to)])
        # liste_config_autrecentre = self.env['liquidation.configthalasso'].search(
        #     [('centre_base', '=', False), ('date_debut_saison', '>=', self.date_from),
        #      ('date_fin_saison', '<=', self.date_to)])
        #
        id = 0
        id = self._context.get('active_ids')[0]
        # if len(self.env['ctm.commission.thalasso'].search(
        #         [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to), ('etat_id', '=', id)])) > 0:
        #     raise UserError('Dates can not intercept an old records ')
        # else:
        #     chiffre_affaire_centrebase = 0
        #     pax_centrebase = 0
        #
        #     for ligne in liste_reservation_centrebase:
        #         chiffre_affaire_centrebase = chiffre_affaire_centrebase + ligne.tarif
        #         pax_centrebase = pax_centrebase + ligne.paxe
        #     if pax_centrebase != 0:
        #
        #         if chiffre_affaire_centrebase / pax_centrebase >= liste_config_centrebase.montant_moyen:
        #             commission_guide_centrebase = chiffre_affaire_centrebase * liste_config_centrebase.commission_representant_max / 100
        #         else:
        #             commission_guide_centrebase = chiffre_affaire_centrebase * liste_config_centrebase.commission_representant_min / 100
        #     else:
        #         commission_guide_centrebase = 0
        #
        #     chiffre_affaire_autrecentre = 0
        #     pax_autrecentre = 0
        #
        #     for ligne1 in liste_reservation_autrecentre:
        #         chiffre_affaire_autrecentre = chiffre_affaire_autrecentre + ligne1.tarif
        #         pax_autrecentre = pax_autrecentre + ligne1.paxe
        #
        #     if pax_autrecentre != 0:
        #
        #         if chiffre_affaire_autrecentre / pax_autrecentre >= liste_config_autrecentre.montant_moyen:
        #             commission_guide = chiffre_affaire_autrecentre * liste_config_autrecentre.commission_representant_max / 100
        #         else:
        #             commission_guide = chiffre_affaire_autrecentre * liste_config_autrecentre.commission_representant_min / 100
        #
        #     else:
        #         commission_guide = 0

        obj = {
            'etat_id': id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'sale_number': chiffre_affaire_thalasso,

            'commission_brut': commission_thalasso_guide,

            'commission_TO': commission_thalasso_to

        }
        self.env['ctm.commission.thalasso'].create(obj)


class WizardReturnReports(models.TransientModel):
    _name = 'wizard.target_report_lagune'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    lagune_bool = fields.Boolean('Lagune')
    bellamarina_bool = fields.Boolean('Bella Marina')
    levoilier_bool = fields.Boolean('Le voilier')
    lether_bool = fields.Boolean('Lether shop')
    photograph_bool = fields.Boolean('Photograph')

    def calculate_commission_lagune(self):

        if not self.lagune_bool and not self.bellamarina_bool and not self.levoilier_bool and not self.lether_bool and not self.photograph_bool:
            raise UserError('tu dois cocher au moins une case')

        # control saisie
        if self.date_to < self.date_from:
            raise UserError('vérifier les dates')

        rec_guide_target = self.env['etat.guide.target.commision'].search(
            [('id', '=', self._context.get('active_ids'))])
        id = self._context.get('active_ids')[0]

        if self.lagune_bool:

            if len(self.env['ctm.commission.lagune'].search(
                    [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to),
                     ('etat_id', '=', id)])) > 0:
                raise UserError('Dates can not intercept an old records ')
            else:
                chiffre_affaire = 0
                guide = rec_guide_target.guide
                liste_lagune = self.env['ctm.sale.lagune'].search(
                    [('representant', '=', guide.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])

                for ligne in liste_lagune:
                    chiffre_affaire = chiffre_affaire + ligne.prix
                commission = chiffre_affaire * 0.05

            obj = {
                'etat_id': id,
                'date_from': self.date_from,
                'date_to': self.date_to,
                'sale_number': chiffre_affaire,
                'commission': commission,

            }
            self.env['ctm.commission.lagune'].create(obj)

        if self.bellamarina_bool:

            if len(self.env['ctm.commission.bella_marina'].search(
                    [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to),
                     ('etat_id', '=', id)])) > 0:
                raise UserError('Dates can not intercept an old records ')
            else:
                chiffre_affaire1 = 0
                commission_rep = 0
                commission_to = 0
                guide = rec_guide_target.guide
                liste_bellamarina = self.env['ctm.sale.bella_marina'].search(
                    [('representant', '=', guide.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
                las_config_bellamarina = self.env['liquidation.configrestaurant'].search([
                    ('nom_restaurant', '=', 'Bella Marina'),
                    ('date_debut_saison', '<=', datetime.datetime.strftime(self.date_from, '%Y-%m-%d')),
                    ('date_fin_saison', '>=', datetime.datetime.strftime(self.date_to, '%Y-%m-%d'))
                ])
                for ligne in liste_bellamarina:
                    chiffre_affaire1 = chiffre_affaire1 + ligne.pax
                    commission_to = commission_to + (ligne.pax * las_config_bellamarina[0].commission_agence)
                    commission_rep = commission_rep + (ligne.pax * las_config_bellamarina[0].commission_representant)

                obj1 = {
                    'etat_id': id,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'sale_number': chiffre_affaire1,
                    'commission': commission_rep,
                    'commission_to': commission_to,

                }

                self.env['ctm.commission.bella_marina'].create(obj1)

        if self.levoilier_bool:

            if len(self.env['ctm.commission.levoilier'].search(
                    [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to),
                     ('etat_id', '=', id)])) > 0:
                raise UserError('Dates can not intercept an old records ')
            else:
                chiffre_affaire1 = 0
                commission_rep = 0
                commission_to = 0
                guide = rec_guide_target.guide
                liste_bellamarina = self.env['ctm.sale.levoilier'].search(
                    [('representant', '=', guide.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])

                for ligne in liste_bellamarina:
                    chiffre_affaire1 = chiffre_affaire1 + ligne.pax
                    commission_to = commission_to + ligne.commission_agence
                    commission_rep = commission_rep + ligne.commission_representant

                obj4 = {
                    'etat_id': id,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'sale_number': chiffre_affaire1,
                    'commission': commission_rep,
                    'commission_to': commission_to,

                }

                self.env['ctm.commission.levoilier'].create(obj4)

        if self.lether_bool:
            if len(self.env['ctm.commission.lether_shop'].search(
                    [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_from),
                     ('etat_id', '=', id)])) > 0:
                raise UserError('Commission leather  ')
            else:
                guide = rec_guide_target.guide
                liste_leathershop = self.env['ctm.sale.leather_shop'].search(
                    [('representant', '=', guide.id), ('date_passage', '>=', self.date_from),
                     ('date_passage', '<=', self.date_to)])
                chiffre_affaire2 = 0
                commission_rep1 = 0

                for ligne in liste_leathershop:
                    chiffre_affaire2 = chiffre_affaire2 + ligne.amount
                    commission_rep1 = commission_rep1 + (ligne.amount * ligne.taux_commission)
                commission_to1 = chiffre_affaire2 * 0.15

                obj2 = {
                    'etat_id': id,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'sale_number': chiffre_affaire2,
                    'commission': commission_rep1,
                    'commission_to': commission_to1,

                }
            self.env['ctm.commission.lether_shop'].create(obj2)

        if self.photograph_bool:
            if len(self.env['ctm.commission.photograph'].search(
                    [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_from),
                     ('etat_id', '=', id)])) > 0:
                raise UserError('Commission photographe pour guide hotel déjà calculée ')
            else:
                guide = rec_guide_target.guide
                liste_photograph = self.env['ctm.sale.photograph'].search(
                    [('representant', '=', guide.id), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to)])

                chiffre_affaire3 = 0
                commission_rep2 = 0
                commission_to1 = 0

                for ligne in liste_photograph:
                    chiffre_affaire3 = chiffre_affaire3 + ligne.montant
                    commission_rep2 = commission_rep2 + ligne.commission_representant
                    commission_to1 = commission_to1 + ligne.commission_to

                obj3 = {
                    'etat_id': id,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'sale_number': chiffre_affaire3,
                    'commission': commission_rep2,
                    'commission_to': commission_to1,

                }
                self.env['ctm.commission.photograph'].create(obj3)


class WizardReturnReports(models.TransientModel):
    _name = 'wizard.target_report_commissionchauffeur'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def calculate_commission_chauffeur(self):

        # control saisie
        if self.date_to < self.date_from:
            raise UserError('vérifier les dates')

        rec_chauffeur = self.env['commission.chauffeur'].search(
            [('id', '=', self._context.get('active_ids'))])
        id1 = self._context.get('active_ids')[0]
        chauffeur = rec_chauffeur.chauffeur
        # rec_excursion_plan = self.env['excursion.transport.plan'].search(
        #     [('chauffeur', '=', chauffeur.id)])
        # id = rec_excursion_plan[0].excursion_id

        etat_vente_excursion = self.env['excursion.extra'].search(
            [('dat', '>=', self.date_from), ('dat', '<=', self.date_to)])
        liste_config_chauffeur = self.env['excursion.configsahara'].search([])
        last_config_chauffeur = liste_config_chauffeur[-1]

        if len(self.env['commission.chauffeur'].search(
                [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to),
                 ('id', '=', id1)])) > 0:
            raise UserError('Commission chauffeur déjà calculée dans cette période')
        else:
            commission_chameau = 0
            chiffre_affaire_chameau = 0
            pax_sahara = 0
            liste_config_chameau = self.env['liquidation.configchameau'].search([])
            last_config_chameau = liste_config_chameau[-1]
            part_chauffeur = (last_config_chameau.prix_vente - (
                    last_config_chameau.commission_guide + last_config_chameau.prix_achat)) / 2
            etat_vente_camel = self.env['excursion.movementday'].search(
                [('date_m', '>=', self.date_from), ('date_m', '<=', self.date_to), ('chauffeur', '=', chauffeur.id)])

            for ligne in etat_vente_camel:
                if ligne.excursion_id in self.env['excursion.excursion'].search([('type_excursion_camel', '=', True)]):

                    for x in ligne.touriste_info:
                        pax_sahara = pax_sahara + x.nbr_adulte + x.nbr_enfant

                commission_chameau = part_chauffeur * pax_sahara
                chiffre_affaire_chameau = pax_sahara * last_config_chameau.prix_vente

            chiffre_affaire_tapis = 0
            commission_tapis = 0
            etat_vente_tapis = self.env['liquidation.tapis'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                 ('chauffeur_excursion', '=', chauffeur.id)])
            for ligne1 in etat_vente_tapis:
                commission_tapis = commission_tapis + ligne1.commission_chauffeur
                chiffre_affaire_tapis = chiffre_affaire_tapis + ligne1.chiffre_affaire

            # for ligne2 in etat_vente_excursion:
            #     pax_sahara = pax_sahara + ligne2.adulte + ligne2.enfant

            commission = 500 + commission_tapis + commission_chameau

            rec_chauffeur.update({

                'date_from': self.date_from,
                'date_to': self.date_to,

                'commisssion': commission,
            })
            obj = {

                'comm_chff_id': id1,
                'sale_camel': chiffre_affaire_chameau,
                'sale_tapis': chiffre_affaire_tapis,
                'pax_sahara': pax_sahara,
                'commission_camel': commission_chameau,
                'commission_tapis': commission_tapis,

            }
            self.env['commission.chauffeur.detail'].create(obj)


class WizardReturnReport(models.TransientModel):
    _name = 'wizard.target_report_commissionguide'
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)

    def calculate_commission_guide(self):

        # control saisie
        if self.date_to < self.date_from:
            raise UserError('vérifier les dates')

        rec_guide = self.env['commission.excursion.guide'].search(
            [('id', '=', self._context.get('active_ids'))])
        id1 = self._context.get('active_ids')[0]
        guide = rec_guide.guide_id

        if len(self.env['commission.excursion.guide'].search(
                [('date_from', '<=', self.date_from), ('date_to', '>=', self.date_to),
                 ('id', '=', id1)])) > 0:
            raise UserError('Commission guide déjà calculée dans cette période')
        else:

            etat_vente = self.env['excursion.movementday'].search(
                [('date_m', '>=', self.date_from), ('date_m', '<=', self.date_to), ('guide_principale', '=', guide.id)])
            liste_config_chameau = self.env['liquidation.configchameau'].search([])
            last_config_chameau = liste_config_chameau[-1]
            part_guide = (last_config_chameau.prix_vente - (
                    last_config_chameau.commission_guide + last_config_chameau.prix_achat)) / 2
            pax_sahara = 0
            commission_chameau = 0
            chiffre_affaire_chameau = 0

            for ligne in etat_vente:
                if ligne.excursion_id in self.env['excursion.excursion'].search([('type_excursion_camel', '=', True)]):
                    for x in ligne.touriste_info:
                        pax_sahara = pax_sahara + x.nbr_adulte + x.nbr_enfant

                commission_chameau = part_guide * pax_sahara
                chiffre_affaire_chameau = pax_sahara * last_config_chameau.prix_vente

            etat_vente_tapis = self.env['liquidation.tapis'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                 ('guide_excursion', '=', guide.id)])
            commission_tapis = 0
            chiffre_affaire_tapis = 0

            for ligne1 in etat_vente_tapis:
                commission_tapis = commission_tapis + ligne1.commission_guide
                chiffre_affaire_tapis = chiffre_affaire_tapis + ligne1.chiffre_affaire

            etat_vente_jazira = self.env['liquidation.aljazira'].search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('guide_excursion', '=', guide.id)])
            chiffre_affaire_jazira = 0
            commission_jazira = 0
            chiffre_affaire_vrac = 0
            chiffre_emballe = 0

            for ligne2 in etat_vente_jazira:
                chiffre_affaire_jazira = chiffre_affaire_jazira + ligne2.chiffre_affaire_total
                commission_jazira = commission_jazira + ligne2.commission_guide
                chiffre_affaire_vrac = chiffre_affaire_vrac + ligne2.chiffre_affaire_vrac
                chiffre_emballe = chiffre_emballe + ligne2.chiffre_affaire_condition

            pax_quatre = 0
            liste_config_quatrefois = self.env['liquidation.quatrefois'].search([])
            last_config_quatrefois = liste_config_quatrefois[-1]

            for ligne1 in etat_vente:
                if ligne1.excursion_id in self.env['excursion.excursion'].search([('type_excursion_q_f_q', '=', True)]):
                    for y in ligne1.touriste_info:
                        pax_quatre = pax_quatre + y.nbr_adulte + y.nbr_enfant

            nbre_quatre = pax_quatre // 6

            if (pax_quatre % 6) != 0:
                nbre_quatre = nbre_quatre + 1
            total_cout = nbre_quatre * (
                    last_config_quatrefois.prix_location + last_config_quatrefois.frais_chauffeur) + pax_quatre
            chiffre_affaire_quatre = pax_quatre * 60
            commission_quatre_calcule = 0.15 * (chiffre_affaire_quatre - total_cout)
            if (commission_quatre_calcule / pax_quatre) > last_config_quatrefois.commission_max:

                commission_par_paxe = last_config_quatrefois.commission_max

            else:

                commission_par_paxe = commission_quatre_calcule / pax_quatre

            commission_quatre = commission_par_paxe * pax_quatre

            commission = commission_chameau + commission_jazira + commission_tapis + commission_quatre
            rec_guide.update({

                'date_from': self.date_from,
                'date_to': self.date_to,
                'commission': commission,
            })
            obj = {

                'commggid': id1,
                'sale_camel': chiffre_affaire_chameau,
                'sale_tapis': chiffre_affaire_tapis,
                'sale_quad': chiffre_affaire_quatre,
                'cost_quad': last_config_quatrefois.prix_location,
                'double_guide_bonus': False,
                'oil_oil': chiffre_affaire_vrac,
                'sale_oil': chiffre_emballe,
                'commission_quatre': commission_quatre,
                'commission_aljazira': commission_jazira,
                'commission_camel': commission_chameau,
                'commission_tapis': commission_tapis,
                'commission_double_guide': 0,

            }
            self.env['commission.excursion.guide.detail'].create(obj)


class AffichageReport(models.TransientModel):
    _name = 'wizard.ventereport'
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    guide_id = fields.Many2many('excursion.guide', domain=[('etat', '=', 'representant')])
    liquidation = fields.Boolean('ventes liquidés')
    noliquidation = fields.Boolean('ventes non liquidés')
    ticket_from = fields.Integer('ticket from')
    ticket_to = fields.Integer('ticket to')
    date_liquidation_from = fields.Date('date liquidation from')
    date_liquidation_to = fields.Date('date liquidation to')
    debiteur = fields.Boolean('débiteur')
    nodebiteur = fields.Boolean('non débiteur')

    def get_report_vente(self):
        domain_liquide = [('dat', '>=', self.date_from), ('dat', '<=', self.date_to), ('liquidation', '=', True),
                          ('state', '=', 'cnf')]
        domain_noliquide = [('dat', '>=', self.date_from), ('dat', '<=', self.date_to), ('liquidation', '=', False),
                            ('state', '=', 'cnf')]

        rec_excursions_liquide = self.env['excursion.extra'].search(domain_liquide)
        rec_excursions_noliquide = self.env['excursion.extra'].search(domain_noliquide)

        if not self.liquidation and not self.noliquidation:
            raise UserError('tu dois choisir au moins une case liquidation')
        if not self.debiteur and not self.nodebiteur:
            raise UserError('tu dois choisir au moins une case débiteur')
        liste_liquide = []
        liste_noliquide = []
        liste_total_device_liquide = []
        liste_total_device_noliquide = []
        guides_list = []
        liste_total_device_avoir = []
        liste_liquide_avoir = []

        if len(self.guide_id) == 0:
            for x in self.env['excursion.guide'].search([('etat', '=', 'representant')]):
                guides_list.append(x.id)
        else:
            for x in self.guide_id:
                guides_list.append(x.id)
        if len(guides_list) / 2 != 0:
            guides_list.append(0)
        if self.liquidation:
            if self.debiteur and not self.nodebiteur:
                requette = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = True and debiteur = TRUE and state = 'cnf' "
            elif not self.debiteur and self.nodebiteur:
                requette = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = True and debiteur = FALSE and state = 'cnf'"
            else:
                requette = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = True  and state = 'cnf'"
            cond = []

            if self.date_to and self.date_from:
                cond.append("dat >= '{0}' and dat <= '{1}'".format(self.date_from, self.date_to))
            if self.ticket_from and self.ticket_to:
                cond.append(
                    "ticket_number >= '{0}' and ticket_number <= '{1}'".format(self.ticket_from, self.ticket_to))
            if self.date_liquidation_from:
                cond.append(
                    "dat_liquidation >= '{0}' and dat_liquidation <= '{1}'".format(str(self.date_liquidation_from),
                                                                                   str(self.date_liquidation_to)))
            if len(self.guide_id) > 0:
                cond.append("vendeur_id in {0}".format(tuple(guides_list)))
            for con in cond:
                requette = requette + " and " + con

            requette = requette + "  order by ticket_number  ;"

            self._cr.execute(requette)
            for x in self._cr.fetchall():
                obj = {
                    'adultes': x[0],
                    'enfants': x[1],
                    'bebe': x[2],
                    'ticket_number': x[3],
                    'selling_price': x[4],
                    'excursion_name': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])
                    [0].excursion_id.name,
                    'excursion_date': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[0].dat,
                    'seller_name': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].vendeur_id.name,
                    'dat_liquidation': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].dat_liquidation,
                    'currency_id': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].currency_id.name,
                }
                liste_liquide.append(obj)
            list_currency = []
            list_tick = []
            list_tick_lick = []
            list_tick_nolick = []
            liste_total_device_liquide = []
            liste_total_device_noliquide = []
            if len(liste_liquide) > 0:
                for x in liste_liquide:
                    list_tick_lick.append(x['ticket_number'])
                if len(list_tick_lick) == 1:
                    list_tick_lick.append(0)
                requette_list_currency = '''select name from res_currency where 
                    id in ( select distinct currency_id from excursion_reservations
                    where ticket_number in {0}
                    )
                    
                    '''.format(tuple(list_tick_lick))
                self._cr.execute(requette_list_currency)
                for flouss in self._cr.fetchall():
                    obj_flouss = {
                        'name': flouss[0]
                    }
                    list_currency.append(obj_flouss)
                list_currency = [{'name':'USD'},{'name':'TND'}]
                for devise in list_currency:
                    total_par_devise = 0
                    total_avoir = 0
                    for ligne in liste_liquide:
                        if devise['name'] == ligne['currency_id']:
                            total_par_devise = total_par_devise + ligne['selling_price']
                    if self.date_liquidation_from:
                        if self.nodebiteur:
                            for k in self.env['excursion.reservations'].search(
                                    [('avoir_date', '>=', self.date_liquidation_from),
                                     ('avoir_date', '<=', self.date_liquidation_to),
                                     ('vendeur_id', 'in', guides_list), ('debiteur', '=', False),
                                     ('currency_id.name', '=', devise['name'])]):
                                obj_liquide_avoir = {
                                    'adultes': k.adulte,
                                    'enfants': k.enfant,
                                    'bebe': k.inf,
                                    'ticket_number': k.ticket_number,
                                    'selling_price': k.avoir_amount,
                                    'excursion_name': k.excursion_id.name,
                                    'excursion_date': k.dat,
                                    'seller_name': k.vendeur_id.name,
                                    'dat_liquidation': k.dat_liquidation,
                                    'avoir_date': k.avoir_date,
                                    'currency_id': k.currency_id.name,
                                }
                                liste_liquide_avoir.append(obj_liquide_avoir)
                                total_par_devise = total_par_devise - k.avoir_amount
                                total_avoir = total_avoir + k.avoir_amount
                        if self.debiteur:
                            for k in self.env['excursion.reservations'].search(
                                    [('avoir_date', '>=', self.date_liquidation_from),
                                     ('avoir_date', '<=', self.date_liquidation_to),
                                     ('vendeur_id', 'in', guides_list), ('debiteur', '=', True), ('state', '=', 'cnf'),
                                     ('currency_id.name', '=', devise['name'])]):
                                obj_liquide_avoir = {
                                    'adultes': k.adulte,
                                    'enfants': k.enfant,
                                    'bebe': k.inf,
                                    'ticket_number': k.ticket_number,
                                    'selling_price': k.avoir_amount,
                                    'excursion_name': k.excursion_id.name,
                                    'excursion_date': k.dat,
                                    'seller_name': k.vendeur_id.name,
                                    'dat_liquidation': k.dat_liquidation,
                                    'avoir_date': k.avoir_date,
                                    'currency_id': k.currency_id.name,
                                }
                                liste_liquide_avoir.append(obj_liquide_avoir)
                                total_par_devise = total_par_devise - k.avoir_amount
                                total_avoir = total_avoir + k.avoir_amount
                    obj_avoir = {
                        'devise': devise['name'],
                        'total': total_avoir
                    }
                    if obj_avoir['total'] > 0:
                        liste_total_device_avoir.append(obj_avoir)

                    obj_devise = {
                        'devise': devise['name'],
                        'total': total_par_devise
                    }
                    liste_total_device_liquide.append(obj_devise)

        else:
            liste_liquide = []
        if self.noliquidation:
            if self.debiteur and not self.nodebiteur:
                requette2 = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = FALSE and debiteur = TRUE and state = 'cnf'"
            elif not self.debiteur and self.nodebiteur:
                requette2 = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = FALSE and debiteur = FALSE and state = 'cnf' "
            else:
                requette2 = " select adulte , enfant , inf , ticket_number ,selling_price   from excursion_reservations where liquidation = FALSE and state = 'cnf'"
            cond = []

            if self.date_to and self.date_from:
                cond.append("dat >= '{0}' and dat <= '{1}'".format(self.date_from, self.date_to))
            if self.ticket_from and self.ticket_to:
                cond.append(
                    "ticket_number >= '{0}' and ticket_number <= '{1}'".format(self.ticket_from, self.ticket_to))
            if self.date_liquidation_from:
                cond.append("dat_liquidation >= '{0}' and dat_liquidation <= '{1}'".format(self.date_liquidation_from,
                                                                                           self.date_liquidation_to))
            if len(self.guide_id) > 0:
                cond.append("vendeur_id in {0}".format(tuple(guides_list)))
            for con in cond:
                requette2 = requette2 + " and " + con

            requette2 = requette2 + " order by ticket_number  ;"

            self._cr.execute(requette2)
            for x in self._cr.fetchall():
                obj = {
                    'adultes': x[0],
                    'enfants': x[1],
                    'bebe': x[2],
                    'ticket_number': x[3],
                    'selling_price': x[4],
                    'excursion_name': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])
                    [0].excursion_id.name,
                    'excursion_date': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[0].dat,
                    'seller_name': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].vendeur_id.name,
                    'dat_liquidation': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].dat_liquidation,
                    'currency_id': self.env['excursion.reservations'].search([('ticket_number', '=', x[3])])[
                        0].currency_id.name,
                }
                liste_noliquide.append(obj)
            liste_total_device_noliquide = []
            list_tick_nolick = []
            if len(liste_noliquide) > 0:
                for x in liste_noliquide:
                    list_tick_nolick.append(x['ticket_number'])
                if len(list_tick_nolick) == 1:
                    list_tick_nolick.append(0)
                requette_list_currency = '''select name from res_currency where 
                    id in ( select distinct currency_id from excursion_reservations
                    where ticket_number in {0}
                    )
                    
                    '''.format(tuple(list_tick_nolick))
                self._cr.execute(requette_list_currency)
                list_currency = []
                for flouss in self._cr.fetchall():
                    obj_flouss = {
                        'name': flouss[0]
                    }
                    list_currency.append(obj_flouss)
                list_currency = [{'name':'USD'},{'name':'TND'}]
                for devise in list_currency:
                    total_par_devise = 0
                    for ligne in liste_noliquide:
                        if devise['name'] == ligne['currency_id']:
                            total_par_devise = total_par_devise + ligne['selling_price']
                    obj_devise = {
                        'devise': devise['name'],
                        'total': total_par_devise
                    }
                    liste_total_device_noliquide.append(obj_devise)

        else:
            liste_noliquide = []

        if len(liste_total_device_noliquide) == 0 and len(liste_total_device_liquide) == 0:
            raise UserError('Sorry !! , No excursions has been found , try with other filters or change search datas')
        else:
            return {

                'data': {'ventelisteliquide': liste_liquide,
                         'ventelistenoliquide': liste_noliquide,
                         'chiffreliquide': liste_total_device_liquide,
                         'chiffrenoliquide': liste_total_device_noliquide,
                         'chiffreavoir': liste_total_device_avoir,
                         'ventelisteavoir': liste_liquide_avoir
                         },
                'type': 'ir.actions.report',
                'report_name': 'ctm_liquidation.vente_excursion',
                'report_type': 'qweb-pdf',
                'name': 'Etat de vente ',
            }


class Duplication(models.TransientModel):
    _name = 'wizard.duplication'
    nbre_duplication = fields.Integer('nbre de duplications')

    @api.multi
    def dupliquer(self):
        id1 = self._context.get('active_ids')[0]
        etat_a_dupliquer = self.env['liquidation.thalasso'].search([('id', '=', id1)])
        i = 0
        for x in range(0, self.nbre_duplication):
            i = i + 1
            etat_a_dupliquer.copy({'numero_etat': str(i)})


class Calculeradulte(models.TransientModel):
    _name = 'wizard.calculadulte'
    date_from = fields.Date('date from', required=True)
    date_to = fields.Date('date to', required=True)
    excursion = fields.Many2one('excursion.excursion', string="Excursion name", required=True)
    representant = fields.Many2one('excursion.guide', string="Seller name", required=True)

    def calculer_adulte(self):
        liste_vente = self.env['excursion.reservations'].search(
            [('vendeur_id', '=', self.representant.id), ('excursion_id', '=', self.excursion.id),
             ('dat', '>=', self.date_from),
             ('dat', '<=', self.date_to)])
        pax_total = 0
        pax_adulte = 0
        for liste in liste_vente:
            pax_total = pax_total + liste.adulte + liste.enfant + liste.inf
            pax_adulte = pax_adulte + liste.adulte
        if pax_total == 0:
            raise UserError('aucun enregistrement existe pour ces critères')
        obj = {
            'date_debut': self.date_from,
            'date_fin': self.date_to,
            'excursion': self.excursion.id,
            'representant': self.representant.id,
            'pourcentage': pax_adulte / pax_total * 100
        }
        self.env['liquidation.pourcentageadulte'].create(obj)


class Reportthalasso(models.TransientModel):
    _name = 'wizard.ventethalasso'

    date_from = fields.Date('date vente from', required=True)
    date_to = fields.Date('date vente to', required=True)
    date_from_encaissement = fields.Date("date d'encaissement from")
    date_to_encaissement = fields.Date("date d'encaissement to")
    date_payment = fields.Date("date payement")
    rep = fields.Many2one('excursion.guide', string="représentants")
    centre_base = fields.Many2one('liquidation.centrethalasso', string="centre de base")
    centre_autre = fields.Many2one('liquidation.centrethalasso', string="autre centre")
    commission_calcule = fields.Boolean('commission calculé')
    commission_noncalcule = fields.Boolean('commission non calculé')

    def get_report_vente_thalasso(self):

        list_vent_date = self.env['liquidation.thalasso'].search([
            ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        if self.date_from_encaissement:
            domain_encaissement = [('date_recu', '>=', self.date_from_encaissement),
                                   ('date_recu', '<=', self.date_to_encaissement)]
        else:
            domain_encaissement = []
        list_vent_encaissement = self.env['liquidation.thalasso'].search(domain_encaissement)

        if self.date_payment:
            domain_payment = [('date_paiement', '=', self.date_payment)]
        else:
            domain_payment = []
        list_vent_payment = self.env['liquidation.thalasso'].search(domain_payment)

        guides_list = []
        if not self.rep:
            for x in self.env['excursion.guide'].search([('etat', '=', 'representant')]):
                guides_list.append(x.id)
            domain_rep = [('representant', 'in', guides_list)]
        else:
            domain_rep = [('representant', '=', self.rep.id)]
        centres_list = []

        # liste des centres
        lsc = []
        if self.centre_base or self.centre_autre:
            for x in self.centre_base:
                lsc.append(x.id)
            for x in self.centre_autre:
                lsc.append(x.id)
            domain_centre = [('centre_thalasso', 'in', lsc)]
        else:
            for x in self.env['liquidation.centrethalasso'].search([]):
                centres_list.append(x.id)
            domain_centre = [('centre_thalasso', 'in', centres_list)]
        list_vent_rep = self.env['liquidation.thalasso'].search(domain_rep)
        list_vent_centre = self.env['liquidation.thalasso'].search(domain_centre)
        # list_vent = [value for value in list_vent_rep if value in list_vent_centre]
        list_vent = self.env['liquidation.thalasso'].search([], order="date")
        # if len(list_vent) == 0:
        #     raise UserError('aucune résultat trouvée')
        list_vente_commission = []
        list_total_commission = []
        if self.commission_calcule:

            total_chiffre = 0
            total_commission = 0

            for x in list_vent:
                if (x in list_vent_centre) and (x in list_vent_date) and (x in list_vent_encaissement) and (
                        x in list_vent_payment) and (x in list_vent_rep) and (x.commission != 0):
                    l1 = []
                    total_chiffre = total_chiffre + x.tarif
                    total_commission = total_commission + x.commission
                    for y in x.representant:
                        obj_name = {
                            'name': y.name
                        }
                        l1.append(obj_name)
                    obj = {
                        'date': x.date,
                        'representant': l1,
                        'nom_hotel': x.nom_hotel.name,
                        'centre_thalasso': x.centre_thalasso.nom_centre,
                        'tarif': x.tarif,
                        'numero_etat': x.numero_etat,
                        'commission': x.commission,
                        'date_encaissement': x.date_recu,
                        'date_payment': x.date_paiement
                    }
                    list_vente_commission.append(obj)

            obj_total = {
                'total': total_chiffre,
                'commission': total_commission

            }
            list_total_commission.append(obj_total)
        list_vente_nocommission = []
        list_total_nocommission = []
        if self.commission_noncalcule:
            total_chiffre1 = 0
            for x in list_vent:
                if (x in list_vent_centre) and (x in list_vent_date) and (x in list_vent_rep) and (x.commission == 0):
                    l2 = []
                    total_chiffre1 = total_chiffre1 + x.tarif
                    for y in x.representant:
                        obj_name1 = {
                            'name': y.name
                        }
                        l2.append(obj_name1)
                        obj2 = {
                            'date': x.date,
                            'representant': l2,
                            'nom_hotel': x.nom_hotel.name,
                            'centre_thalasso': x.centre_thalasso.nom_centre,
                            'tarif': x.tarif,
                            'numero_etat': x.numero_etat,
                            'commission': x.commission
                        }
                    list_vente_nocommission.append(obj2)

            obj_total1 = {
                'total': total_chiffre1

            }
            list_total_nocommission.append(obj_total1)

        if len(list_vente_commission) == 0 and len(list_vente_nocommission) == 0:
            raise UserError('aucune résultat trouvée')

        return {

            'data': {'ventelistecommission': list_vente_commission,
                     'totalcommission': list_total_commission,
                     'ventelistenocommission': list_vente_nocommission,
                     'totalnocommission': list_total_nocommission,
                     },
            'type': 'ir.actions.report',
            'report_name': 'ctm_liquidation.vente_thalasso',
            'report_type': 'qweb-pdf',
            'name': 'Etat de vente',
        }


class ReportHistouriqueRep(models.TransientModel):
    _name = 'wizard.historiquerep'

    date_from = fields.Date('date from', required=True)
    date_to = fields.Date('date to', required=True)
    rep = fields.Many2one('excursion.guide', string="représentants", required=True)

    def get_report_historique_rep(self):
        list_affectation = self.env['liquidation.historiquerep'].search(
            [('date_debut', '>=', self.date_from), ('date_fin', '<=', self.date_to),
             ('representant', '=', self.rep.id)], order="date_debut")
        liste_affectation = []
        for x in list_affectation:

            list_hotel = []
            for y in x.hotel_id:
                obj_hotel = {
                    'name': y.name
                }
                list_hotel.append(obj_hotel)

                obj = {
                    'date_debut': x.date_debut,
                    'date_fin': x.date_fin,
                    'hotel': list_hotel,
                    'pax_adulte': x.pax_adulte,
                    'pax_enfant': x.pax_enfant,
                    'pax': x.pax,
                }
            liste_affectation.append(obj)
        rep = {
            'name': self.rep.name
        }
        return {

            'data': {'ventete': liste_affectation,
                     'representant': rep
                     },
            'type': 'ir.actions.report',
            'report_name': 'ctm_liquidation.historique_report',
            'report_type': 'qweb-pdf',
            'name': 'Etat de vente',
        }


class ReportAnalyseVentePasDateArrive(models.TransientModel):
    _name = 'wizard.anveda'

    by_checkin = fields.Boolean('By arrival date')
    by_liquid = fields.Boolean('By liquidation date')
    checkin_from = fields.Date('Checkin from')
    checkin_to = fields.Date('Checkin to')
    lquid_from = fields.Date('Liquidation from')
    lquid_to = fields.Date('Liquidation to')
    seller = fields.Many2many('excursion.guide', domain=[('etat', '=', 'representant')])
    excursion = fields.Many2many('excursion.excursion')
    show_tickets = fields.Boolean('show tickets ? ')
    show_avoir = fields.Boolean('show avoir details')

    @api.multi
    def print(self):

        # initialisation

        tts = 0
        ttsl = 0
        tpx = 0
        tpxl = 0
        reps = ''
        fil = ''
        bl = []
        booking_str = 'a'
        resl = []
        cresl = []
        guides = []
        list_booking_final = []
        avoir_detail1 = []
        somme_avoir_liq1 = 0
        somme_avoir1 = 0
        excursions = []

        for s in self.seller:
            guides.append(s.id)
        for ex in self.excursion:
            excursions.append((ex.id))
        if self.by_checkin:
            fil = fil + ' Par date arrivé '
        if self.by_liquid:
            fil = fil + ' Par date de liquidation'
        for x in self.seller:
            reps = reps + x.name + " "
        date_list = []
        # filtre de recherche
        domain_search = []
        # ajout vendeur
        if self.seller:
            domain_search.append(('vendeur_id', 'in', guides))

        # ajout date de liquidation

        if self.by_liquid:
            if self.lquid_from:
                domain_search.append(("dat_liquidation", ">=", self.lquid_from))
            if self.lquid_to:
                domain_search.append(("dat_liquidation", "<=", self.lquid_to))
        # ajout excursion
        if self.excursion:
            domain_search.append(('excursion_id', 'in', excursions))
            # if len(self.excursion) == 1:
            #     domain_search.append(('excursion_id', '=', self.excursion.id))
            # else:
            #     domain_search.append(('excursion_id', 'in', self.excursion.id))
        # remplir tableau par date chekin avec ou sans date liquidation

        if self.by_checkin:

            # recupérer les dates de chekin

            base = self.checkin_from
            nbr = (self.checkin_to - self.checkin_from).days + 1
            date_list = [base + datetime.timedelta(days=kk) for kk in range(0, nbr)]

            for x in self.env['excursion.reservations'].search(domain_search):
                if not x.booking_number:
                    continue
                else:
                    booking_str = booking_str + x.booking_number
            booking_str = booking_str.split(",")

            del booking_str[0]

            # get bookings records

            for b in booking_str:
                if not self.env['ctm.reservation.list'].search([('reservation_number', '=', b.split()[0])]):
                    continue
                resl.append(self.env['ctm.reservation.list'].search([('reservation_number', '=', b.split()[0])])[0])
                id = self.env['ctm.reservation.list'].search([('reservation_number', '=', b.split()[0])])[0].id
                if id > 0:
                    bl.append(id)

            # sort bookings in dates

            for dt in date_list:
                bookings = []
                for res in resl:
                    if res.chekin == dt:
                        bookings.append(res)
                obj1 = {
                    'dat': dt,
                    'bookings': bookings,
                    'sale': 0,
                    'salel': 0,
                    'pax': 0,
                    'paxl': 0,
                    'tickets': []
                }
                cresl.append(obj1)
            # raise UserError(str(cresl))

            for y in cresl:
                sum = 0
                suml = 0
                pax = 0
                paxl = 0
                tickets = []
                for exc in self.env['excursion.reservations'].search(domain_search):
                    if exc.booking_number:
                        for z in y['bookings']:
                            if z.reservation_number in exc.booking_number:
                                if exc.ticket_number not in tickets:
                                    tickets.append(exc.ticket_number)
                                    if exc.liquidation is True:
                                        if exc.avoir_bool is True:
                                            if exc.avoir_amount == exc.selling_price:
                                                continue
                                            else:
                                                suml = suml + exc.selling_price - exc.avoir_amount
                                                _logger.error(exc.selling_price)
                                                tts = tts + exc.selling_price - exc.avoir_amount
                                                ttsl = ttsl + exc.selling_price - exc.avoir_amount
                                                tpx = tpx + exc.adulte + exc.enfant + exc.inf
                                                tpxl = tpxl + exc.adulte + exc.enfant + exc.inf
                                                paxl = paxl + exc.adulte + exc.enfant + exc.inf
                                                sum = sum + exc.selling_price - exc.avoir_amount
                                                pax = pax + exc.adulte + exc.enfant + exc.inf
                                        suml = suml + exc.selling_price
                                        _logger.error(exc.selling_price)
                                        tts = tts + exc.selling_price
                                        ttsl = ttsl + exc.selling_price
                                        tpx = tpx + exc.adulte + exc.enfant + exc.inf
                                        tpxl = tpxl + exc.adulte + exc.enfant + exc.inf
                                        paxl = paxl + exc.adulte + exc.enfant + exc.inf
                                        sum = sum + exc.selling_price
                                        pax = pax + exc.adulte + exc.enfant + exc.inf
                                    else:
                                        tpx = tpx + exc.adulte + exc.enfant + exc.inf
                                        tts = tts + exc.selling_price
                                        sum = sum + exc.selling_price
                                        pax = pax + exc.adulte + exc.enfant + exc.inf
                y['sale'] = y['sale'] + sum
                y['pax'] = y['pax'] + pax
                y['salel'] = y['salel'] + suml
                y['paxl'] = y['paxl'] + paxl
                y['tickets'] = tickets
            print('hi')
            domain_search_avoir = domain_search
            domain_search_avoir.append(('avoir_bool', '=', True))

            for reservation in self.env['excursion.reservations'].search(domain_search_avoir):
                for record in cresl:
                    for z in record['bookings']:
                        if reservation.booking_number:
                            if z.reservation_number in reservation.booking_number:
                                obj_avoir1 = {
                                    'date_chekin': record['dat'],
                                    'montant_liquide': reservation.selling_price,
                                    'montant_avoir': reservation.avoir_amount,
                                    'ticket': reservation.ticket_number,

                                }
                                if obj_avoir1 not in avoir_detail1:
                                    avoir_detail1.append(obj_avoir1)
                        else:
                            obj_avoir1 = {
                                'date_chekin': 'indéfini',
                                'montant_liquide': reservation.selling_price,
                                'montant_avoir': reservation.avoir_amount,
                                'ticket': reservation.ticket_number,

                            }
                            if obj_avoir1 not in avoir_detail1:
                                avoir_detail1.append(obj_avoir1)
            # raise UserError(str(avoir_detail1))

        # remplir table par date liquidation seulement
        somme_vendu = 0
        somme_pax = 0
        avoir_detail = []
        somme_avoir = 0
        somme_avoir_liq = 0
        if self.by_liquid and not self.by_checkin:
            list_liquid = self.env['excursion.reservations'].search(domain_search)
            final_sum = 0
            final_avoir = 0
            for kkk in list_liquid:
                final_sum = final_sum + kkk.selling_price - kkk.avoir_amount
                final_avoir = final_avoir + kkk.avoir_amount
            list_booking = []
            for ligne in list_liquid:
                if not ligne.booking_number:
                    somme_vendu = somme_vendu + ligne.selling_price - ligne.avoir_amount
                    somme_avoir = somme_avoir + ligne.avoir_amount
                else:

                    detail = 'a' + str(ligne.booking_number)
                    detail = detail.split(",")
                    del detail[0]
                    if ligne.avoir_bool is True and (ligne.selling_price == ligne.avoir_amount):

                        obj_avoir = {
                            'date_chekin': '',
                            'montant_liquide': ligne.selling_price,
                            'montant_avoir': ligne.avoir_amount,
                            'ticket': ligne.ticket_number,
                            'booking_number': detail
                        }
                        avoir_detail.append(obj_avoir)
                    elif ligne.avoir_bool is True and (ligne.selling_price != ligne.avoir_amount):
                        etat = {
                            'date_chekin': '',
                            'montant': ligne.selling_price - ligne.avoir_amount,
                            'pax': ligne.adulte + ligne.enfant + ligne.inf,
                            'ticket': ligne.ticket_number,
                            'date_liquidation': ligne.dat_liquidation,
                            'booking_number': detail
                        }
                        obj_avoir = {
                            'date_chekin': '',
                            'montant_liquide': ligne.selling_price,
                            'montant_avoir': ligne.avoir_amount,
                            'ticket': ligne.ticket_number,
                            'booking_number': detail
                        }
                        avoir_detail.append(obj_avoir)

                    else:
                        etat = {
                            'date_chekin': '',
                            'montant': ligne.selling_price,
                            'pax': ligne.adulte + ligne.enfant + ligne.inf,
                            'ticket': ligne.ticket_number,
                            'date_liquidation': ligne.dat_liquidation,
                            'booking_number': detail
                        }
                    list_booking.append(etat)
            for xx in list_booking:
                valeur = self.env['ctm.reservation.list'].search(
                    [('reservation_number', '=', xx['booking_number'][0].split()[0])])
                if not valeur:
                    continue
                else:
                    xx['date_chekin'] = valeur[0].chekin

            tab = []
            for val in list_booking:
                if not (val['date_chekin'] in tab):
                    if val['date_chekin'] == '':
                        continue
                    else:

                        tab.append(val['date_chekin'])

            tab.sort()

            for zz in tab:
                ticketss = []
                montant = 0
                pax = 0
                for zzz in list_booking:
                    if zz == zzz['date_chekin']:
                        montant = montant + zzz['montant']
                        pax = pax + zzz['pax']
                        ticketss.append(zzz['ticket'])
                etat1 = {
                    'date_chekin': zz,
                    'montant': montant,
                    'pax': pax,
                    'ticket': ticketss,
                }
                list_booking_final.append(etat1)
            for zzaa in list_booking_final:
                somme_vendu = somme_vendu + zzaa['montant']
                somme_pax = somme_pax + zzaa['pax']
            for mm in avoir_detail:
                if mm['booking_number']:
                    vals = self.env['ctm.reservation.list'].search(
                        [('reservation_number', '=', mm['booking_number'][0].split()[0])])
                    mm['date_chekin'] = vals[0].chekin
                else:
                    mm['date_chekin'] = 'indéfini'

        if len(avoir_detail) > 0:
            for avv in avoir_detail:
                somme_avoir_liq = somme_avoir_liq + avv['montant_liquide']
                somme_avoir = somme_avoir + avv['montant_avoir']
        if len(avoir_detail1) > 0:
            for avv1 in avoir_detail1:
                somme_avoir_liq1 = somme_avoir_liq1 + avv1['montant_liquide']
                somme_avoir1 = somme_avoir1 + avv1['montant_avoir']
        return {
            'data': {'tts': tts, 'ttsl': ttsl, 'tpx': tpx, 'tpxl': tpxl, 'show_tickets': self.show_tickets,
                     'arrr': self.by_checkin, 'arrf': self.checkin_from, 'arrt': self.checkin_to, 'rep': reps,
                     'fil': fil, 'dt': date_list, 'bo': cresl, 'bol': list_booking_final,
                     'somme_liq': final_sum,
                     'pax_liq': somme_pax, 'alll': self.by_liquid, 'allf': self.lquid_from,
                     'allt': self.lquid_to,
                     'avoir': avoir_detail, 'avoir1': avoir_detail1, 'avoir_bool': self.show_avoir,
                     'somme_avoir_liq1': somme_avoir_liq1, 'somme_avoir1': somme_avoir1,
                     'somme_avoir_liq': final_avoir, 'somme_avoir': final_avoir},
            'type': 'ir.actions.report',
            'report_name': 'ctm_liquidation.avenda_report',
            'report_type': 'qweb-pdf',
            'name': 'Analyse des vente represenant',
        }
