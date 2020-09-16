from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class WizardReturnReports(models.Model):
    _name = 'wizards.print.prestataires'
    years = fields.Selection(selection=[('2018', 2018), ('2019', 2019), ('2020', 2020), ('2021', 2021),
                                        ('2022', 2022), ('2023', 2023), ('2024', 2024), ('2025', 2025),
                                        ('2026', 2026), ('2027', 2027), ('2028', 2028),
                                        ('2029', 2029), ('2030', 2030), ('2031', 2031), ('2032', 2032),
                                        ('2033', 2033), ('2034', 2034), ('2035', 2035), ('2036', 2036),
                                        ('2037', 2037), ('2038', 2038), ('2039', 2039), ('2040', 2040)],
                             string="Année")
    report_type = fields.Selection(
        selection=[('ep', 'Etat Des Prestataire '), ('lt', 'Liste des Tarifs')],
        string="Type d'etat")

    def get_report(self):
        finallist = []
        if self.report_type == 'ep':
            dtmax = datetime(int(self.years), 12, 31)
            dtmin = datetime(int(self.years), 1, 1)
            domain = [('date', '>=', dtmin), ('date', '<=', dtmax.date())]
            list_prestataire = self.env['excursion.etat.prestataire'].search(domain)
            for y in list_prestataire:
                pourcentage = y.pourcentage
                observation = y.observation
                delais_paiment = y.delais_paiment
                excursion = y.excursion_id.name
                prestation = y.prestation_id.name
                prix_adult = y.detail_prix.prix_adult

                gratuite = y.detail_prix.gratuite
                prix_enfant = y.detail_prix.prix_enfant

                prestation_obj = {
                    'pourcentage': pourcentage,
                    'observation': observation,
                    'delais_paiment': delais_paiment,
                    'excursion': excursion,
                    'prestation': prestation,
                    'prix_adult': prix_adult,
                    'gratuite': gratuite,
                    'prix_enfant': prix_enfant
                }
                finallist.append(prestation_obj)
            return {

                'data': {'years': self.years, 'eplist': finallist},
                'type': 'ir.actions.report',
                'report_name': 'excursion.ep_report',
                'report_type': 'qweb-pdf',

                'name': 'Etat des prestataire',
            }

        elif self.report_type == 'lt':

            list_pointll = self.env['excursion.depart'].search([])
            tarifs = self.env['excursion.tarif'].search([])
            nbr = len(list_pointll)
            noms_point = []
            list_tarif = []
            for tar in tarifs:
                itinerary = tar.itinerary.text
                duration = tar.duration
                l_point = []
                points_dep = []
                points_dep = self.env['excursion.pointdepart'].search([('tarif_id', '=', tar.id)])

                for i in points_dep:
                    emplacement = i.emplacement.name
                    prix_a = i.adult
                    prix_e = i.children

                    point_obj = {
                        'children': prix_e,
                        'adult': prix_a,
                        'emplacement': emplacement,
                    }
                    l_point.append(point_obj)
                tarif_obj = {
                    'itinerary': itinerary,
                    'duration': duration,
                    'liste_point': l_point,
                }
                list_tarif.append(tarif_obj)

            for t in list_pointll:
                noms_point.append(t.name)
            # raise UserError(str(nbr)+'\n'+str(noms_point)+'\n'+str(list_tarif))
            return {

                'data': {'nbr': nbr, 'noms': noms_point, 'tarifs': list_tarif},
                'type': 'ir.actions.report',
                'report_name': 'excursion.lt_report',
                'report_type': 'qweb-pdf',

                'name': 'Liste des tarifs',
            }


