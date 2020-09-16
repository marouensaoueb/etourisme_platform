# -*- coding: utf-8 -*-


from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


# class ctm_liquidation(models.Model):
#     _name = 'ctm_liquidation.ctm_liquidation'
#
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
class RepresentantGuide(models.Model):
    _inherit = 'excursion.guide'
    code = fields.Char('Code Guide')
    tel = fields.Char('numéro de téléphone')
    partner_id = fields.Many2one('res.partner', string="partner lié")

    hotel_id = fields.Many2many('rooming.hotels', string="hotel lié")
    details_id = fields.One2many('guide.hotels.detail', 'guide_id', string="Details des reservations")

    @api.onchange('partner_id')
    def auto_remplir(self):
        self.tel = self.partner_id.mobile
        self.name = self.partner_id.name

    @api.multi
    def get_reservations(self):
        id = self._context.get('active_ids') or self.id
        return {'type': 'ir.actions.act_window',

                'name': 'Historique affectation',

                'res_model': 'liquidation.historiquerep',

                'view_type': 'form',
                'domain': [('representant', '=', id)],

                'view_mode': 'tree,form',

                }


class lfkdngkjdfbgkjd(models.Model):
    _name = "guide.hotels.detail"
    date = fields.Date('Date')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    pax = fields.Float('PAX', digits=(10, 2))
    enfants = fields.Integer('Nbre enfants')
    adults = fields.Integer('Nbre adults')
    bebes = fields.Integer('Nbre bébés')
    guide_id = fields.Many2one('excursion.guide', string="Guide")


class kjfekjdbgkjd(models.Model):
    _name = 'ctm.commission.thalasso'
    _rec_name = 'date_from'
    _description = 'etat commission thalasso par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("Chiffre d'affaire")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission_TO = fields.Monetary('Commission thalasso')
    retenue = fields.Monetary('Retenue')
    commission_brut = fields.Monetary('commission brut')
    commission_net = fields.Monetary('commission net')


class Bellamarina(models.Model):
    _name = 'ctm.sale.bella_marina'

    prestation = fields.Char('prestation')
    date = fields.Date('date')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    pax = fields.Integer('nombre de pax')
    room_number = fields.Char('Num chambre')
    representant = fields.Many2one('excursion.guide', string='representant hotel',
                                   domain=[('etat', '=', 'representant')])
    currency_id = fields.Many2one('res.currency')
    commission_representant = fields.Float()
    commission_agence = fields.Float()

    @api.model
    def create(self, vals):
        rec = self.env['liquidation.configrestaurant'].search(
            [('date_debut_saison', '<=', vals['date']), ('date_fin_saison', '>=', vals['date']),
             ('nom_restaurant', '=', 'Bella Marina')])

        vals['commission_agence'] = rec[-1].commission_agence * vals['pax']
        vals['commission_representant'] = rec[-1].commission_representant * vals['pax']

        rec = super(Bellamarina, self).create(vals)
        return rec


class Levoilier(models.Model):
    _name = 'ctm.sale.levoilier'

    prestation = fields.Char('prestation')
    date = fields.Date('date')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    pax = fields.Integer('nombre de pax')
    room_number = fields.Char('Num chambre')
    representant = fields.Many2one('excursion.guide', string='representant hotel',
                                   domain=[('etat', '=', 'representant')])
    currency_id = fields.Many2one('res.currency')
    commission_representant = fields.Float()
    commission_agence = fields.Float()

    @api.model
    def create(self, vals):
        rec = self.env['liquidation.configrestaurant'].search(
            [('date_debut_saison', '<=', vals['date']), ('date_fin_saison', '>=', vals['date']),
             ('nom_restaurant', '=', 'Le voilier')])

        vals['commission_agence'] = rec[-1].commission_agence * vals['pax']
        vals['commission_representant'] = rec[-1].commission_representant * vals['pax']

        rec = super(Levoilier, self).create(vals)
        return rec


