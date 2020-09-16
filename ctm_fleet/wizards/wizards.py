# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
import logging

# Get the logger
_logger = logging.getLogger(__name__)


class WizardReturnReports(models.Model):
    _name = 'wizard.print.states'

    report_type = fields.Selection(
        selection=[('erd', 'Etat recapitulatif des depenses'), ('eri', 'Etat recapitulatif des interventions'),
                   ('lv', 'Liste des voitures')],
        string="Type d'etat")
    filter_type = fields.Selection(
        selection=[('tv', 'Type de vehicule'), ('v', 'Vehicule'), ('r', 'Rubrique')], string="Filtre")
    filter_date = fields.Selection(
        selection=[('m', 'Mensuel'), ('a', 'Annuel')], string="Filtre date")
    filter_lo = fields.Selection(
        selection=[('l', 'Location'), ('p', 'Parc CTM'), ('pr', 'Parc personnel')], string="Filtre location")
    months = fields.Selection(
        selection=[('1', 'Janvier'), ('2', 'Fevrier'), ('3', 'Mars'), ('4', 'Avril'), ('5', 'Mai'), ('6', 'Juin'),
                   ('7', 'Juillet'),
                   ('8', 'Aout'), ('9', 'Septembre'), ('10', 'Octobre'), ('11', 'Nouvembre'), ('12', 'Decembre')],
        string="Moi")
    years = fields.Selection(selection=[('2018', 2018), ('2019', 2019), ('2020', 2020), ('2021', 2021),
                                        ('2022', 2022), ('2023', 2023), ('2024', 2024), ('2025', 2025),
                                        ('2026', 2026), ('2027', 2027), ('2028', 2028),
                                        ('2029', 2029), ('2030', 2030), ('2031', 2031), ('2032', 2032)],
                             string="Année")

    def get_report(self):
        datas = self.env['ctm.vehicle.state.detail'].search([('id', '>', 9)]).ids
        records = self.env['ctm.vehicle.state.detail'].search([('id', '>', 9)])
        domain = []
        finallist = []
        lostr = ""
        datestr = ""
        month_name = ""
        # constructing the domain
        # step one : date
        if self.report_type == "erd":

            # init
            kmstart = 0
            kmend = 0
            kmoverall = 0
            entretien = 0
            changepieces = 0
            reparation = 0
            parking = 0
            peage = 0
            carbs = 0
            vulc = 0
            othercharges = 0
            total_charges = 0
            observation = ""

            vehicle_list_dict = []
            prk = 0
            # step three : by single vehicle / by model or by rubrique
            # in vehicles case : this operation is devised into 3 stages :
            # stage one : models
            # stage two : get vehicles with that model
            if self.filter_type == 'tv':
                if self.filter_date == "m":
                    month = self.months
                    datestr = " Mensuel "
                    month_name = _(self.months)
                    if int(self.months) in [1, 3, 5, 7, 8, 10, 12]:
                        dtmax = datetime(datetime.now().year, int(month), 31)
                    if int(self.months) in [4, 6, 9, 11]:
                        dtmax = datetime(datetime.now().year, int(month), 30)
                    if int(self.months) == 2:
                        if datetime.now().year in (2020, 2024, 2028, 2032):
                            dtmax = datetime(datetime.now().year, int(month), 29)
                        else:
                            dtmax = datetime(datetime.now().year, int(month), 28)
                    dtmin = datetime(datetime.now().year, int(month), 1)
                    domain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                elif self.filter_date == "a":
                    datestr = " Annuel "
                    dtmax = datetime(int(self.years), 12, 31)
                    dtmin = datetime(int(self.years), 1, 1)
                    domain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                    # step two : location or parc ctm
                if self.filter_lo == 'l':
                    lostr = " Location "

                    domain.append(('lo', '=', True))
                    domain.append(('personnel', '=', False))
                elif self.filter_lo == 'p':
                    lostr = " (Parc CTM) "
                    domain.append(('lo', '=', False))
                    domain.append(('personnel', '=', False))
                elif self.filter_lo == 'pr':
                    lostr = " Parc Personnel "
                    domain.append(('personnel', '=', True))
                    domain.append(('lo', '=', False))
                vehicles_detail_in_the_right_date_and_loan_state = self.env['ctm.vehicle.state.detail'].search(domain)

                if len(vehicles_detail_in_the_right_date_and_loan_state) > 0:

                    for x in self.env['ctm.vehicle.type'].search([]):
                        vehicles_detail_in_the_right_model = []
                        kmstart = 0
                        kmend = 0
                        kmoverall = 0
                        entretien = 0
                        changepieces = 0
                        reparation = 0
                        parking = 0
                        peage = 0
                        carbs = 0
                        vulc = 0
                        othercharges = 0
                        total_charges = 0
                        observation = ""
                        domain1 = []
                        domain1 = domain
                        domain1.append(('state_id.vehicle.model_id.types.id', '=', x.id))

                        for z in vehicles_detail_in_the_right_date_and_loan_state:
                            if z.state_id.vehicle.model_id.types.id == x.id:
                                vehicles_detail_in_the_right_model.append(z)

                        if len(vehicles_detail_in_the_right_model) > 0:
                            model_with_vehicle_obj = {
                                'model_name': x.name,
                                'sum_values': {},
                            }

                            for y in vehicles_detail_in_the_right_model:
                                kmstart = kmstart + y.kmstart
                                kmend = kmend + y.kmend
                                kmoverall = kmoverall + y.kmoverall
                                entretien = entretien + y.entretien
                                changepieces = round(changepieces + y.changepieces, 3)
                                reparation = reparation + y.reparation
                                parking = parking + y.Parking
                                peage = peage + y.peage
                                carbs = carbs + y.carbs
                                vulc = vulc + y.vulc
                                othercharges = othercharges + y.othercharges
                                total_charges = total_charges + y.total_charges
                            vehicle_obj = {
                                'kmstart': round(kmstart, 3),
                                'kmend': round(kmend, 3),
                                'kmoverall': round(kmoverall, 3),
                                'entretien': round(entretien, 3),
                                'changepieces': round(changepieces, 3),
                                'reparation': round(reparation, 3),
                                'parking': round(parking, 3),
                                'peage': round(peage, 3),
                                'carbs': round(carbs, 3),
                                'vulc': round(vulc, 3),
                                'othercharges': round(othercharges, 3),
                                'total_charges': round(total_charges, 3),
                                'observation': observation
                            }
                            model_with_vehicle_obj['sum_values'] = vehicle_obj
                            finallist.append(model_with_vehicle_obj)

                context = dict(self.env.context, active_ids=[datas])
                titlestr = " Etat" + datestr + " des dépenses Par type de vehicule " + lostr
                isyear = False
                isyear = True if self.filter_date == "a" else False
                month_name = _(self.months) if self.filter_date == "m" else self.years
                return {
                    'context': context,
                    'data': {'isyear': isyear, 'month_name': month_name, 'titlestr': titlestr, 'carslist': finallist},
                    'type': 'ir.actions.report',
                    'report_name': 'ctm_fleet.emdtv_report_view',
                    'report_type': 'qweb-pdf',

                    'name': 'Etat des dépenses par Type de vehicule',
                }
            elif self.filter_type == 'v':
                if self.filter_lo == 'l':
                    lostr = " Location "
                    domain = [('lo', '=', True), ('personnel', '=', False)]
                elif self.filter_lo == 'p':
                    lostr = " (Parc CTM) "
                    domain = [('lo', '=', False), ('personnel', '=', False)]
                elif self.filter_lo == 'pr':
                    lostr = " Parc Personnel "
                    domain = [('lo', '=', False), ('personnel', '=', True)]
                if self.filter_date == "m":
                    month = self.months
                    datestr = " Mensuel "
                    month_name = _(self.months)
                    if int(self.months) in [1, 3, 5, 7, 8, 10, 12]:
                        dtmax = datetime(datetime.now().year, int(month), 31)
                    if int(self.months) in [4, 6, 9, 11]:
                        dtmax = datetime(datetime.now().year, int(month), 30)
                    if int(self.months) == 2:
                        if datetime.now().year in (2020, 2024, 2028, 2032):
                            dtmax = datetime(datetime.now().year, int(month), 29)
                        else:
                            dtmax = datetime(datetime.now().year, int(month), 28)

                    dtmin = datetime(datetime.now().year, int(month), 1)
                    dtdomain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                elif self.filter_date == "a":
                    datestr = " Annuel "
                    dtmax = datetime(int(self.years), 12, 31)
                    dtmin = datetime(int(self.years), 1, 1)
                    dtdomain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                vehicles_list = self.env['ctm.vehicle.state'].search(domain)
                for x in self.env['ctm.vehicle.type'].search([]):
                    right_vehicles = []
                    cpt = 0
                    observation = ""
                    for wrz in vehicles_list:
                        if wrz.vehicle.model_id.types.id == x.id:
                            right_vehicles.append(wrz)
                    if len(right_vehicles) > 0:
                        model_with_list_of_vehicles_obj = {
                            'model_name': x.name,
                            'vehicles_list': []
                        }
                        for y in right_vehicles:
                            cpt = cpt + 1

                            kmstart = 0
                            kmend = 0
                            kmoverall = 0
                            entretien = 0
                            changepieces = 0
                            reparation = 0
                            parking = 0
                            peage = 0
                            carbs = 0
                            vulc = 0
                            othercharges = 0
                            total_charges = 0
                            if len(y.statedetail.search(dtdomain)) > 0:
                                for z in y.statedetail.search(dtdomain):
                                    conteur = 0
                                    if z.state_id.id == y.id:
                                        if conteur == 0:
                                            kmstart = z.kmstart
                                        conteur = conteur + 1
                                        kmend = z.kmend
                                        kmoverall = kmoverall + z.kmoverall
                                        entretien = entretien + z.entretien
                                        changepieces = changepieces + z.changepieces
                                        reparation = reparation + z.reparation
                                        parking = parking + z.Parking
                                        peage = peage + z.peage
                                        carbs = carbs + z.carbs
                                        vulc = vulc + z.vulc
                                        othercharges = othercharges + z.othercharges
                                        total_charges = total_charges + z.total_charges
                                vehicle_obj = {
                                    'cpt': cpt,
                                    'matricule': y.vehicle.license_plate,
                                    'kmstart': round(kmstart, 3),
                                    'kmend': round(kmend, 3),
                                    'kmoverall': round(kmoverall, 3),
                                    'entretien': round(entretien, 3),
                                    'changepieces': round(changepieces, 3),
                                    'reparation': round(reparation, 3),
                                    'parking': round(parking, 3),
                                    'peage': round(peage, 3),
                                    'carbs': round(carbs, 3),
                                    'vulc': round(vulc, 3),
                                    'othercharges': round(othercharges, 3),
                                    'total_charges': round(total_charges, 3),
                                    'observation': observation
                                }
                                model_with_list_of_vehicles_obj['vehicles_list'].append(vehicle_obj)
                        if len(model_with_list_of_vehicles_obj['vehicles_list']) > 0:
                            finallist.append(model_with_list_of_vehicles_obj)

                context = dict(self.env.context, active_ids=[datas])
                # return self.env.ref('ctm_fleet.emdv_report').report_action(self, docids=[datas])9+
                titlestr = " Etat" + datestr + " des dépenses Par vehicule " + lostr
                isyear = False
                isyear = True if self.filter_date == "a" else False
                month_name = _(self.months) if self.filter_date == "m" else self.years
                return {
                    'context': context,
                    'data': {'isyear': isyear, 'month_name': month_name, 'titlestr': titlestr, 'carslist': finallist},
                    'type': 'ir.actions.report',
                    'report_name': 'ctm_fleet.emdv_report_view',
                    'report_type': 'qweb-pdf',

                    'name': 'Etat des dépenses par  vehicule',
                }
            elif self.filter_type == 'r':
                if self.filter_lo == 'l':
                    lostr = " Location "
                    domain = [('lo', '=', True), ('personnel', '=', False)]
                elif self.filter_lo == 'p':
                    lostr = " (Parc CTM) "
                    domain = [('lo', '=', False), ('personnel', '=', False)]
                elif self.filter_lo == 'pr':
                    lostr = " Parc Personnel "
                    domain = [('lo', '=', False), ('personnel', '=', True)]
                if self.filter_date == "m":
                    month = self.months
                    datestr = " Mensuel "
                    month_name = _(self.months)
                    if int(self.months) in [1, 3, 5, 7, 8, 10, 12]:
                        dtmax = datetime(datetime.now().year, int(month), 31)
                    if int(self.months) in [4, 6, 9, 11]:
                        dtmax = datetime(datetime.now().year, int(month), 30)
                    if int(self.months) == 2:
                        if datetime.now().year in (2020, 2024, 2028, 2032):
                            dtmax = datetime(datetime.now().year, int(month), 29)
                        else:
                            dtmax = datetime(datetime.now().year, int(month), 28)
                    dtmin = datetime(datetime.now().year, int(month), 1)
                    dtdomain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                elif self.filter_date == "a":
                    datestr = " Annuel "
                    dtmax = datetime(int(self.years), 12, 31)
                    dtmin = datetime(int(self.years), 1, 1)
                    dtdomain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
                vehicles_records = self.env['ctm.vehicle.state'].search(domain)
                rubriques_records = self.env['ctm.intervention.rubrique'].search([])

                if self.filter_lo == 'l':
                    detail_interventions_filtered_by_loan = self.env['ctm.intervention.detail'].search(
                        [('lo', '=', True), ('personnel', '=', False),
                         ('dat', '<=', dtmax.date())])
                elif self.filter_lo == 'p':
                    detail_interventions_filtered_by_loan = self.env[
                        'ctm.intervention.detail'].search(
                        [('lo', '=', False), ('personnel', '=', False),
                         ('dat', '<=', dtmax.date())])
                elif self.filter_lo == 'pr':
                    detail_interventions_filtered_by_loan = self.env['ctm.intervention.detail'].search(
                        [('lo', '=', False), ('personnel', '=', True),
                         ('dat', '<=', dtmax.date())])

                if self.filter_lo == 'l':
                    detail_interventions_filtered_by_all = self.env['ctm.intervention.detail'].search(
                        [('lo', '=', True), ('personnel', '=', False), ('dat', '>=', dtmin),
                         ('dat', '<=', dtmax.date())])
                elif self.filter_lo == 'p':
                    detail_interventions_filtered_by_all = self.env[
                        'ctm.intervention.detail'].search(
                        [('lo', '=', False), ('personnel', '=', False), ('dat', '>=', dtmin), ('dat', '<=', dtmax.date())])
                elif self.filter_lo == 'pr':
                    detail_interventions_filtered_by_all = self.env[
                        'ctm.intervention.detail'].search(
                        [('lo', '=', False), ('personnel', '=', True), ('dat', '>=', dtmin), ('dat', '<=', dtmax.date())])

                finallist = []
                for x in vehicles_records:
                    list_rub = []
                    sum_prk = 0
                    prk = 0
                    sukm = 0
                    summkm = 0
                    if len(x.intervention_detail) > 0:
                        for y in rubriques_records:
                            sum_cumul = 0
                            sum_month = 0

                            if len(detail_interventions_filtered_by_loan.search([('state_id.id', '=', x.id)])) > 0:
                                for z in detail_interventions_filtered_by_loan.search([('state_id', '=', x.id)]):
                                    if x.id == z.state_id.id and z.rubrique.id == y.id:
                                        sum_cumul = sum_cumul + z.cost
                                for w in detail_interventions_filtered_by_all.search([('state_id.id', '=', x.id)]):
                                    if x.id == w.state_id.id and w.rubrique.id == y.id:
                                        sum_month = sum_month + w.cost
                                        sum_prk = round(sum_prk + w.cost, 3)

                                rub_obj = {
                                    'rub_name': y.name,
                                    'somme_obj': {
                                        'somme_moi': round(sum_month, 3),
                                        'cumul': round(sum_cumul, 3)
                                    }
                                }
                                list_rub.append(rub_obj)
                        if self.filter_lo == "p":
                            for kw in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('dat', '>=', dtmin),
                                     ('dat', '<=', dtmax.date())]):
                                summkm = summkm + kw.kmoverall
                            for wk in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('dat', '<=', dtmax.date())]):
                                sukm = sukm + wk.kmoverall
                        elif self.filter_lo == "l":
                            for kw in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', True), ('dat', '>=', dtmin),
                                     ('dat', '<=', dtmax.date())]):
                                summkm = summkm + kw.kmoverall
                            for wk in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', True), ('dat', '<=', dtmax.date())]):
                                sukm = sukm + wk.kmoverall
                        prk = round(sum_prk / summkm, 3) if summkm > 0 else 0
                        if len(list_rub) > 0:
                            vehicle_obj = {
                                'matriule': x.vehicle.license_plate,
                                'parc': summkm,
                                'cumulparc': sukm,
                                'prk': round(prk, 3),
                                'list_rub': list_rub
                            }
                            finallist.append(vehicle_obj)
                    else:
                        if self.filter_lo == "p":
                            for kw in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('personnel', '=', False), ('dat', '>=', dtmin),
                                     ('dat', '<=', dtmax.date())]):
                                summkm = summkm + kw.kmoverall
                            for wk in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('personnel', '=', False), ('dat', '<=', dtmax.date())]):
                                sukm = sukm + wk.kmoverall
                        elif self.filter_lo == "l":
                            for kw in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', True), ('personnel', '=', False), ('dat', '>=', dtmin),
                                     ('dat', '<=', dtmax.date())]):
                                summkm = summkm + kw.kmoverall
                            for wk in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', True), ('personnel', '=', False), ('dat', '<=', dtmax.date())]):
                                sukm = sukm + wk.kmoverall
                        elif self.filter_lo == "pr":
                            for kw in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('personnel', '=', True), ('dat', '>=', dtmin),
                                     ('dat', '<=', dtmax.date())]):
                                summkm = summkm + kw.kmoverall
                            for wk in self.env['ctm.vehicle.state.detail'].search(
                                    [('state_id', '=', x.id), ('lo', '=', False), ('personnel', '=', True), ('dat', '<=', dtmax.date())]):
                                sukm = sukm + wk.kmoverall
                        for i in rubriques_records:
                            rub_obj = {
                                'rub_name': i.name,
                                'somme_obj': {
                                    'somme_moi': 0,
                                    'cumul': 0
                                }
                            }
                            list_rub.append(rub_obj)
                        vehicle_obj = {
                            'matriule': x.vehicle.license_plate,
                            'parc': summkm,
                            'cumulparc': sukm,
                            'prk': round(prk, 3),
                            'list_rub': list_rub
                        }
                        finallist.append(vehicle_obj)

                context = dict(self.env.context, active_ids=[datas])
                # return self.env.ref('ctm_fleet.emdv_report').report_action(self, docids=[datas])9+
                titlestr = " Etat" + datestr + " des dépenses Par Rubrique " + lostr
                isyear = False
                isyear = True if self.filter_date == "a" else False
                month_name = _(self.months) if self.filter_date == "m" else self.years
                rl = []
                for m in rubriques_records:
                    rl.append({
                        'name': m.name,
                    })

                return {
                    'context': context,
                    'data': {'isyear': isyear, 'month_name': month_name, 'titlestr': titlestr, 'carslist': finallist,
                             'rub_list': rl},
                    'type': 'ir.actions.report',
                    'report_name': 'ctm_fleet.edir_report_view',
                    'report_type': 'qweb-pdf',
                    'name': 'Etat des intervention par rubrique',
                }
        elif self.report_type == "eri":

            if self.filter_date == "m":
                month = self.months
                datestr = " Mensuel "
                month_name = _(self.months)
                if int(self.months) in [1, 3, 5, 7, 8, 10, 12]:
                    dtmax = datetime(datetime.now().year, int(month), 31)
                if int(self.months) in [4, 6, 9, 11]:
                    dtmax = datetime(datetime.now().year, int(month), 30)
                if int(self.months) == 2:
                    if datetime.now().year in (2020, 2024, 2028, 2032):
                        dtmax = datetime(datetime.now().year, int(month), 29)
                    else:
                        dtmax = datetime(datetime.now().year, int(month), 28)
                dtmin = datetime(datetime.now().year, int(month), 1)
                domain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
            elif self.filter_date == "a":
                datestr = " Annuel "
                dtmax = datetime(int(self.years), 12, 31)
                dtmin = datetime(int(self.years), 1, 1)
                domain = [('dat', '>=', dtmin), ('dat', '<=', dtmax.date())]
            # step two : location or parc ctm
            if self.filter_lo == 'l':
                lostr = " Location "
                domain.append(('lo', '=', True))
                domain.append(('personnel', '=', False))
            elif self.filter_lo == 'p':
                lostr = " (Parc CTM) "
                domain.append(('personnel', '=', False))
                domain.append(('lo', '=', False))
            elif self.filter_lo == 'pr':
                lostr = " Parc Personnel "
                domain.append(('personnel', '=', True))
                domain.append(('lo', '=', False))
            intervention_records = self.env['ctm.intervention.detail'].search(domain)
            if len(intervention_records) > 1:
                for x in intervention_records:
                    finallist.append({
                        'date': x.dat,
                        'immatriculation': x.state_id.vehicle.license_plate,
                        'KM': x.km,
                        'intervention': x.intervention,
                        'Fournisseur': x.Fournisseur,
                        'refbtc': x.refbtc,
                        "cost": x.cost

                    })
                context = dict(self.env.context, active_ids=[datas])
                # return self.env.ref('ctm_fleet.emdv_report').report_action(self, docids=[datas])9+
                titlestr = " Etat" + datestr + " des Interventions " + lostr
                isyear = False
                isyear = True if self.filter_date == "a" else False
                month_name = _(self.months) if self.filter_date == "m" else self.years
                return {
                    'context': context,
                    'data': {'isyear': isyear, 'month_name': month_name, 'titlestr': titlestr, 'carslist': finallist},
                    'type': 'ir.actions.report',
                    'report_name': 'ctm_fleet.ermi_report_view',
                    'report_type': 'qweb-pdf',
                    'name': 'Etat des Interventions',
                }
        elif self.report_type == "lv":
            lostring = ""
            if self.filter_lo == "l":
                v = self.env["fleet.vehicle"].search([('lo', '=', True), ('personnel', '=', False)])
                lostring = " (Location)"
            elif self.filter_lo == "p":
                v = self.env["fleet.vehicle"].search([('lo', '=', False), ('personnel', '=', False)])
                lostring = " (Parc CTM) "
            elif self.filter_lo == "pr":
                v = self.env["fleet.vehicle"].search([('lo', '=', False), ('personnel', '=', True)])
                lostring = " (Parc Personnel) "
            for x in v:
                try:
                    finallist.append({
                        'agence': x.tag_ids[0].name,
                        'type': x.model_id.types.name,
                        'model': x.model_id.brand_id.name,
                        'lp': x.license_plate
                    })
                except:
                    finallist.append({
                        'agence': '',
                        'type': x.model_id.types.name,
                        'model': x.model_id.brand_id.name,
                        'lp': x.license_plate
                    })
            context = dict(self.env.context, active_ids=[datas])
            # return self.env.ref('ctm_fleet.emdv_report').report_action(self, docids=[datas])9+
            return {
                'context': context,
                'data': {'f_list': finallist, 'lostring': lostring},
                'type': 'ir.actions.report',
                'report_name': 'ctm_fleet.lv_report_view',
                'report_type': 'qweb-pdf',
                'name': 'Liste des vehicules',
            }
