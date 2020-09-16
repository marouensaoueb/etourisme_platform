# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class VehicleType(models.Model):
    _name = "vehicle.types"
    _rec_name = "name"

    name = fields.Char('Name', required=True)


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    def return_domain(self):
        id = self.env.ref('ctm_tools.job_driver').id
        return [('job_id', '=', id)]

    capacity = fields.Integer('Capacité des personnes', required=True)
    driver_id = fields.Many2one('hr.employee', string="Conducteur", domain=return_domain)


class CountryStatecity(models.Model):
    _name = 'res.country.state.city'
    _rec_name = 'name'

    name = fields.Char('nom', required=True)
    state = fields.Many2one('res.country.state')
    region = fields.Char('Region')


class TransferTiming(models.Model):
    _name = 'fleet.transfer.timing'

    city_from = fields.Many2one('res.country.state.city', 'Ville depart', required=True)
    city_to = fields.Many2one('res.country.state.city', 'Ville arrivé', required=True)
    vehicle_type = fields.Many2one('vehicle.types', string="Type de vehicule", required=True)
    distance = fields.Float('Distance', digits=(10, 4))
    time_travel = fields.Float('Temp')


class FleetvehiCleassignationlog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    driver_id = fields.Many2one('hr.employee', string="Conducteur")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    city = fields.Many2one('res.country.state.city', string='Ville')


class LocalisationAireport(models.Model):
    _name = 'localisation.aireport'
    _rec_name = 'code'
    code = fields.Char('Code')
    name = fields.Char('Full name')
    city = fields.Many2one('res.country.state.city', string='Ville')
    


class TransferTypes(models.Model):
    _name = 'transfer.types'
    _rec_name = 'name'

    name = fields.Char('name')
    individual = fields.Boolean('Solo')
    max = fields.Integer('Max persons')


class TransferTypes(models.Model):
    _name = 'point.type'
    _rec_name = 'name'

    name = fields.Char('name')


class TransferTypes(models.Model):
    _name = 'point.list'
    _rec_name = 'code'

    name = fields.Char('name')
    code = fields.Char('Code')
    typ = fields.Many2one('point.type',string="Point type")
    city = fields.Many2one('res.country.state.city',string='city')


class TransportRequest(models.Model):
    _name = 'transport.request'

    def makedomain(self):
        id = self.env.ref('ctm_tools.industry_field_travel').id
        return [('industry_id', '=', id)]

    def makedomain1(self):
        id = self.env.ref('ctm_tools.industry_field_travel_aireport').id
        return [('industry_id', '=', id)]

    agency = fields.Many2one('res.partner',  domain=makedomain)
    destination = fields.Many2one('res.country.state.city', required=True)
    hotel = fields.Many2one('rooming.hotels', required=True)
    date_transfer = fields.Date('Date')
    pax = fields.Integer('PAX')
    transfer_type = fields.Many2one('transfer.types', string='Transfer type')
    aireport = fields.Many2one('localisation.aireport', string='Aireport')
    flight_number = fields.Char('Flight number')
    nature_de_transfer = fields.Selection(selection=[('d', 'depart'), ('a', 'arrivé')], string="nature de transfer")
    point_from = fields.Many2one('point.list', string="point de depart")
    point_to = fields.Many2one('point.list', string="point d'arrivé")
    time_of_landing = fields.Float("Temp d'arrivé")
    time_departure_hotel = fields.Float("Temp depart de l'hotel")
    time_departure_flight = fields.Float('Temp depart Vol')
    time_arrive = fields.Float("Heure d'arrivé")
    vehicle = fields.Many2one('fleet.vehicle', string="Vehicule")
    reservation_id = fields.Many2one('rooming.list', string="reservation_number")


class WizTransp(models.TransientModel):
    _name = 'transp.wiz'

    get_options = fields.Selection(selection=[('all', 'All reservations'), ('selected', 'Selected reservation'),
                                              ('specific', 'Specific reservation'), ('date', 'By date')])
    reservation_id = fields.Many2one('rooming.list', string="Reservation")
    date_from = fields.Date('date from')
    date_to = fields.Date('Date to')

    @api.multi
    def get_details(self):
        if self.get_options == 'selected':
            active_ids = self.env['rooming.list'].prepare_reservation()
            rec = self.env['rooming.list'].search([('id', 'in', active_ids)])
            raise UserWarning(rec)
        elif self.get_options == 'all':
            recs = self.env['rooming.list'].search([])
            raise UserWarning(recs)
        elif self.get_options == 'specific':
            rec = self.reservation_id
            raise UserWarning(rec)
        elif self.get_options == 'date':
            recsarriv = self.env['rooming.list'].search(
                [('checkin', '>=', self.date_from), ('checkin', '<=', self.date_to)])
            recsdepart = self.env['rooming.list'].search(
                [('checkout', '>=', self.date_from), ('checkout', '<=', self.date_to)])
            raise UserWarning(recsarriv, recsdepart)
        return True


class ExCurs(models.Model):
    _name = 'excurs.circuit'

    name = fields.Char('Nom de circuit')


class PaperworkReport(models.Model):
    _name = 'paperwork.indiv'

    @api.onchange('arrive', 'depart')
    def set_length_days(self):
        if self.arrive and self.depart:
            res = relativedelta(self.depart, self.arrive).days
            self.sej_length = res
    num_reserv = fields.Char('Num reservation')
    instance = fields.Char('Instance')
    code_agence = fields.Char('Code agence')
    code_circ = fields.Char('Code circuit')
    code_hotel = fields.Char('Code hotel')
    name = fields.Char('Nom')
    country = fields.Many2one('res.country', string='Pays')
    pax = fields.Integer('Num PAX')
    sejour_hotel = fields.Many2one('rooming.hotels', 'Hotel de séjour')
    agence = fields.Many2one('res.partner', 'Agence')
    circuit = fields.Many2one('excurs.circuit', string="Circuit")
    repartition = fields.Selection(
        selection=[('s', 'Single'), ('d', 'Double'), ('t', 'Triple'), ('q', 'Quadruple'), ('qu', 'quintuple'),
                   ('sx', 'sixtuplé')], string="Repartition")
    arrive = fields.Datetime('Arrivé')
    depart = fields.Datetime('Depart')
    sej_length = fields.Integer('Durée de séjour', compute=set_length_days)
    # payment_method = fields.Many2one('payment.acquirer', string="Moyen de payement",
    #                                  domain=[('website_published', '=', True)])

# excel modifications


class VehicleCostAdjustement(models.Model):
    _name = "fleet.vehicle.cost"

    partner = fields.Many2one('res.partner', string='Fournisseur')
    num_btc = fields.Char('Num bon de commande')
    Km = fields.Char('KM')