class Saleleathershop(models.Model):
    _name = 'ctm.sale.leather_shop'

    date_passage = fields.Date('Date passage')
    representant = fields.Many2one('excursion.guide', string='representant hotel',
                                   domain=[('etat', '=', 'representant')])
    agence = fields.Char('Agence')
    produit = fields.Char('Produit')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    montant = fields.Float('Montant', digits=(10, 2))
    typ = fields.Selection(selection=[('d', 'Directement avec lether shop '), ('ind', 'A traver le representant')])
    commission_agence = fields.Float('commission agence')
    commission_representant = fields.Float('commission représentant')
    currency_id = fields.Many2one('res.currency')


class Configleathershop(models.Model):
    _name = 'ctm.sale.configleathershop'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    typ = fields.Selection(selection=[('d', 'Directement avec lether shop '), ('ind', 'A traver le representant')])
    commission_representant = fields.Float('commission représentant', digits=(10, 3))
    commission_agence = fields.Float('commission agence', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class Salephoto(models.Model):
    _name = 'ctm.sale.photograph'

    date = fields.Date('Date')
    representant = fields.Many2one('excursion.guide', string='representant hotel',
                                   domain=[('etat', '=', 'representant')])
    montant = fields.Float('prix de vente', digits=(10, 3))
    commission_to = fields.Float('Commission agence', digits=(10, 3))
    commission_representant = fields.Float('Commission representant', digits=(10, 3))
    nbre_photo = fields.Integer('nombres de session photo')
    currency_id = fields.Many2one('res.currency')

    @api.model
    def create(self, vals):
        rec = self.env['liquidation.configphoto'].search(
            [('date_debut_saison', '<=', vals['date']), ('date_fin_saison', '>=', vals['date'])])

        vals['commission_to'] = rec[-1].commission_to * vals['nbre_photo']
        vals['commission_representant'] = rec[-1].commission_rep * vals['nbre_photo']
        vals['montant'] = rec[-1].prix_photo * vals['nbre_photo']

        rec = super(Salephoto, self).create(vals)
        return rec


class fhgfjgkjhk(models.Model):
    _name = 'ctm.sale.lagune'

    date = fields.Date('Date')
    representant = fields.Many2one('excursion.guide', string='representant hotel',
                                   domain=[('etat', '=', 'representant')])
    produit = fields.Char('Produit')
    prix = fields.Float('prix de vente', digits=(10, 3))
    commission = fields.Float('commission representant', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')

    @api.model
    def create(self, vals):
        vals['commission'] = vals['prix'] * 0.05
        rec = super(fhgfjgkjhk, self).create(vals)
        return rec


class kjfekjfhfjnndbgkjd(models.Model):
    _name = 'ctm.commission.lagune'
    _rec_name = 'date_from'
    _description = 'etat commission thalasso par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("Chiffre d'affaire")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission = fields.Monetary('commission')


class kjfekjfhfjnndbgkjd(models.Model):
    _name = 'ctm.commission.bella_marina'
    _rec_name = 'date_from'
    _description = 'etat commission bella_marina par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("nombre de pax")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission = fields.Monetary('commission representant')
    commission_to = fields.Monetary('commission agence')


class kjfekjfhfjnndbgkjd(models.Model):
    _name = 'ctm.commission.levoilier'
    _rec_name = 'date_from'
    _description = 'etat commission le voilier par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("nombre de pax")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission = fields.Monetary('commission representant')
    commission_to = fields.Monetary('commission agence ')


class kjfekjfhfjnndbgkjd(models.Model):
    _name = 'ctm.commission.lether_shop'
    _rec_name = 'date_from'
    _description = 'etat commission lether_shop par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("Chiffre d'affaire")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission = fields.Monetary('commission representant')
    commission_to = fields.Monetary('commission agence')


class kjfekjfhfjnndbgkjd(models.Model):
    _name = 'ctm.commission.photograph'
    _rec_name = 'date_from'
    _description = 'etat commission photographe par periode'

    @api.one
    def get_currency(self):
        self.currency_id = self.env.user.company_id.id

    date_from = fields.Date('De')
    date_to = fields.Date('à')
    sale_number = fields.Monetary("Chiffre d'affaire")
    currency_id = fields.Many2one('res.currency', default=get_currency)
    etat_id = fields.Many2one('etat.guide.target.commision')
    commission = fields.Monetary('commission representant')
    commission_to = fields.Monetary('commission agence')


class fsdjhfhjbfkj(models.Model):
    _name = "etat.guide.target.commision"
    _rec_name = 'show_name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    guide = fields.Many2one('excursion.guide', string="Guide", required=True, domain=[('etat', '=', 'representant')])
    show_name = fields.Char('Nom guide')
    target_detail = fields.One2many('target.detail', 'etat_id', string="Detail Commision excursion")
    commission_thalasso = fields.One2many('ctm.commission.thalasso', 'etat_id', string='commission thalasso')
    commision_lagune = fields.One2many('ctm.commission.lagune', 'etat_id', string='Commission lagune')
    commision_bella_marina = fields.One2many('ctm.commission.bella_marina', 'etat_id', string='Commission bella marina')
    commision_levoilier = fields.One2many('ctm.commission.levoilier', 'etat_id', string='Commission le voilier')
    commision_lether_shop = fields.One2many('ctm.commission.lether_shop', 'etat_id', string='Commission lether shop')
    commision_photograph = fields.One2many('ctm.commission.photograph', 'etat_id', string='Commission photograph')
    currency_id = fields.Many2one('res.currency')

    _sql_constraints = [
        ('guide_uniq', 'unique (guide)', "Vous ne pouvez avoir deux enregistrement pour le méme guide !"),
    ]

    # @api.multi
    # def get_target(self):
    #     return True

    @api.onchange('guide')
    def test_guide(self):
        self.target_detail = []

    @api.model
    def create(self, vals):
        guide = vals['guide']
        rec = self.env['excursion.guide'].search([('id', '=', guide)])
        vals['show_name'] = rec.name
        rec = super(fsdjhfhjbfkj, self).create(vals)
        return rec


class slkdjnfkjsdf(models.Model):
    _name = "target.detail"

    @api.model
    def get_currency(self):
        return self.env.user.company_id.currency_id.id

    date_from = fields.Date('de')
    date_to = fields.Date('à')
    paxe = fields.Float('Paxe arrivé')
    paxe_sale = fields.Float('Paxe gagné')
    sale_amount = fields.Monetary('Sale amount')
    currency_id = fields.Many2one('res.currency', default=get_currency)
    # hotel_id = fields.Many2one('rooming.hotels', string='Hotel')
    target = fields.Monetary(string="Target", digits=(10, 2))
    target_rate = fields.Float(string="Porcentage de retenue", digits=(10, 3))
    commission = fields.Monetary(string="Commision", digits=(10, 3))
    etat_id = fields.Many2one('etat.guide.target.commision')


class AgenceTransport(models.Model):
    _name = 'liquidation.agence.transport'
    _rec_name = 'name'
    name = fields.Char('Transporteur')


class Chauffeur(models.Model):
    _inherit = 'ctm.conductor'
    agence_transporteur = fields.Many2one('liquidation.agence.transport', string='Transporteur')


class VenteExcursion(models.Model):
    _name = 'vente.excursion'
    arrivee = fields.Date('Arrivée Du')
    hotel_id = fields.Many2one('rooming.hotels', string='hotel')
    zone_id = fields.Many2one('excursion.emplacement', string='Zone')
    tour_operateur = fields.Many2one('tour.operator', string='Tour Operateur')
    representant_id = fields.Many2one('excursion.guide', string='Representant')
    excursion_id = fields.Many2one('excursion.excursion', string='Excursion')
    nbr_adulte = fields.Integer('Nbre Adulte')
    nbr_enfant = fields.Integer('Nbre Enfant')
    nbr_bebe = fields.Integer('Nbre Bébé')
    produit = fields.Char('Produit')
    currency_id = fields.Many2one('res.currency')


class MouvementGuide(models.Model):
    _name = 'mouvement.guide'
    date = fields.Date('Date')
    guide_principale = fields.Many2one('excursion.guide', string="Guide Principale")
    guide_doubleur = fields.Many2one('excursion.guide', string="Guide Doubleur")
    chauffeur_id = fields.Many2one('ctm.conductor', string="Chauffeur")
    transporteur_id = fields.Many2one('liquidation.agence.transport', string='Transporteur')
    excursion_id = fields.Many2one('excursion.excursion', string="Excursion")
    nbr_adulte = fields.Integer('Nbre Adulte')
    nbr_enfant = fields.Integer('Nbre Enfant')

    # @api.model
    # def create(self, vals):
    #     rec_plan_excursion = self.env['excursion.movementday'].search([('date_m', '=', vals['date'])])
    #     vals['chauffeur'] = rec_plan_excursion[0].chauffeur.id
    #     vals['guide_principale'] = rec_plan_excursion[0].guide_principale.id
    #
    #     rec = super(Extra, self).create(vals)
    #     return rec


class AjJazira(models.Model):
    _name = "liquidation.aljazira"
    # _rec_name = "Aljazira"
    _description = "les états de vente de type AlJazira"

    date = fields.Date("Date d'Excursion")
    tour_operateur = fields.Many2one('tour.operator', string='Tour Operateur')
    guide_excursion = fields.Many2one('excursion.guide', string='guide Excursion')

    chiffre_affaire_condition = fields.Float("chiffre d'affaire conditionné", digits=(10, 3))
    quantite_huile = fields.Float("quantité d'huiles en Vrac", digits=(10, 3))

    commission_guide = fields.Float('commission guide', digits=(10, 3))
    commisson_to = fields.Float('commission agence', digits=(10, 3))
    chiffre_affaire_total = fields.Float("chiffre d'affaire total", digits=(10, 3))
    chiffre_affaire_vrac = fields.Float("chiffre d'affaire en vrac", digits=(10, 3))
    currency_id = fields.Many2one('res.currency')

    @api.model
    def create(self, vals):
        config_jazira = self.env['liquidation.configjazira'].search(
            [('date_debut_saison', '<=', vals['date']), ('date_fin_saison', '>=', vals['date'])])
        vals['commission_guide'] = (vals['chiffre_affaire_condition'] * config_jazira[
            0].commission_guide_condition) / 100 + config_jazira[0].commission_guide * vals['quantite_huile']
        vals['commisson_to'] = (vals['chiffre_affaire_condition'] * config_jazira[
            0].commission_agence_condition) / 100 + config_jazira[0].commission_agence * vals['quantite_huile']

        vals['chiffre_affaire_vrac'] = vals['quantite_huile'] * config_jazira[0].prix_litre
        vals['chiffre_affaire_total'] = vals['chiffre_affaire_condition'] + vals['chiffre_affaire_vrac']

        rec = super(AjJazira, self).create(vals)
        return rec


class Tapis(models.Model):
    _name = "liquidation.tapis"
    _description = "etat de vente tapis"

    date = fields.Date("Date d'Excursion")
    guide_excursion = fields.Many2one('excursion.guide', string='guide Excursion')
    chauffeur_excursion = fields.Many2one('ctm.conductor', string='Chauffeur')
    tour_operateur = fields.Many2one('tour.operator', string='Tour Operateur')
    chiffre_affaire = fields.Float("chiffre d'affaire", digits=(10, 3))
    commission_guide = fields.Float('commission guide', digits=(10, 3))
    commission_chauffeur = fields.Float('commission chauffeur', digits=(10, 3))
    commission_to = fields.Float('commission agence', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')

    @api.model
    def create(self, vals):
        config_tapis = self.env['liquidation.configtapis'].search(
            [('date_debut_saison', '<=', vals['date']), ('date_fin_saison', '>=', vals['date'])])
        vals['commission_guide'] = (vals['chiffre_affaire'] * config_tapis[0].commission_guide * config_tapis[
            0].commission_total) / 10000
        vals['commission_chauffeur'] = (vals['chiffre_affaire'] * config_tapis[0].commission_chauffeur * config_tapis[
            0].commission_total) / 10000
        vals['commission_to'] = (vals['chiffre_affaire'] * config_tapis[0].commission_agence * config_tapis[
            0].commission_total) / 10000

        rec = super(Tapis, self).create(vals)
        return rec


class EtatLiquidation(models.Model):
    _name = 'etat.liquidation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "nbr_etat"
    nbr_etat = fields.Integer('N° Etat')
    reps = fields.Many2one('excursion.guide', string="Reps")
    date_liquidation = fields.Date('Date de Liquidation', default=str(datetime.today()))
    type_liquidation = fields.Selection(string='Type liquidation',
                                        selection=[('Excursion', 'Excursion'), ('Thalasso', 'Thalasso')])
    chiffre_affaire = fields.Float("Chiffre D'Affaire", digits=(10, 3))
    commission = fields.Float("Commission", digits=(10, 3))
    retenue = fields.Float('Retenue 3%', digits=(10, 3))
    net = fields.Float('Net à Payer', digits=(10, 3))
    date_paiment_commission = fields.Date('Date de Paiment de Commission')
    payed = fields.Boolean('Payé ')
    currency_id = fields.Many2one('res.currency')


class Configchameau(models.Model):
    _name = 'liquidation.configchameau'
    _description = 'les configuiration des commissions et prix de chameau'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    prix_achat = fields.Float('prix achat', digits=(10, 3))
    prix_vente = fields.Float('prix vente', digits=(10, 3))
    commission_vendeur = fields.Float('commission représentant', digits=(10, 3))
    commission_chauffeur = fields.Float('commission chauffeur', digits=(10, 3))
    commission_guide = fields.Float('commission guide excursion', digits=(10, 3))
    commission_agence = fields.Float('commission agence', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class Configtapis(models.Model):
    _name = 'liquidation.configtapis'
    _description = 'les configuiration des commissions des tapis'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    commission_total = fields.Float('commission total en %', digits=(10, 3))
    commission_chauffeur = fields.Float('commission chauffeur en %', digits=(10, 3))
    commission_guide = fields.Float('commission guide excursion en %', digits=(10, 3))
    commission_agence = fields.Float('commission agence en %', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class Configjazira(models.Model):
    _name = 'liquidation.configjazira'
    _description = 'les configuirations des commissions de aljazira'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    prix_litre = fields.Float("prix litre d'huile en Vrac", digits=(10, 3))
    commission_guide_condition = fields.Float('commission guide conditionné en %', digits=(10, 3))
    commission_agence_condition = fields.Float('commission agence conditionné en %', digits=(10, 3))
    commission_guide = fields.Float('commission guide excursion par litre en Vrac', digits=(10, 3))
    commission_agence = fields.Float('commission agence par litre en Vrac', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class Configrestaurant(models.Model):
    _name = 'liquidation.configrestaurant'
    _description = 'les configuirations des commissions des restaurants'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    nom_restaurant = fields.Selection(string='Nom restaurant',
                                      selection=[('Bella Marina', 'Bella Marina'),
                                                 ('Le voilier', 'Le voilier'
                                                  )])
    commission_representant = fields.Float('commission représentant', digits=(10, 3))
    commission_agence = fields.Float('commission agence', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class Configquatre(models.Model):
    _name = 'liquidation.quatrefois'
    _description = 'les configuration des prix et commissions 4*4'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    prix_vente = fields.Float('prix de vente par pax', digits=(10, 3))
    commission_representant = fields.Float('commission représentant', digits=(10, 3))
    prix_location = fields.Float('prix location 4*4', digits=(10, 3))
    frais_chauffeur = fields.Float('frais chauffeur 4*4', digits=(10, 3))
    commission_max = fields.Float('commission max par pax', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


# class Configsahara(models.Model):
#     _name = 'liquidation.configsahara'
#     _description = 'les configurations des commissions chauffeurs sahara'
#
#     date_debut_saison = fields.Date('date début saison')
#     date_fin_saison = fields.Date('date fin saison')
#     commission_chauffeur = fields.Float('commission chauffeur')
# liste_excursion_sahara = fields.One2many('excursion.excursion', 'config_sahara', string='liste excursions sahara')


class Bareme(models.Model):
    _name = 'ctm.liquidation.bareme'

    _description = "les baremes des commission des excursions"

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')

    pourcentage_commission = fields.Float('Pourcentage appliqué', digits=(10, 3))
    borne_supperieur = fields.Float('Borne supperieur', digits=(10, 3))
    borne_inferieur = fields.Float('Borne inferieur', digits=(10, 3))


class ConfigurationPhotograph(models.Model):
    _name = 'liquidation.configphoto'
    _description = 'les configurations de commisson photographe'

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    prix_photo = fields.Float('prix session de photo', digits=(10, 3))
    commission_to = fields.Float('commission agence', digits=(10, 3))
    commission_rep = fields.Float('commission representant', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class sdlkfnksjhgkgjb(models.Model):
    _name = 'commission.chauffeur.extra'

    date = fields.Date('Date')
    chauffeur = fields.Many2one('ctm.conductor', string='chauffeur')
    amount = fields.Float('Montant', digits=(10, 3))
    guide = fields.Many2one('excursion.guide', string='Guide', domain=[('etat', '=', 'principale')])


class sdohfbsdjn(models.Model):
    _name = 'commission.chauffeur'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    date_from = fields.Date('Date debut')
    date_to = fields.Date('Date fin')
    chauffeur = fields.Many2one('ctm.conductor', string='chauffeur')
    commisssion = fields.Float('Commission', digits=(10, 3))
    detail_commission = fields.One2many('commission.chauffeur.detail', 'comm_chff_id', string='Details du commisssion')
    currency_id = fields.Many2one('res.currency')


class osidfgidnkjfn(models.Model):
    _name = 'commission.chauffeur.detail'

    sale_camel = fields.Float('Vente chameaux', digits=(10, 3))
    sale_tapis = fields.Float('Vente tapis', digits=(10, 3))
    pax_sahara = fields.Float('pax chameaux', digits=(10, 3))
    commission_camel = fields.Float('commission chameaux', digits=(10, 3))
    commission_tapis = fields.Float('commission tapis', digits=(10, 3))
    # commission_sahara = fields.Float('commission sahara', digits=(10, 3))
    comm_chff_id = fields.Many2one('commission.chauffeur')
    extra = fields.Float('Commission extra', digits=(10, 2))
    currency_id = fields.Many2one('res.currency')


class fisdhbfjbgffbgd(models.Model):
    _name = 'commission.excursion.guide'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    guide_id = fields.Many2one('excursion.guide', string='Guide', domain=[('etat', '=', 'principale')])
    date_from = fields.Date('Date debut')
    date_to = fields.Date('Date fin')
    commission = fields.Float('Commission', digits=(10, 3))
    commission_detail = fields.One2many('commission.excursion.guide.detail', 'commggid', 'Details du commission')
    currency_id = fields.Many2one('res.currency')


class zdjfkjsbkjgb(models.Model):
    _name = 'commission.excursion.guide.detail'

    commggid = fields.Many2one('commission.excursion.guide')
    sale_camel = fields.Float('Vente chameaux', digits=(10, 3))
    sale_quad = fields.Float('Vente 4x4', digits=(10, 3))
    cost_quad = fields.Float('cout 4x4', digits=(10, 3))
    sale_tapis = fields.Float('Vente tapis', digits=(10, 3))
    sale_oil = fields.Float('C.AFF al jazira embalé 20%', digits=(10, 3))
    oil_oil = fields.Float('C.AFF al jazira en vrac', digits=(10, 3))
    double_guide_bonus = fields.Boolean('prime guide doubleur')
    commission_camel = fields.Float('commission chameaux', digits=(10, 3))
    commission_quatre = fields.Float('commission 4*4', digits=(10, 3))
    commission_tapis = fields.Float('commission tapis', digits=(10, 3))
    commission_aljazira = fields.Float('Commission al jazira', digits=(10, 3))
    commission_double_guide = fields.Float('Commission guide doubleur', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class NumReservation(models.Model):
    _name = 'liquidation.numreservation'
    _rec_name = "date"
    _description = " NOmbres des reservation dans une date Donnée"
    date = fields.Date('Date Reservation')
    number_reservation = fields.Integer('numéro réservation')
    pax = fields.Float('Paxe', digits=(10, 3))
    hotel = fields.Many2one('rooming.hotels', string='Hotel')
    adulte = fields.Float('Nombre des adultes', digits=(10, 3))
    enfant = fields.Float('Nombre des enfants', digits=(10, 3))
    bebe = fields.Float('Nombre des bébés', digits=(10, 3))


class Historiquerepresentant(models.Model):
    _name = 'liquidation.historiquerep'
    _description = 'historique des affectations des guides hotels'

    date_debut = fields.Date('date début')
    date_fin = fields.Date('date fin')
    hotel_id = fields.Many2many('rooming.hotels', string='Hotel')
    pax_adulte = fields.Float('pax adulte')
    pax_enfant = fields.Float('pax enfant')
    pax = fields.Float('nombre de pax', digits=(10, 2))
    representant = fields.Many2one('excursion.guide', string='représentant', domain=[('etat', '=', 'representant')])
    to = fields.Many2many('tour.operator', strring="Tour operator")
    target_rep = fields.Float('target')

    @api.multi
    def write(self, vals):

        sum_pax = 0
        sum_pax_adulte = 0
        sum_pax_enfant = 0
        rec1 = self.ids[0]
        rec1 = self.env['liquidation.historiquerep'].search([('id', '=', rec1)])
        domain = []
        lto = []
        to = []
        try:
            dt = vals['date_fin']
        except:
            dt = self.date_fin
        try:
            to = vals['to'][0][2]
        except:
            to = []

        if len(self.env['liquidation.historiquerep'].search(
                [('date_fin', '>=', dt), ('date_debut', '<=', dt), ('representant', '=', self.representant.id)])) > 1:
            raise UserError('vérifier date fin ')

        for hotel in rec1.hotel_id:
            if len(to) == 0:

                domain = [('hotel_id', '=', hotel.id), ('chekin', '>=', rec1.date_debut),
                          ('chekin', '<=', dt)]
            else:
                for x in to:
                    lto.append(x)
                domain = [('hotel_id', '=', hotel.id), ('chekin', '>=', rec1.date_debut),
                          ('chekin', '<=', dt), ('touroperator_id', 'in', lto)]
            rec_reservations = self.env['ctm.reservation.list'].search(
                domain,
                order='chekin')

            sum_hotel = 0
            pax_adult = 0
            pax_enfant = 0
            calculate = True
            for x in rec_reservations:
                for detail in x.reservation_detail:
                    if detail.status == "Cancelled":
                        calculate = False
                if calculate:
                    pax_adult = pax_adult + x.pax_adult
                    pax_enfant = pax_enfant + x.pax_enfant

            sum_pax_adulte = sum_pax_adulte + pax_adult
            sum_pax_enfant = sum_pax_enfant + pax_enfant
            sum_pax = sum_pax_adulte + sum_pax_enfant / 2
        self._cr.execute(
            "update liquidation_historiquerep set pax ={0}, pax_adulte = {1} , pax_enfant = {2} where id = {3}".format(
                sum_pax, sum_pax_adulte, sum_pax_enfant,
                rec1.id))
        rec = super(Historiquerepresentant, self).write(vals)
        return rec

    @api.multi
    def target(self, vals):
        total_vent = 0
        for x in self.representant:
            for y in self.env['excursion.reservations'].search(
                    [('dat', '>=', self.date_debut), ('dat', '<=', self.date_fin), ('vendeur_id', '=', x.id)]):
                total_vent = total_vent + y.selling_price

        self.target_rep = total_vent / self.pax


class Pourcentageadulte(models.Model):
    _name = 'liquidation.pourcentageadulte'
    _description = 'pourcentage des adultes das les excursions'

    date_debut = fields.Date("date début")
    date_fin = fields.Date("date fin")
    excursion = fields.Many2one('excursion.excursion', string="Excursion name")
    representant = fields.Many2one('excursion.guide', string="Seller name")
    pourcentage = fields.Float('%adulte', digits=(10, 3))
