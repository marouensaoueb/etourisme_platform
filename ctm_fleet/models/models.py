# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields, api, exceptions


class ReportVehiclesUsage(models.Model):
    _name = 'report.vehicle.usage'
    _order = 'date_from'
    _rec_name = 'company_id'

    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')
    company_id = fields.Many2one('res.partner', string='Client')
    vehicle = fields.Many2one('fleet.vehicle', string='Voiture')
    matricule = fields.Char(related='vehicle.license_plate', string='Matricule')
    sale_price = fields.Float('Prix vente', digits=(10, 3))
    cost = fields.Float('Cout', digits=(10, 3))
    marge = fields.Float('Marge', digits=(10, 3))
    margetx = fields.Float('Taux de marge', digits=(10, 3))
    avance = fields.Float('Avance', digits=(10, 3))
    state = fields.Char('Etat')
    contact = fields.Char('Personne de contact')


class VehiculeFleet(models.Model):
    _inherit = 'fleet.vehicle'
    _order = 'model_id'
    driver_id = fields.Many2one('ctm.conductor', string="Conducteur", track_visibility='onchange')
    lo = fields.Boolean('Location ? ', track_visibility='onchange')
    personnel = fields.Boolean('Personnel ? ', track_visibility='onchange')
    debut_exp = fields.Date("debut d'exploitation", track_visibility='onchange')
    fin_exp = fields.Date("fin d'exploitation", track_visibility='onchange')
    date_visite = fields.Date("date de visite ", track_visibility='onchange')

    date_assurence = fields.Date("date d'assurence", track_visibility='onchange')
    taxe_vignette = fields.Integer(" Taxe Vignette ", track_visibility='onchange')
    dat_taxe_vignette = fields.Date(" date Taxe Vignette ", track_visibility='onchange')
    nbr_siege = fields.Integer("nombre de siege ", track_visibility='onchange')
    typess = fields.Many2one('ctm.vehicle.type', string="Type de vehicule")


class CtmConductor(models.Model):
    _name = "ctm.conductor"
    _rec_name = "name"

    name = fields.Char('Nom conducteur', required=True, track_visibility='onchange')
    adresse = fields.Char('adresse conducteur', track_visibility='onchange')
    num_cin = fields.Char('Numero Cin conducteur', required=True, track_visibility='onchange')
    num_tel = fields.Char('numero Telephone conducteur', required=True, track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string="Employé  lié", track_visibility='onchange')

    @api.onchange('employee_id')
    def auto_remplir(self):
        self.name = self.employee_id.name
        self.num_cin = self.employee_id.identification_id
        self.num_tel = self.employee_id.mobile_phone
        self.adresse = self.employee_id.adresse_personel


class CtmEmployee(models.Model):
    _inherit = 'hr.employee'
    identification_id = fields.Char(string='numero de cin ', required=True, track_visibility='onchange')
    adresse_personel = fields.Char(string='addresse reél', track_visibility='onchange')