class LiquidationTickets(models.TransientModel):
    _name = 'wizards.liquidationtickets'

    ticket_from = fields.Integer('Ticket From', required=True)
    ticket_to = fields.Integer('Ticket To', required=True)
    date_liquidation = fields.Date('date liquidation', required=True)
    list_excursion = fields.Many2many('excursion.reservations', string='liste des etats de ventes')

    @api.onchange('ticket_to')
    def auto_remplir(self):
        self.list_excursion = self.env['excursion.reservations'].search(
            [('ticket_number', '>=', self.ticket_from), ('ticket_number', '<=', self.ticket_to),
             ('liquidation', '=', False), ('state','=','cnf')])

    def liquider(self):
        guide_id = None
        recs = self.env['excursion.reservations'].sudo().search(
            [('ticket_number', '>=', self.ticket_from), ('ticket_number', '<=', self.ticket_to)])
        list_liquide = self.env['excursion.reservations'].sudo().search(
            [('ticket_number', '>=', self.ticket_from), ('ticket_number', '<=', self.ticket_to),
             ('liquidation', '=', True)])
        list_ticket = []
        for y in list_liquide:
            ticket = "ticket n°" + str(y.ticket_number)
            list_ticket.append(ticket)
        if len(list_liquide) > 0:
            raise UserError('list liquidé' + str(list_ticket))
        if len(recs) > 0:
            for x in recs:
                guide_id = x.vendeur_id
                x.sudo().update({
                    'liquidation': True,
                    'dat_liquidation': self.date_liquidation
                })

            # make the sequence first
            seq = self.env.ref('ctm_liquidation.liquidation_report_sequence').sudo().next_by_id()
            seq = seq
            # get liquidation date
            liquidation_date = self.date_liquidation
            # get current user + creation date
            user = self.env.user.id
            dat = datetime.today().date()
            # search for avoirs
            avoir_list = []
            for x in self.env['excursion.reservations'].sudo().search([('vendeur_id', '=', guide_id.id)]):
                if x.avoir_bool and x.avoir_date == self.date_liquidation:
                    aobj = {
                        'avoir_date': x.avoir_date,
                        'avoir_amount': x.selling_price,
                        'ticket_id': x.id,
                        'currency_id': x.currency_id.id,
                        'liquidation_report_id': 0
                    }
                    avoir_list.append(aobj)
            rep_obj = {
                'sequence_number': seq,
                'liquidation_date': liquidation_date,
                'creation_user': user,
                'creation_dat': dat,
                'guide_id': guide_id.id
            }
            liquidation_report = self.env['liquidation.report'].sudo().create(rep_obj)
            # traittement des tickets
            for x in recs:
                x.sudo().update({
                    'liquidation_report_id': liquidation_report.id,

                })
            # traittement des avoirs
            if len(avoir_list) > 0:
                for avoir in avoir_list:
                    if len(self.env['excursion.avoir'].sudo().search([('ticket_id', '=', avoir['ticket_id'])])) == 0:
                        avoir['liquidation_report_id'] = liquidation_report.id
                        self.env['excursion.avoir'].sudo().create(avoir)
                    else:
                        if self.env['excursion.avoir'].sudo().search(
                                [('ticket_id', '=', avoir['ticket_id'])]).liquidation_report_id == False:
                            self.env['excursion.avoir'].sudo().search(
                                [('ticket_id', '=', avoir['ticket_id'])]).liquidation_report_id = liquidation_report.id
            # total computation  :
            devises = []
            for x in recs:
                if x.currency_id not in devises:
                    devises.append(x.currency_id)
            for x in devises:
                s = 0
                dobj = {
                    'currency_id': x.id,
                    'amount': 0,
                    'liquidation_report_id': liquidation_report.id
                }
                for y in recs:
                    if x.id == y.currency_id.id:
                        s = s + y.selling_price
                dobj['amount'] = s
                if len(liquidation_report.avoir_detail) > 0:
                    for a in liquidation_report.avoir_detail:
                        if a.currency_id.id == x.id:
                            s = s - a.avoir_amount
                    dobj['amount'] = s
                self.env['liquidation.devise.totals'].sudo().create(dobj)

class Ajoutcamel(models.TransientModel):
    _name = 'wizards.ajoutcamel'

    @api.model
    def auto_remplir(self):
        li = []
        rec_movement = self.env['excursion.movementday'].search([('id', '=', self._context.get('active_ids'))])
        rec = self.env['excursion.reservations'].search(
            [('dat', '=', rec_movement.date_m), ('excursion_id.type_excursion_camel', '=', True),
             ('movementday_id', '=', False)])
        for x in rec:
            li.append(x.id)
        return [('id', 'in', li)]

    ajouter_ligne = fields.Many2many('excursion.reservations', string='liste des ventes camel', required=True,
                                     domain=auto_remplir)

    @api.multi
    def ajout_camel(self):
        for ii in self.ajouter_ligne:
            ii.update({
                'movementday_id': self._context.get('active_ids')[0],
            })
