from odoo import models, fields, api


class Thalasso(models.Model):
    _name = 'liquidation.thalasso'
    _rec_name = 'reservation'
    _description = "cette classe permet d'afficher les données de thalasso"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    representant = fields.Many2many('excursion.guide', string='representant hotel',
                                    domaine=[('etat', '=', 'representant')])
    vochar = fields.Char('Voucher')
    reservation = fields.Char('Num reservation')
    date_arrivee = fields.Date("date d'arrivée")
    nom_hotel = fields.Many2one('rooming.hotels', string='Hotels')
    nom_agence = fields.Char('agence')
    centre_thalasso = fields.Many2one('liquidation.centrethalasso', string='centres thalasso')
    cure = fields.Char('Cure')
    cure_thalasso = fields.Many2one('liquidation.cure', string="cures")
    nembre_jours = fields.Char('nembre de jours')
    nembre_soins = fields.Char('nembre de soins')
    paxe = fields.Integer('paxe')
    tarif = fields.Float('montant', digits=(10, 3))
    tarif_agence = fields.Float("tarif d'agence")
    commission_to = fields.Float('Commission TO', digits=(10, 3))
    commission = fields.Float("commision guide", digits=(10, 3))
    date = fields.Date("date")
    date_recu = fields.Date("date d'encaissement")
    date_paiement = fields.Date('date de paiement')
    numero_etat = fields.Char("N° VT", required=True)
    pourcentage = fields.Float('pourcentage')
    num_reservation = fields.Many2one('ctm.reservation.list',
                                      string="num reservation")
    statut = fields.Selection(selection=[('confirmé', 'confirmé'), ('non confirmé', 'non confirmé')], string="statut")
    currency_id = fields.Many2one('res.currency')
    client_name = fields.Text('Nom de client')

    @api.multi
    def confirmer(self):
        self.statut = 'confirmé'
        self.commission = self.tarif * self.pourcentage / 100

    @api.multi
    def deconfirmer(self):
        self.statut = 'non confirmé'
        self.commission = 0

    @api.onchange('num_reservation')
    def change_reserv(self):
        if self.num_reservation:
            name = ""
            for x in self.num_reservation.reservation_detail:
                name = name + x.client_name + "\n"
            return self.update({
                'nom_hotel': self.num_reservation.hotel_id.id,
                'client_name': name,
            })

    # @api.model
    # def create(self, vals):
    #     centre_id = vals['centre_thalasso']
    #     centre = self.env['liquidation.centrethalasso'].search([('id', '=', centre_id)])
    #     commision_to = (vals['tarif'] * centre.pourcentage_cure) / 100
    #     commission_guide = commision_to * 0.4
    #     vals['commission'] = commission_guide
    #     vals['commission_to'] = commision_to
    #
    #     rec = super(Thalasso, self).create(vals)
    #     return rec


class Cure(models.Model):
    _name = 'liquidation.cure'
    _rec_name = 'nom_cure'
    _description = "cette classe permet d'afficher les données de cure"

    code = fields.Char('code', required=True)
    nom_cure = fields.Char('nom des cures')
    prix_individuel = fields.Float('prix individuel', digits=(10, 3))
    prix_agence = fields.Float('prix agence', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')


class CentreThalasso(models.Model):
    _name = 'liquidation.centrethalasso'
    _rec_name = 'nom_centre'
    _description = "cette classe permet d'afficher les centres thalasso"

    code = fields.Char('code', required=True)
    nom_centre = fields.Char('centre thalasso')
    centre_base = fields.Boolean('centre de base')
    num_telephone = fields.Integer('numéro de téléphone')
    nom_hotel = fields.Many2many('rooming.hotels', string='Hotel')
    pourcentage_cure = fields.Float('% cures')
    pourcentage_carte = fields.Float('% à la carte')
    cure_id = fields.Many2many('liquidation.cure', string='cures')


class Etatliquidationthalasso(models.Model):
    _name = 'liquidation.etatliquidationthalasso'
    _rec_name = 'date_liquidation'
    _description = "cette classe permet d'afficher la liquidation thalasso"

    code = fields.Char("n° d'état", required=True)
    representant = fields.Many2one('excursion.guide', string='reps')
    date_liquidation = fields.Date('date de liquidation')
    type_liquidation = fields.Char('type liquidation')
    tarif_individuel = fields.Float('tarif individuel', digits=(10, 3))
    tarif_agence = fields.Float('tarif agence', digits=(10, 3))
    commision_reps = fields.Float('commision reps', digits=(10, 3))
    net_payer = fields.Float('net à payer', digits=(10, 3))
    date_paiement_commision = fields.Date("date de paiement commision")
    currency_id = fields.Many2one('res.currency')
    paye = fields.Boolean('payé')


class Configthalasso(models.Model):
    _name = 'liquidation.configthalasso'
    _description = "configuration des commissions thalasso"

    date_debut_saison = fields.Date('date début saison')
    date_fin_saison = fields.Date('date fin saison')
    montant_moyen = fields.Float('montant moyen minimum', digits=(10, 3))
    currency_id = fields.Many2one('res.currency')
    centre_base = fields.Boolean('centre de base')
    commission_representant_max = fields.Float('commission representant max en %', digits=(10, 3))
    commission_representant_min = fields.Float('commission representant min en %', digits=(10, 3))