class VehicleState(models.Model):
    _name = "ctm.vehicle.state"
    _rec_name = "vehicle"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    vehicle = fields.Many2one('fleet.vehicle', string="Vehicule", track_visibility='onchange')
    chauffeur = fields.Many2one('ctm.conductor', string="Chauffeur", track_visibility='onchange')
    lykm = fields.Float('Derniére année KM', readonly=True, digits=(10, 0), track_visibility='onchange')
    circdate = fields.Date("Date d'acqusition ", readonly=True, track_visibility='onchange')
    date_visite = fields.Date('Date de Visite', readonly=True, track_visibility='onchange')
    dat_assurance = fields.Date("Date Assurance", readonly=True, track_visibility='onchange')
    tax_v = fields.Char("Taxe Vignette", readonly=True, track_visibility='onchange')
    dat_tax_v = fields.Date("Date Taxe Vignette", readonly=True, track_visibility='onchange')
    debut_exploit = fields.Date("Debut d'exploitation", readonly=True, track_visibility='onchange')
    fin_exploit = fields.Date("Fin d'exploitation", readonly=True, track_visibility='onchange')
    lo = fields.Boolean('Location', readonly=True, track_visibility='onchange')
    personnel = fields.Boolean('Personnel ', readonly=True, track_visibility='onchange')
    agence = fields.Char('Agence', readonly=True, track_visibility='onchange')
    modele = fields.Char('Modele', readonly=True, track_visibility='onchange')
    type_vehicle = fields.Char('Type de Vehicle', readonly=True, track_visibility='onchange')
    nbr_siege = fields.Char('Nombre de Siege ', readonly=True, track_visibility='onchange')
    state = fields.Selection(string="state", selection=[('v', 'verrouillé'), ('nv', 'non verrouillé')],
                             track_visibility='onchange')
    statedetail = fields.One2many('ctm.vehicle.state.detail', 'state_id', 'Details des dépenses journaliére',
                                  track_visibility='onchange')
    intervention_detail = fields.One2many('ctm.intervention.detail', 'state_id', 'Details des Intervention',
                                          track_visibility='onchange')

    _sql_constraints = [
        ('vehicle_uniq', 'unique (vehicle)', "Vous ne pouvez avoir deux enregistrement de la méme voiture !"),
    ]

    @api.multi
    def lock_rec(self):
        return self.update({
            'state': 'v'
        })

    @api.multi
    def unlock_rec(self):
        return self.update({
            'state': 'nv'
        })

    @api.multi
    def refresh_d(self):
        self.chauffeur = self.vehicle.driver_id
        self.lykm = self.vehicle.odometer
        self.circdate = self.vehicle.acquisition_date
        self.date_visite = self.vehicle.date_visite

        self.dat_assurance = self.vehicle.date_assurence
        self.tax_v = self.vehicle.taxe_vignette
        self.dat_tax_v = self.vehicle.dat_taxe_vignette
        self.debut_exploit = self.vehicle.debut_exp
        self.fin_exploit = self.vehicle.fin_exp
        self.lo = self.vehicle.lo
        self.personnel = self.vehicle.personnel
        self.agence = self.vehicle.tag_ids.name
        self.modele = self.vehicle.model_id.brand_id.name
        self.type_vehicle = self.vehicle.typess.name
        self.nbr_siege = self.vehicle.nbr_siege

    def refresh_d_mult(self):
        for x in self:
            x.chauffeur = x.vehicle.driver_id
            x.lykm = x.vehicle.odometer
            x.circdate = x.vehicle.acquisition_date
            x.date_visite = x.vehicle.date_visite

            x.dat_assurance = x.vehicle.date_assurence
            x.tax_v = x.vehicle.taxe_vignette
            x.dat_tax_v = x.vehicle.dat_taxe_vignette
            x.debut_exploit = x.vehicle.debut_exp
            x.fin_exploit = x.vehicle.fin_exp
            x.lo = x.vehicle.lo
            x.personnel = x.vehicle.personnel
            x.agence = x.vehicle.tag_ids.name
            x.modele = x.vehicle.model_id.brand_id.name
            x.type_vehicle = x.vehicle.typess.name
            x.nbr_siege = x.vehicle.nbr_siege
            for y in x.statedetail:
                y.lo = x.lo
                y.personnel = x.personnel
            for z in x.intervention_detail:
                z.lo = x.lo
                z.personnel = x.personnel

    @api.model
    def create(self, vals):
        vals['state'] = "nv"
        rec = super(VehicleState, self).create(vals)
        return rec

    @api.onchange('vehicle')
    def fill_attrs(self):
        if self.vehicle:
            self.chauffeur = self.vehicle.driver_id
            self.lykm = self.vehicle.odometer
            self.circdate = self.vehicle.acquisition_date
            self.date_visite = self.vehicle.date_visite
            self.dat_assurance = self.vehicle.date_assurence
            self.tax_v = self.vehicle.taxe_vignette
            self.dat_tax_v = self.vehicle.dat_taxe_vignette
            self.debut_exploit = self.vehicle.debut_exp
            self.fin_exploit = self.vehicle.fin_exp
            self.lo = self.vehicle.lo
            self.personnel = self.vehicle.personnel
            self.agence = self.vehicle.tag_ids.name
            self.modele = self.vehicle.model_id.brand_id.name
            self.type_vehicle = self.vehicle.typess.name
            self.nbr_siege = self.vehicle.nbr_siege


