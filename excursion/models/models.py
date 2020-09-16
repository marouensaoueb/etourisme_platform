# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from operator import itemgetter

from odoo import models, fields, api


class Excursion(models.Model):
    _name = 'excursion.excursion'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    config_sahara = fields.Many2one('liquidation.configsahara')
    code = fields.Char('code Excursion')
    name = fields.Char("nom de l'excursion")
    nbr_jours = fields.Integer('Nbr jours', rrquired=True)
    p_a_t_n = fields.Float('prix adulte ')
    p_e_t_n = fields.Float('prix enfant')
    p_a_t_p = fields.Float('prix adulte')
    p_e_t_p = fields.Float('prix enfant ')
    commission = fields.Selection(string="Commission ", selection=[('taux', 'Taux'), ('montant', 'Montant')])
    chauf = fields.Selection(string="Chauff.oblig  ", selection=[('oui', 'Oui'), ('non', 'Non')])
    guide = fields.Selection(string="Guide.oblig ", selection=[('oui', 'Oui'), ('non', 'Non')])
    act = fields.Selection(string="Active ", selection=[('oui', 'Oui'), ('non', 'Non')])
    observation = fields.Char('Observation')
    jours = fields.Many2many('excursion.jour', string="Journées Depart")
    h_depart = fields.Float('Heure Départ')
    h_retour = fields.Float('Heure Retour')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    h_depart_hotel = fields.Float('Heure Départ')

    # region_id = fields.Many2one('excursion.emplacement', string="Region")
    # date = fields.Date(string="Date Excursion")
    #
    # prix_adult = fields.Float(string="prix Adult", digits=(10, 3))
    # prix_enfant = fields.Float(string="prix Enfant", digits=(10, 3))
    # prix_bebe = fields.Float(string="prix Bebe", digits=(10, 3))
    # vehicule = fields.Many2one('fleet.vehicle', String="Vehicule")
    # prestataire = fields.Many2one('excursion.prestation', string="Prestataire")
    type_excursion_q_f_q = fields.Boolean('4*4 ')
    type_excursion_camel = fields.Boolean('camel')
    type_excursion_sahara = fields.Boolean('sahara')
    liste_region_tarif = fields.One2many('excursion.tarif.region', 'excursion_id')
    liste_hotel_depart = fields.One2many('excursion.hotel.depart', 'excursion_id')
    liste_jours_pro = fields.One2many('excursion.jour.programme', 'excursion_id')
    currency_id = fields.Many2one('res.currency')
    prixbase = fields.Monetary('prix de base')
    prixextra = fields.Monetary('prix extra')
    ito_curency = fields.Many2one('res.currency', string='ito Curency')
    bebemaxage = fields.Integer('age bebe max')
    enfmaxage = fields.Integer('age enfant max')
    ppp = fields.Boolean('Prix par groupe')

    @api.onchange('nbr_jours')
    def nombre_jours_programme(self):
        excursion_id = self._context.get('active_ids')
        l = []
        for i in range(0, self.nbr_jours):
            jour = i + 1
            # self.env['excursion.jour.programme'].create({'jour_num': jour, 'excursion_id': excursion_id})
            obj = {
                'jour_num': jour,
                'excursion_id': excursion_id
            }
            l.append(obj)
        self.liste_jours_pro = l

    @api.multi
    def return_the_action(self):
        exc_id = self.id
        return {

            'type': 'ir.actions.act_window',

            'name': 'Historique des prix excursions',

            'view_mode': 'tree',

            'res_model': 'exc.prices.history',

            'target': "current",

            'domain': [('excursion_id', '=', exc_id)]

        }


class JourProgramme(models.Model):
    _name = "excursion.jour.programme"
    jour_num = fields.Integer('Jour numero')
    liste_pro = fields.One2many('excursion.programme', 'jp_id', string="Programmes de jour")
    excursion_id = fields.Many2one('excursion.excursion')


class Programme(models.Model):
    _name = 'excursion.programme'
    fournisseur = fields.Many2one('excursion.vendeur')
    prestation = fields.Many2one('excursion.prestation', string="Prestation")
    bv = fields.Boolean('B.V')
    jp_id = fields.Many2one('excursion.jour.programme')