class VehicleStatedetail(models.Model):
    _name = "ctm.vehicle.state.detail"
    _rec_name = "dat"
    _order = "dat"

    @api.one
    @api.depends('entretien', 'changepieces', 'reparation', 'Parking', 'carbs', 'vulc', 'othercharges')
    def compute_total_charges(self):
        self.total_charges = self.entretien + self.changepieces + self.reparation + self.Parking + self.carbs \
                             + self.vulc + self.othercharges

    @api.one
    @api.depends('kmend', 'kmstart')
    def compute_overallkm(self):
        self.kmoverall = self.kmend - self.kmstart

    @api.one
    @api.depends('state_id')
    def get_vehicle_model(self):
        self.vehicle_model_id = self.state_id.vehicle.model_id

    @api.one
    @api.depends('state_id')
    def get_lo(self):
        self.lo = self.state_id.vehicle.lo

    @api.one
    @api.depends('state_id')
    def get_personnel(self):
        self.personnel = self.state_id.vehicle.personnel

    @api.one
    @api.depends('total_charges', 'kmoverall', 'kmend')
    def compute_prk(self):
        if self.kmoverall:
            self.prk = self.total_charges / self.kmoverall
        if self.kmend < self.kmstart:
            raise exceptions.UserError("le km fin ne peut pas etre moins de km debut")

    @api.multi
    def lock_state(self):
        return self.update({
            'state': 'v'
        })

    @api.multi
    def unlock_state(self):
        return self.update({
            'state': 'nv'
        })

    state = fields.Selection(string="state", selection=[('v', 'verrouillé'), ('nv', 'non verrouillé')],
                             track_visibility='onchange')
    dat = fields.Date('Date', required=True, track_visibility='onchange')
    num_ordre_mission = fields.Char('Numer ordre de mission', track_visibility='onchange')
    kmstart = fields.Float('KM Début', digits=(10, 0), track_visibility='onchange')
    kmend = fields.Float('KM Fin', digits=(10, 0), track_visibility='onchange')
    kmoverall = fields.Float('KM Parcorue', digits=(10, 0), compute=compute_overallkm, store=True,
                             track_visibility='onchange')
    entretien = fields.Float('Entretien', digits=(10, 3), track_visibility='onchange')
    changepieces = fields.Float('Piéce de rechange', digits=(10, 3), track_visibility='onchange')
    reparation = fields.Float('Réparation', digits=(10, 3), track_visibility='onchange')
    Parking = fields.Float('Parking', digits=(10, 3), track_visibility='onchange')
    peage = fields.Float('Péage', digits=(10, 3), track_visibility='onchange')
    carbs = fields.Float('Carburon consommé', digits=(10, 3), track_visibility='onchange')
    vulc = fields.Float('Vulcanisation', digits=(10, 3), track_visibility='onchange')
    othercharges = fields.Float('Autre charges', digits=(10, 3), track_visibility='onchange')
    total_charges = fields.Float('Total des charges', digits=(10, 3), compute=compute_total_charges, store=True,
                                 track_visibility='onchange')
    observation = fields.Text('Observation', track_visibility='onchange')
    state_id = fields.Many2one('ctm.vehicle.state', string="Vehicule", track_visibility='onchange')
    vehicle_model_id = fields.Many2one('fleet.vehicle.model', store=True, compute=get_vehicle_model,
                                       track_visibility='onchange')
    lo = fields.Boolean('Location ?', store=True, compute=get_lo, track_visibility='onchange')
    personnel = fields.Boolean('Personnel ?', store=True, compute=get_personnel, track_visibility='onchange')
    prk = fields.Float('PRK', compute=compute_prk, store=True, digits=(1, 4), track_visibility='onchange')

    @api.model
    def create(self, vals):
        dae = vals['dat']
        cont = self.env['ctm.vehicle.state.detail'].search([('dat', '=', dae), ('state_id', '=', vals['state_id'])])
        if len(cont) > 0:
            raise exceptions.UserError(
                'vous ne pouvez pas entrer deux enregistrement de la méme date pour la méme voiture')
        rec = super(VehicleStatedetail, self).create(vals)
        return rec

    @api.one
    @api.constrains('dat')
    def control_date(self):
        if self.dat > datetime.today().date():
            raise UserWarning("You can't enter a date that is supperior of today")


class InterventionDetails(models.Model):
    _name = 'ctm.intervention.detail'
    _rec_name = 'dat'
    _order = "dat"

    @api.one
    @api.depends('state_id')
    def get_vehicle_model(self):
        self.vehicle_model_id = self.state_id.vehicle.model_id

    @api.one
    @api.depends('state_id')
    def get_lo(self):
        self.lo = self.state_id.vehicle.lo

    @api.one
    @api.depends('state_id')
    def get_personnel(self):
        self.personnel = self.state_id.vehicle.personnel

    @api.multi
    def lock_det(self):
        return self.update({
            'state': 'v'
        })

    @api.multi
    def unlock_det(self):
        return self.update({
            'state': 'nv'
        })

    state = fields.Selection(string="state", selection=[('v', 'verrouillé'), ('nv', 'non verrouillé')],
                             track_visibility='onchange')

    state_id = fields.Many2one('ctm.vehicle.state', string="Vehicule", track_visibility='onchange')
    vehicle_model_id = fields.Many2one('fleet.vehicle.model', store=True, compute=get_vehicle_model,
                                       track_visibility='onchange')
    rubrique = fields.Many2one('ctm.intervention.rubrique', string="rubrique de l'intervention",
                               track_visibility='onchange')
    lo = fields.Boolean('Location ?', store=True, compute=get_lo, track_visibility='onchange')
    personnel = fields.Boolean('Personnel ?', store=True, compute=get_personnel, track_visibility='onchange')
    dat = fields.Date('Date', track_visibility='onchange')
    intervention = fields.Text('Intervention', track_visibility='onchange')
    km = fields.Float('KM', digits=(10, 0), track_visibility='onchange')
    Fournisseur = fields.Char('Fournisseur', track_visibility='onchange')
    refbtc = fields.Char('Num bon de commande', track_visibility='onchange')
    cost = fields.Float("Cout d'intervention /DT", track_visibility='onchange')

    @api.constrains('dat')
    def control_date(self):
        if self.dat > datetime.today().date():
            raise UserWarning('You cant enter a date that is supperior of today')


class InterventionRubrique(models.Model):
    _name = "ctm.intervention.rubrique"

    name = fields.Char('Nom', track_visibility='onchange')


class VehicleType(models.Model):
    _name = "ctm.vehicle.type"

    name = fields.Char('Name', track_visibility='onchange')


class FleetVehicleInherit(models.Model):
    _inherit = 'fleet.vehicle.model'
    _order = 'sequence'
    sequence = fields.Integer('sequence', track_visibility='onchange')
    types = fields.Many2one('ctm.vehicle.type', string="Type de vehicule", track_visibility='onchange')