class HotelDepart(models.Model):
    _name = "excursion.hotel.depart"
    _rec_name = 'code'
    _description = " configuration hotel depart pour l'excursion "
    code = fields.Char('Code')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    depart = fields.Float('Depart')
    excursion_id = fields.Many2one('excursion.excursion')


class WeekDays(models.Model):
    _name = 'excursion.jour'
    name = fields.Char("Jours")


class HeriteState(models.Model):
    _inherit = "res.country.state"
    region = fields.Many2one('excursion.emplacement')


class RegionTarif(models.Model):
    _name = 'excursion.tarif.region'
    _rec_name = 'code'
    _description = ' les configuration des region prix '

    code = fields.Char('Code')
    region = fields.Many2one('excursion.pointdepart', string="Region")
    p_adulte_n = fields.Float('prix Adulte Normal', digits=(10, 3))
    p_bebe_n = fields.Float('prix enfant Normal', digits=(10, 3))
    p_bb_n = fields.Float('prix bebe Normal', digits=(10, 3))
    p_adulte_p = fields.Float('prix Adulte Package', digits=(10, 3))
    p_bebe_p = fields.Float('prix enfant Package', digits=(10, 3))
    p_bb_p = fields.Float('prix bebe Package', digits=(10, 3))
    currency_id = fields.Many2one('res.currency', string="currency")
    excursion_id = fields.Many2one('excursion.excursion')
    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')

    @api.multi
    def write(self, vals):
        exc_id = self.env['excursion.excursion'].search([('name', '=', self.excursion_id.name)]).id
        obj = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'region': self.region.id,
            'p_adulte_n': self.p_adulte_n,
            'p_bebe_n': self.p_bebe_n,
            'p_bb_n': self.p_bb_n,
            'p_adulte_p': self.p_adulte_p,
            'p_bebe_p': self.p_bebe_p,
            'p_bb_p': self.p_bb_p,
            'currency_id': self.currency_id.id,
            'excursion_id': exc_id,
        }
        if len(self.env['exc.prices.history'].search(
                [('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to),
                 ('excursion_id', '=', exc_id), ('region', '=', self.region.id)])) == 0:
            rec = self.env['exc.prices.history'].create(obj)
        rec = super(RegionTarif, self).write(vals)

        return rec


class Configsahara(models.Model):
    _name = 'excursion.configsahara'
    _description = 'les configurations des commissions chauffeurs sahara'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    commission_chauffeur = fields.Float('commission chauffeur')
    # liste_excursion_sahara = fields.One2many('excursion.excursion', 'config_sahara', string='liste excursions sahara')


class MovementDay(models.Model):
    _name = 'excursion.movementday'
    _rec_name = "date_m"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def get_domain(self):
        recs = self.env['excursion.excursion'].search([('type_excursion_camel', '=', False)])
        l = []
        for x in recs:
            l.append(x.id)
        return [('excursion_id.id', 'in', l)]

    def get_domain1(self):
        recs = self.env['excursion.excursion'].search([('type_excursion_camel', '=', True)])
        l = []
        for x in recs:
            l.append(x.id)
        return [('excursion_id.id', 'in', l)]

    date_m = fields.Date("Journée")
    excursion_id = fields.Many2one('excursion.excursion', string="Excursion")
    guide_principale = fields.Many2one('excursion.guide', string='Guide Principale',
                                       domain=[('etat', '=', 'principale')])
    numero_guide_principale = fields.Char('Tel Guide Principale')
    guide_doubleur = fields.Many2one('excursion.guide', string='Guide Doubleur', domain=[('etat', '=', 'principale')])
    numero_guide_doubleur = fields.Char('Tel Guide Doubleur')
    chauffeur = fields.Many2one('ctm.conductor', string='Chauffeur')
    vehicule = fields.Many2one('fleet.vehicle', String="Vehicule")
    num_order = fields.Char('Num Order de mission')
    nbr_adulte = fields.Integer('Nbre Adulte')
    nbr_enfant = fields.Integer('Nbre Enfant')
    nbr_bebe = fields.Integer('Nbre Bébé')
    pax = fields.Float('nombre total de paxes')
    touriste_info = fields.One2many('excursion.reservations', 'movementday_id', domain=get_domain,
                                    string='Touriste Info')
    Camel_info = fields.One2many('excursion.reservations', 'movementday_id', domain=get_domain1, string='Extra Camel')
    nbr_q_q = fields.Integer('nbr 4*4')
    representatives_info = fields.One2many('move.repres.info', 'mov_id', string="Representatives Info")

    @api.onchange('guide_principale')
    def auto_remplir_guide_principale(self):
        self.numero_guide_principale = self.guide_principale.tel

    @api.onchange('guide_doubleur')
    def auto_remplir_guide_doubleur(self):
        self.numero_guide_doubleur = self.guide_doubleur.tel

    @api.model
    def create(self, vals):
        vals['num_order'] = self.env.ref('excursion.sequence_ordre_mission').next_by_id()
        return super(MovementDay, self).create(vals)

    # @api.depends('touriste_info')
    # def totalpaxes(self):
    #     for k in self.touriste_info:
    #         self.nbr_bebe = self.nbr_bebe + k.inf
    #         self.nbr_adulte = self.nbr_adulte + k.adulte
    #         self.nbr_enfant =  self.nbr_enfant + k.enfant
    #     total_pax = self.nbr_bebe + self.nbr_adulte + self.nbr_enfant
    @api.multi
    def config_order_hotel(self):
        return {

            'type': 'ir.actions.act_window',

            'name': 'Configuration de depart hotels',

            'view_mode': 'tree',

            'res_model': 'hotel.depart.config',

            'target': "new",

            'domain': [('movementday_id', '=', self.id)]

        }

    def print_order(self):
        guide_doub = False
        num_guide_doub = False
        if self.guide_doubleur != False:
            guide_doub = self.guide_doubleur.name
            num_guide_doub = self.numero_guide_doubleur
        s = self.excursion_id.h_depart
        i, d = divmod(s, 1)
        minutes = d * 60 / 100
        minutes = round(minutes, 3)
        split_num = str(minutes).split('.')
        decimal_part = int(split_num[1])
        if decimal_part < 10:
            decimal_part = decimal_part * 10
        split_num2 = str(s).split('.')
        int_part = int(split_num2[0])
        temps = str(int_part) + ':' + str(decimal_part)
        date_depart = "le " + str(self.date_m.strftime('%d-%m-%Y')) + " à " + str(temps)
        s = self.excursion_id.h_retour
        i, d = divmod(s, 1)
        minutes = d * 60 / 100
        minutes = round(minutes, 3)
        split_num = str(minutes).split('.')
        decimal_part = int(split_num[1])
        if decimal_part < 10:
            decimal_part = decimal_part * 10
        split_num2 = str(s).split('.')
        int_part = int(split_num2[0])
        temps = str(int_part) + ':' + str(decimal_part)
        nbr_jours = self.excursion_id.nbr_jours
        retor = self.date_m + timedelta(days=nbr_jours)
        retor = retor.strftime('%d-%m-%Y')
        date_retour = "le " + str(retor) + " à " + str(temps)
        liste_res = []
        reel_total_adulte = 0
        reel_total_enfant = 0
        for x in self.touriste_info:
            rec_kk = self.env['hotel.depart.config'].search(
                [('movementday_id', '=', self.id), ('hotel', "=", x.hotel_id.id)])
            s1 = rec_kk[0].heure
            i1, d1 = divmod(s1, 1)
            minutes1 = d1 * 60 / 100
            minutes1 = round(minutes1, 3)
            split_num1 = str(minutes1).split('.')
            decimal_part1 = int(split_num1[1])
            if decimal_part1 < 10:
                decimal_part1 = decimal_part1 * 10
            split_num21 = str(s1).split('.')
            int_part1 = int(split_num21[0])
            temps1 = str(int_part1) + ':' + str(decimal_part1)
            reel_total_adulte = reel_total_adulte + x.radulte
            reel_total_enfant = reel_total_enfant + x.renfant
            oo = {
                'depart': temps1,
                'ticket': x.ticket_number + " " + x.vendeur_id.name,
                'hotel': x.hotel_id.name,
                'client': x.tour_operateur.name,
                'room': x.room_nbr,
                'adulte': x.adulte,
                'enfant': x.enfant,
                'reel_adulte': x.radulte,
                'reel_enfant': x.renfant,
            }
            liste_res.append(oo)
        lll = sorted(liste_res, key=itemgetter('depart'))
        km_sortie = self.vehicule.odometer

        obj = {
            'excursion': self.excursion_id.name,
            'vehicule': self.vehicule.name,
            'chauffeur': self.chauffeur.name,
            'num_chauf': self.chauffeur.num_tel,
            'guide': self.guide_principale.name,
            'num_guide': self.numero_guide_principale,
            'num_ordre': self.num_order,
            'guide_doub': guide_doub,
            'num_guide_doub': num_guide_doub,
            'depart': date_depart,
            'retour': date_retour,
            'liste_res': lll,
            'km_sortie': km_sortie,
            'total_enfant': self.nbr_enfant,
            'total_adulte': self.nbr_adulte,
            'rtadulte': reel_total_adulte,
            'rtenfant': reel_total_enfant,
        }
        # raise UserError(str(num_guide_doub))
        return {

            'data': {'orde': obj},
            'type': 'ir.actions.report',
            'report_name': 'excursion.ep_report',
            'report_type': 'qweb-pdf',

            'name': 'Order de mission',
        }


# class InfoClient(models.Model):
#     _name = 'excursion.client'
#     _description = 'cette classe pour connaitre le client avec son nombre de ticket et sa hotel'
#     _rec_name = 'ticket_nbr'
#     ticket_nbr = fields.Char('Nombre de ticket')
#     room_nbr = fields.Char('Room number')
#     hotel_id = fields.Many2one('rooming.hotels', string=" Hotel")
#     nbr_adulte = fields.Integer('Nbre Adulte')
#     nbr_enfant = fields.Integer('Nbre Enfant')
#     nbr_bebe = fields.Integer('Nbre Bébé')
#     movementday_id = fields.Many2one('excursion.movementday', string='movement Day')


#
# class GeneraleData(models.Model):
#     _name = 'excursion.generale.data'
#     _rec_name = 'excursion_id'
#     excursion_id = fields.Many2one('excursion.excursion', string="Excursion")
#     guide_principale = fields.Many2one('excursion.guide', string='Guide Principale')
#     numero_guide_principale = fields.Char('Tel Guide Principale')
#     guide_doubleur = fields.Many2one('excursion.guide', string='Guide Doubleur')
#     numero_guide_doubleur = fields.Char('Tel Guide Doubleur')
#     nbr_adulte = fields.Integer('Nbre Adulte')
#     nbr_enfant = fields.Integer('Nbre Enfant')
#     nbr_bebe = fields.Integer('Nbre Bébé')
#     movementday_id = fields.Many2one('excursion.movementday', string='movement Day')
#
#
# class TransportPlan(models.Model):
#     _name = 'excursion.transport.plan'
#     _rec_name = 'excursion_id'
#     excursion_id = fields.Many2one('excursion.excursion', string="Excursion")
#     chauffeur = fields.Many2one('ctm.conductor', string='Chauffeur')
#     vehicule = fields.Many2one('fleet.vehicle', String="Vehicule")
#     first_hotel = fields.Many2one('rooming.hotels', string="Premier Hotel")
#     last_hotel = fields.Many2one('rooming.hotels', string="Dernier Hotel")
#     num_order = fields.Char('Num Order de mission')
#     movementday_id = fields.Many2one('excursion.movementday', string='movement Day')


class MovRepInfo(models.Model):
    _name = "move.repres.info"

    representative_id = fields.Many2one('excursion.guide', string="representant")
    nbr_pax = fields.Integer('clients number')
    mov_id = fields.Many2one('excursion.movementday')


class ExcursionPlan(models.Model):
    _name = 'excursion.excursionplan'
    _rec_name = 'excursion'
    excursion = fields.Many2one('excursion.excursion', string='Excursion')
    packsnbr = fields.Integer('packs Number')
    first_hotel = fields.Many2one('rooming.hotels', string="First Hotel")
    last_hotel = fields.Many2one('rooming.hotels', string="Last Hotel")
    guide = fields.Many2one('excursion.guide', string='Guide')
    numero_guide = fields.Char('numero Tel Guide')
    chauffeur = fields.Many2one('ctm.conductor', string='Chauffeur')
    numero_chauffeur = fields.Char('numero Chauffeur')
    movementday_id = fields.Many2one('excursion.movementday', string='movement Day')


class Circuit(models.Model):
    _name = 'excursion.circuit'
    _rec_name = 'text'
    text = fields.Char('Circuit à afficher ')
    emplacements = fields.One2many('excursion.emplacement', 'circuit_id', 'Emplacement')

    @api.model
    def create(self, vals):
        names = []

        for obj in vals['emplacements']:
            names.append(obj[2]['name'])
        res = ""
        for i in names:
            res += i + " + "
        res = res[:-2]
        vals['text'] = res
        rec = super(Circuit, self).create(vals)
        return rec


class Emplacement(models.Model):
    _name = 'excursion.emplacement'
    name = fields.Char(string='nom Region')
    circuit_id = fields.Many2one('excursion.circuit', string="Tarif")


class Prestation(models.Model):
    _name = 'excursion.prestation'
    name = fields.Char("prestation")

    fornisseur_id = fields.Many2one('excursion.vendeur')


class DetailPrix(models.Model):
    _rec_name = 'designation'
    _name = 'excursion.detail.prix'
    prix_adult = fields.Float('Adult', digits=(10, 1))

    gratuite = fields.Selection(string='Gratuite',
                                selection=[('1/25', '1/25'), ('non', 'Non'), ('1/15 4*4', '1/15 4*4'),
                                           ('Moins 12 ans gratuite', 'Moins 12 ans gratuite')])
    prix_enfant = fields.Float('Enfant', digits=(10, 0))
    designation = fields.Char(readonly=True, default="prix detaillé", string="prix detaillé")


class EtatPrestataire(models.Model):
    _name = 'excursion.etat.prestataire'
    date = fields.Date("date d'excursion ")
    pourcentage = fields.Integer("%")
    observation = fields.Selection(string="Observation",
                                   selection=[('Ok', 'Ok'), ('En Cours', 'En Cours'),
                                              ('Annuler le service', 'Annuler le service')])
    delais_paiment = fields.Selection(string="Delais de Paiment",
                                      selection=[('15 jrs aprés reception Facture', '15jrs aprés reception Facture'),
                                                 ('30 jrs aprés reception Facture', '30 jrs aprés reception Facture'),
                                                 ('07 jrs aprés reception Facture', '07 jrs aprés reception Facture')])
    excursion_id = fields.Many2one('excursion.excursion', string="Excursion")
    # prestation_id = fields.Many2one('excursion.prestation', string="Prestation")
    detail_prix = fields.Many2one('excursion.detail.prix', string="")


class PointDepart(models.Model):
    _name = 'excursion.pointdepart'
    name = fields.Char('nom')
    region = fields.Many2one('excursion.emplacement', string="region")
    tarif_id = fields.Many2one('excursion.tarif', string="Tarif")


class Depart(models.Model):
    _name = 'excursion.depart'
    _rec_name = 'name'
    name = fields.Char("From")
    date_creation = fields.Datetime(string='date et temps de creation ', default=str(datetime.today()))


class Tarif(models.Model):
    _name = 'excursion.tarif'
    _rec_name = 'itinerary'
    itinerary = fields.Many2one('excursion.circuit', string='Itinerary')
    points_departs = fields.One2many('excursion.pointdepart', 'tarif_id', 'point de depart')
    duration = fields.Selection(string="Duration",
                                selection=[('1 day', '1 day'), ('1/2 day', '1/2 day'), ('2 H', '2 H')])


class Agence(models.Model):
    _name = 'excursion.agence'
    _rec_name = 'code'
    name = fields.Char("nom de l'agence")
    code = fields.Char("Code Agence")


class Vendeur(models.Model):
    _name = 'excursion.vendeur'
    _rec_name = 'nom'
    nom = fields.Char("nom de Fournisseur")
    num_tel = fields.Char("tel Fournisseur")
    liste_prestation = fields.One2many('excursion.prestation', 'fornisseur_id', string="liste des prestation")


class Guide(models.Model):
    _name = 'excursion.guide'
    _rec_name = 'name'
    name = fields.Char("nom de Guide")
    etat = fields.Selection(string="Etat",
                            selection=[('principale', 'Guide Excursion principal'),
                                       ('doubleur', 'Guide Excursion doubleur'),
                                       ('representant', ' Guide hotel')])


class HoraireDej(models.Model):
    _name = 'excursion.horairedej'
    _rec_name = 'text'
    text = fields.Char('Circuit à afficher ')
    sortie = fields.Float('Heure de Sortie')
    rentrer = fields.Float('Heure de rentré ')

    @api.model
    def create(self, vals):
        res = "de " + str(vals['sortie']) + " à " + str(vals['rentrer'])
        vals['text'] = res
        rec = super(HoraireDej, self).create(vals)
        return rec


class Extra(models.Model):
    _name = 'excursion.extra'

    dat = fields.Date("Excursion date")
    crdat = fields.Date("Creation  date")
    excursion_id = fields.Many2one('excursion.excursion', string="Excursion name")
    adulte = fields.Integer('Adulte')
    enfant = fields.Integer('Chd')
    inf = fields.Integer('Inf')
    radulte = fields.Integer('reel Adulte')
    renfant = fields.Integer('reel Chd')
    rinf = fields.Integer('reel Inf')
    tour_operateur = fields.Many2one('tour.operator', string='Tour operator')
    booking_number = fields.Char(string='Booking number')
    ticket_number = fields.Integer('Ticket number ')
    vendeur_id = fields.Many2one('excursion.guide', string='Seller name')
    selling_price = fields.Monetary('Selling price')
    seller_commission = fields.Float('Seller commission', digits=(10, 3))
    paid_sum = fields.Monetary('Paid sum')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    room_nbr = fields.Char('Room Nr.')
    liquidation = fields.Boolean('Liquidation')
    dat_liquidation = fields.Date('Date liquidation')
    currency_id = fields.Many2one('res.currency')
    doc_nbr = fields.Char('Document Nr.')
    movementday_id = fields.Many2one('excursion.movementday', string='movement Day')
    ext25 = fields.Boolean('Extra 25% on price ')
    ext25amount = fields.Float('EXT25%amount')
    tu_key = fields.Char('tourist quey')
    region_id = fields.Many2one('excursion.emplacement', string="Region")
    city_key = fields.Many2one('excursion.pointdepart', string="Ville")
    res_id = fields.Many2one('excursion.reservations', string="reservation linked")
    state = fields.Selection(selection=[('cnf', 'Confirmed'), ('cncl', 'Canceled')])

    @api.model
    def create(self, vals):
        excursion_id = vals['excursion_id']
        try:
            region = vals['city_key']
            rec_prix = self.env['excursion.tarif.region'].search(
                [('excursion_id', '=', excursion_id), ('region.id', '=', region), ('date_from', '<=', vals['dat']),
                 ('date_to', '>=', vals['dat'])])
            excursion_rec = self.env['excursion.excursion'].search([('id','=',excursion_id)]).ppp
            if excursion_rec:
                rec_prix = self.env['excursion.tarif.region'].search(
                    [('excursion_id', '=', excursion_id),  ('date_from', '<=', vals['dat']),
                     ('date_to', '>=', vals['dat'])])
                sell_prix = rec_prix[0].p_adulte_p
            else:
                if len(rec_prix) == 0:
                    rec_prix = self.env['exc.prices.history'].search(
                        [('excursion_id', '=', excursion_id), ('region.id', '=', region), ('date_from', '<=', vals['dat']),
                         ('date_to', '>=', vals['dat'])])
                    sell_prix = rec_prix[0].p_adulte_n * vals['adulte'] + rec_prix[0].p_bebe_n * vals['enfant'] + rec_prix[
                        0].p_bb_n * vals['inf']
                else:
                    sell_prix = rec_prix[0].p_adulte_n * vals['adulte'] + rec_prix[0].p_bebe_n * vals['enfant'] + rec_prix[
                        0].p_bb_n * vals['inf']
            vals['selling_price'] = sell_prix
            vals['paid_sum'] = sell_prix
        except:
            pass
        rec = super(Extra, self).create(vals)
        return rec

    @api.onchange('ext25')
    def extra_price(self):
        if self.ext25 is True:
            self.update({
                'paid_sum': self.paid_sum * 0.75,
                'selling_price': self.selling_price * 0.75,
                'ext25amount': self.selling_price * 0.25
            })
        else:
            self.update({
                'paid_sum': self.paid_sum + self.ext25amount,
                'selling_price': self.selling_price + self.ext25amount,
                'ext25amount': 0
            })

    @api.onchange('liquidation')
    def set_liquid_date(self):
        if self.liquidation is True:
            self.update({
                'dat_liquidation': datetime.today().date()
            })


class ExcursionSeason(models.Model):
    _name = "excursion.season"
    _rec_name = "name"
    _description = "this classe is for the season of the excursion module"
    name = fields.Char('Season')
    date_de = fields.Date("du")
    date_a = fields.Date("au")
    liste_prix_prestation = fields.One2many('excursion.season.prestation', 'excursion_season_id',
                                            string="liste des prix de prestation")
    contract_id = fields.Many2one('excursion.contract')


class PrestationSeason(models.Model):
    _name = "excursion.season.prestation"
    _description = "this class is for the configure of the prestation and the price for every season in excursion"
    centre = fields.Many2one('excursion.agence', string="centre")
    excursion_id = fields.Many2one('excursion.excursion', string="excursion")
    prestation = fields.Many2one('excursion.prestation', string="prestation")
    tarif_adulte = fields.Float('Tarif adulte', digits=(10, 3))
    tarif_enfnat = fields.Float('Tarif enfant', digits=(10, 3))
    pax_de = fields.Integer('pax de')
    pax_a = fields.Integer('pax à')
    excursion_season_id = fields.Many2one('excursion.season')


class Rule(models.Model):
    _name = "excursion.rule"
    name = fields.Char('name')
    contingent = fields.Selection(string="Type de Rule", selection=[('valeur', 'Valeur '),
                                                                    ('taux', 'Taux')])
    valeur = fields.Float('valeur', digits=(10, 3))
    seasons = fields.Many2many('excursion.season', string="Seasons")
    age = fields.Boolean('depend to age ?')


class ContractFournissuer(models.Model):
    _name = "excursion.contract"
    _rec_name = "fournisseur"
    _description = " this classe is for the fournisser contract"

    fournisseur = fields.Many2one('excursion.vendeur', string="Fournissuer")
    annee = fields.Integer('Année')
    date_debut = fields.Date('Date de debut')
    date_fin = fields.Date('Date de fin')
    monnaie = fields.Many2one('res.currency')
    t_j = fields.Boolean('Taux/Journée')
    ttc = fields.Boolean('Contract TTC')
    contingent = fields.Selection(string="Contingent", selection=[('pas_contingent', 'Pas de Contingent '),
                                                                  ('par_cat', 'Par Categorie'),
                                                                  ('global', 'Global')])
    signer = fields.Char('Signé par :')
    date_signer = fields.Date('Signé le ')
    observation = fields.Char('Observation')
    liste_seasons = fields.One2many('excursion.season', 'contract_id', string='seasons')


class ConfigHotel(models.Model):
    _name = "hotel.depart.config"

    hotel = fields.Many2one('rooming.hotels', string='hotel')
    heure = fields.Float('Heure depart')
    movementday_id = fields.Many2one('excursion.movementday', string='movement Day')


class ExcursionReservations(models.Model):
    _name = 'excursion.reservations'
    _rec_name = 'ticket_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "ticket_number"

    dat = fields.Date("Excursion date")
    crdat = fields.Date("Creation  date")
    excursion_id = fields.Many2one('excursion.excursion', string="Excursion name")
    adulte = fields.Integer('Adulte')
    enfant = fields.Integer('Chd')
    inf = fields.Integer('Inf')
    radulte = fields.Integer('reel Adulte')
    renfant = fields.Integer('reel Chd')
    rinf = fields.Integer('reel Inf')
    tour_operateur = fields.Many2one('tour.operator', string='Tour operator')
    booking_number = fields.Char(string='Booking number')
    ticket_number = fields.Integer('Ticket number ')
    vendeur_id = fields.Many2one('excursion.guide', string='Seller name')
    selling_price = fields.Monetary('Selling price')
    seller_commission = fields.Float('Seller commission', digits=(10, 3))
    paid_sum = fields.Monetary('Paid sum')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    room_nbr = fields.Char('Room Nr.')
    liquidation = fields.Boolean('Liquidation', track_visibility='onchange')
    dat_liquidation = fields.Date('Date liquidation', track_visibility='onchange')
    currency_id = fields.Many2one('res.currency')
    doc_nbr = fields.Char('Document Nr.')
    movementday_id = fields.Many2one('excursion.movementday', string='movement Day')
    ext25 = fields.Boolean('Extra 25% on price ')
    ext25amount = fields.Float('EXT25%amount')
    tu_key = fields.Char('tourist quey')
    region_id = fields.Many2one('excursion.emplacement', string="Region")
    city_key = fields.Many2one('excursion.pointdepart', string="Ville")
    excursion_detail = fields.One2many('excursion.extra', 'res_id', string='detail of excursion')
    is_manuel = fields.Boolean('is manuel')
    avoir_bool = fields.Boolean('a un Avoir', track_visibility='onchange')
    avoir_amount = fields.Monetary('Avoir amount', track_visibility='onchange')
    avoir_date = fields.Date('Date avoir')
    debiteur = fields.Boolean('débiteur')
    state = fields.Selection(selection=[('cnf', 'Confirmed'), ('cncl', 'Canceled')])

    @api.onchange('avoir_bool')
    def change_avoir_amount(self):
        if not self.avoir_bool:
            self.avoir_amount = 0
        else:
            self.avoir_amount = self.selling_price

    @api.onchange('selling_price')
    def retrun_is_manuelle(self):
        self.is_manuel = True

    @api.onchange('ext25')
    def extra_price(self):
        if self.ext25 is True:
            self.update({
                'paid_sum': self.paid_sum * 0.75,
                'selling_price': self.selling_price * 0.75,
                'ext25amount': self.selling_price * 0.25
            })
        else:
            self.update({
                'paid_sum': self.paid_sum + self.ext25amount,
                'selling_price': self.selling_price + self.ext25amount,
                'ext25amount': 0
            })

    @api.onchange('liquidation')
    def set_liquid_date(self):
        if self.liquidation is True:
            self.update({
                'dat_liquidation': datetime.today().date()
            })


class PricesExcHistory(models.Model):
    _name = "exc.prices.history"
    _rec_name = "date_from"

    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')
    region = fields.Many2one('excursion.pointdepart', string="Region")
    p_adulte_n = fields.Float('prix Adulte Normal', digits=(10, 3))
    p_bebe_n = fields.Float('prix enfant Normal', digits=(10, 3))
    p_bb_n = fields.Float('prix bebe Normal', digits=(10, 3))
    p_adulte_p = fields.Float('prix Adulte Package', digits=(10, 3))
    p_bebe_p = fields.Float('prix enfant Package', digits=(10, 3))
    p_bb_p = fields.Float('prix bebe Package', digits=(10, 3))
    currency_id = fields.Many2one('res.currency', string="currency")
    excursion_id = fields.Many2one('excursion.excursion')
