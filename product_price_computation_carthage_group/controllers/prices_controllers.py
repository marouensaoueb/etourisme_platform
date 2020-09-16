# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import json
from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class MatrixModule(http.Controller):

    # room functions
    @http.route('/hotel', type='http', methods=['post'], auth="user", website=True)
    def hotelpost(self, **kw):
        hootel_id = kw['hotel_selection']
        contract = request.env['contract.contract'].search([('hotel', '=', int(hootel_id))])
        request.session['contract_id'] = contract.id
        company_id = request.session['company_id']
        return request.redirect('/hotel/' + str(hootel_id))

    @http.route('/room/<model("room.prices"):obj1>', type='http', methods=['GET'], auth="user", website=True)
    def room_list(self, obj1, **kw):
        try:
            room_id = obj1.id
            contract_id = request.session['contract_id']
            company_id = request.session['company_id']
            contract = request.env['contract.contract'].search([('id', '=', int(contract_id))])
            room_prices = request.env['room.prices'].search([('id', '=', int(room_id))])
            return request.render(
                'product_price_computation_carthage_group.room_show', {
                    'contract': contract,
                    'page_title': contract.hotel.name, 'company_id': company_id,
                    'room': room_prices,
                }
            )
        except:
            return request.redirect('/home')

    @http.route('/room/del/<model("room.prices"):obj1>', type='http', methods=['GET'], auth="user", website=True)
    def del_room(self, obj1):
        request.env['room.prices'].search([('id', '=', obj1.id)]).unlink()
        contract_id = request.session['contract_id']
        contract = request.env['contract.contract'].search([('id', '=', int(contract_id))])
        return request.redirect('/hotel/' + str(contract.hotel.id))

    @http.route('/room/special_copy', type='http', methods=['POST'], auth="user", website=True)
    def special_copy_controller(self, **kwargs):
        is_copy = False
        source = request.env['room.prices'].search([('id', '=', int(kwargs['source_id']))])
        copy_spos = False
        obj = {}
        room_ids = []
        tmp = 0
        try:
            if kwargs['copy_option'] == 'on':
                copy_spos = True
        except:
            pass
        try:
            if int(kwargs['room_destination_select']) > 0:
                is_copy = True
        except:
            pass
        if is_copy:
            try:
                room_ids = request.httprequest.form.getlist('room_destination_select')
                for x in request.env['room.prices'].search([('id', 'in', room_ids)]):
                    id_dest = x.id
                    for d in x.base_prices:
                        # search for a similar meal and accomodation
                        detail = request.env['room.prices.detail'].search(
                            [('room_prices_id', '=', source.id), ('meal', '=', d.meal.id),
                             ('accomodation', '=', d.accomodation.id)])
                        if len(detail) == 1:
                            for r in detail.room_prices_detail_dates_id:
                                ld = r.copy()
                                ld.update({
                                    'room_prices_detail_id': d.id
                                })
                    for d in x.other_prices:
                        # search for a similar meal and accomodation
                        detail = request.env['room.prices.detail.other'].search(
                            [('room_prices_id', '=', source.id), ('meal', '=', d.meal.id),
                             ('accomodation', '=', d.accomodation.id)])
                        if len(detail) == 1:
                            for r in detail.room_prices_detail_dates_id:
                                ld = r.copy()
                                ld.update({
                                    'room_prices_detail_id': d.id
                                })

            except:
                pass

        contract_id = request.session['contract_id']
        contract = request.env['contract.contract'].search([('id', '=', int(contract_id))])
        return request.redirect('/hotel/' + str(contract.hotel.id))

    @http.route('/hotel/<model("rooming.hotels"):obj>', type='http', methods=['GET'], auth="user", website=True)
    def hotelget(self, obj, **kw):
        try:
            hotel_id = obj.id

            company_id = request.session['company_id']

            contract = request.env['contract.contract'].search([('hotel', '=', int(hotel_id))])
            request.session['contract_id'] = contract.id
            return request.render(
                'product_price_computation_carthage_group.hotel_main', {
                    'contract': contract,
                    'page_title': contract.hotel.name, 'company_id': company_id
                }
            )
        except:
            return request.redirect('/home')

    @http.route('/hotel/room/create', type='http', methods=['GET'], auth="user", website=True)
    def room_create_get(self, **kw):
        try:
            contract_id = request.session['contract_id']
            company_id = request.session['company_id']
            contract = request.env['contract.contract'].search([('id', '=', int(contract_id))])

            return request.render(
                'product_price_computation_carthage_group.room_creation', {
                    'contract': contract,
                    'page_title': 'Create room', 'company_id': company_id
                }
            )
        except:
            return request.redirect('/home')

    @http.route('/hotel/room/create', type='http', methods=['POST'], auth="user", website=True)
    def room_create_post(self, **kw):
        if True:
            contract_id = request.session['contract_id']
            company_id = request.session['company_id']
            contract = request.env['contract.contract'].search([('id', '=', int(contract_id))])
            list_key = kw.keys()
            list_acc = []
            list_meal = []
            currency_id = int(kw['currency_id'])
            is_hostel = False
            create_sale_room = False
            room_infant_included = False
            try:
                if kw['is_hostel_form'] == 'on':
                    is_hostel = True
            except:
                is_hostel = False
            try:
                if kw['create_sale_prices_form'] == 'on':
                    create_sale_room = True
            except:
                is_hostel = False
            try:
                if kw['room_infant_included_check'] == 'on':
                    room_infant_included = True
            except:
                room_infant_included = False
            room = request.env['room.categories'].search([('id', '=', int(kw['room_category_id']))])
            for x in list_key:
                if 'is_acc_form' in x:
                    list_acc.append(x)
                if 'is_meal_form' in x:
                    list_meal.append(x)
            accomodations_id = []
            meals_id = []
            for x in list_acc:
                accomodations_id.append(int(kw[x]))
            for y in list_meal:
                meals_id.append(int(kw[y]))
            obj = {
                'prices_type': 'n',
                'contract_id': contract_id,
                'room': room.id,
                'display_name': room.name,
                'currency_id': currency_id,
                'room_qty': kw['room_qty_form'],
                'room_places': kw['room_places_form'],
                'is_hostel': is_hostel,
                'min': kw['room_min_form'],
                'max': kw['room_max_form'],
                'enf_counted': room_infant_included
            }
            room_record = http.request.env['room.prices'].create(obj)
            room_record.accomodations = accomodations_id
            room_record.meals = meals_id
            room_record.change_url = '/matrix/' + str(contract_id) + '/' + str(room_record.id)
            list_id_base = []
            for li in request.env['accomodations'].search([('is_base', '=', True)]):
                list_id_base.append(li.id)

            for x in accomodations_id:
                for y in meals_id:
                    if x in list_id_base:
                        obj_base = {
                            'room_prices_id': room_record.id,
                            'display_name': room.name,
                            'accomodation': x,
                            'meal': y,
                            'room_prices_detail_dates_id': []
                        }
                        base_price_detail = request.env['room.prices.detail'].create(obj_base)
                    else:
                        obj_other = {
                            'room_prices_id': room_record.id,
                            'display_name': room.name,
                            'accomodation': x,
                            'meal': y,
                            'room_prices_detail_dates_id': []
                        }
                        base_price_detail_other = request.env['room.prices.detail.other'].create(obj_other)
            if create_sale_room:
                obj1 = {
                    'prices_type': 's',
                    'contract_id': contract_id,
                    'room': room.id,
                    'display_name': room.name,
                    'currency_id': contract.currency_id.id,
                    'room_qty': kw['room_qty_form'],
                    'room_places': kw['room_places_form'],
                    'is_hostel': is_hostel,
                    'min': kw['room_min_form'],
                    'max': kw['room_max_form']
                }
                room_record1 = http.request.env['room.prices'].create(obj1)
                room_record1.accomodations = accomodations_id
                room_record1.meals = meals_id
                room_record1.change_url = '/matrix/' + str(contract_id) + '/' + str(room_record1.id)
                list_id_base = []
                for li in request.env['accomodations'].search([('is_base', '=', True)]):
                    list_id_base.append(li.id)

                for x in accomodations_id:
                    for y in meals_id:
                        if x in list_id_base:
                            obj_base = {
                                'room_prices_id': room_record1.id,
                                'display_name': room.name,
                                'accomodation': x,
                                'meal': y,
                                'room_prices_detail_dates_id': []
                            }
                            base_price_detail = request.env['room.prices.detail'].create(obj_base)
                        else:
                            obj_other = {
                                'room_prices_id': room_record1.id,
                                'display_name': room.name,
                                'accomodation': x,
                                'meal': y,
                                'room_prices_detail_dates_id': []
                            }
                            base_price_detail_other = request.env['room.prices.detail.other'].create(obj_other)
            return http.request.redirect('/hotel/' + str(contract.hotel.id))

    @http.route('/room/n2s', type='http', methods=['POST'], auth="user", website=True)
    def n2s_copy(self, **kwargs):
        '''
        this functionnality will copy one or multiple net matrixes and generate new sale matrixes for each one of them and modify it according to some
        special formula
        :param kwargs:
        :return: redirection to the main hotels page
        '''
        a = 2
        return True

    # matrix functions
    @http.route('/matrix/<model("contract.contract"):obj>/<model("room.prices"):obj1>', auth="user", methods=['GET'],
                website=False,
                )
    def main_get(self, obj, obj1, **kw):
        meals = []
        accomodations = []
        other_prices = []
        spos = []
        cell_content = {}
        show_spo_cost = False
        try:
            request.session['age_max'] = request.session['age_max']
            request.session['age_min'] = request.session['age_min']
        except:
            request.session['age_max'] = 0
            request.session['age_min'] = 0
        try:
            show_spo_cost = request.session['show_spo_cost']
        except:
            pass
        try:
            d1 = request.session['d1']
            d2 = request.session['d2']
            d3 = request.session['d3']

        except:
            d3 = datetime.now()
            d1 = datetime.now()
            d2 = d3 + timedelta(days=14)
            request.session['d1'] = d1
            request.session['d2'] = d2
            request.session['d3'] = d3
        for x in obj1.meals:
            meals.append(x)

        def myfunc(e):
            return e.meal.sequence

        def myfunc1(e):
            return e.sequence

        #
        meals.sort(key=myfunc1)
        for y in obj1.accomodations:
            # if y.accomodation not in accomodations:
            accomodations.append(y)
        # for x in obj1.other_prices:
        #     if x.accomodation not in accomodations:
        #         accomodations.append(x.accomodation)
        accomodations.sort(key=myfunc1, reverse=True)
        mm = []
        for x in obj1.base_prices:
            mm.append(x)
        mm.sort(key=myfunc)
        for x in mm:
            details = []
            spos = []
            show_spo = False
            spoobj = {}
            detail = {}
            for y in x.room_prices_detail_dates_id:
                try:
                    if (y.date_from >= d1 and y.date_to <= d2) or (y.date_from <= d1 and y.date_to >= d1) or (
                            y.date_from <= d2 and y.date_to >= d2) or (y.date_from <= d1 and y.date_to >= d2) is True:
                        detail = {
                            'date_from': y.date_from,
                            'date_to': y.date_to,
                            'age_max': y.age_max,
                            'age_min': y.age_min,
                            'prix': y.price,
                            'currency': obj1.currency_id.name,

                            'is_relative': y.is_relative,
                            'model_name': y._name,
                            'period': y.date_range.id,
                            'blocked': y.blocked,
                            'id': y.id
                        }
                        try:
                            if detail['date_from']:
                                details.append(detail)
                        except:
                            pass
                except:
                    if (y.date_from >= d1.date() and y.date_to <= d2.date()) or (
                            y.date_from <= d1.date() and y.date_to >= d1.date()) or (
                            y.date_from <= d2.date() and y.date_to >= d2.date()) or (
                            y.date_from <= d1.date() and y.date_to >= d2.date()) is True:
                        detail = {
                            'date_from': y.date_from,
                            'date_to': y.date_to,
                            'age_max': y.age_max,
                            'age_min': y.age_min,
                            'prix': y.price,
                            'currency': obj1.currency_id.name,

                            'is_relative': y.is_relative,
                            'model_name': y._name,
                            'period': y.date_range.id,
                            'blocked': y.blocked,
                            'id': y.id
                        }
                        try:
                            if detail['date_from']:
                                details.append(detail)
                        except:
                            pass
            try:
                details.sort(key=lambda item: item['date_from'], reverse=False)
            except:
                pass
            for z in x.ac_spos_id:
                try:
                    if z.chekin_from:
                        if z.chekin_from >= d1.date() and z.chekin_to <= d2.date() or z.chekin_from <= d1.date() and z.chekin_to >= d2.date():
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1.date() and z.day_stay_to <= d2.date() or z.day_stay_from <= d1.date() and z.day_stay_to >= d2.date():
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1.date() and z.chekout_to <= d2.date():
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1.date() and z.date_creation_to.date() <= d2.date() or \
                                z.date_creation_from.date() <= d1.date() and z.date_creation_to.date() >= d2.date():
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                except:
                    if z.chekin_from:
                        if z.chekin_from >= d1 and z.chekin_to <= d2 or \
                                z.chekin_from <= d1 and z.chekin_to >= d2:
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1 and z.day_stay_to <= d2 or z.day_stay_from <= d1 and z.day_stay_to >= d2:
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1 and z.chekout_to <= d2:
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1 and z.date_creation_to.date() <= d2 or \
                                z.date_creation_from.date() <= d1 and z.date_creation_to.date() >= d2:
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                if show_spo and show_spo_cost:
                    spoobj = {
                        'name': z.spo_config_id.name_spo,
                        'chekin_from': z.chekin_from,
                        'chekin_to': z.chekin_to,
                        'chekout_from': z.chekout_from,
                        'chekout_to': z.chekout_to,
                        'date_creation_from': z.date_creation_from,
                        'date_creation_to': z.date_creation_to,
                        'day_stay_from': z.day_stay_from,
                        'day_stay_to': z.day_stay_to,
                        'is_relative': z.is_relative,
                        'spo_value': z.spo_value,
                        'id': z.id,
                        'age_from': z.age_from,
                        'age_to': z.age_to,
                        'night_number_from': z.night_number_from,
                        'night_number_to': z.night_number_to,
                        'is_blocked': z.blocked_spo,
                        'spo_type': z.spo_type,
                        'showed_name': z.showed_name,
                        'one_time_payement': z.one_time_payement,
                        'sequence': z.sequence
                    }
                    spos.append(spoobj)

            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'spos': spos,
                'id': x.id,
                'model_name': x._name
            }
            other_prices.append(other_price)
        nn = []
        for x in obj1.other_prices:
            nn.append(x)
        nn.sort(key=myfunc)
        for x in nn:
            details = []
            spos = []
            show_spo = False
            spoobj = {}
            detail = {}
            for y in x.room_prices_detail_dates_id:
                try:
                    if (y.date_from >= d1 and y.date_to <= d2) or (y.date_from <= d1 and y.date_to >= d1) or (
                            y.date_from <= d2 and y.date_to >= d2) or (y.date_from <= d1 and y.date_to >= d2) is True:
                        detail = {
                            'date_from': y.date_from,
                            'date_to': y.date_to,
                            'age_max': y.age_max,
                            'age_min': y.age_min,
                            'prix': y.price,
                            'is_relative': y.is_relative,
                            'currency': obj1.currency_id.name,
                            'id': y.id,
                            'model_name': y._name,
                            'period': y.date_range.id,
                            'blocked': y.blocked
                        }
                except:
                    if (y.date_from >= d1.date() and y.date_to <= d2.date()) or (
                            y.date_from <= d1.date() and y.date_to >= d1.date()) or (
                            y.date_from <= d2.date() and y.date_to >= d2.date()) or (
                            y.date_from <= d1.date() and y.date_to >= d2.date()) is True:
                        detail = {
                            'date_from': y.date_from,
                            'date_to': y.date_to,
                            'age_max': y.age_max,
                            'age_min': y.age_min,
                            'prix': y.price,
                            'is_relative': y.is_relative,
                            'currency': obj1.currency_id.name,
                            'id': y.id,
                            'model_name': y._name,
                            'period': y.date_range.id,
                            'blocked': y.blocked
                        }
                try:
                    if detail['date_from']:
                        details.append(detail)
                except:
                    pass
            for z in x.ac_spos_id:
                try:
                    if z.chekin_from:
                        if z.chekin_from >= d1.date() and z.chekin_to <= d2.date() or z.chekin_from <= d1.date() and z.chekin_to >= d2.date():
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1.date() and z.day_stay_to <= d2.date() or z.day_stay_from <= d1.date() and z.day_stay_to >= d2.date():
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1.date() and z.chekout_to <= d2.date():
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1.date() and z.date_creation_to.date() <= d2.date() or \
                                z.date_creation_from.date() <= d1.date() and z.date_creation_to.date() >= d2.date():
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                except:
                    if z.chekin_from:
                        if z.chekin_from >= d1 and z.chekin_to <= d2 or \
                                z.chekin_from <= d1 and z.chekin_to >= d2:
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1 and z.day_stay_to <= d2 or z.day_stay_from <= d1 and z.day_stay_to >= d2:
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1 and z.chekout_to <= d2:
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1 and z.date_creation_to.date() <= d2 or \
                                z.date_creation_from.date() <= d1 and z.date_creation_to.date() >= d2:
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                if show_spo and show_spo_cost:
                    spoobj = {
                        'name': z.spo_config_id.name_spo,
                        'chekin_from': z.chekin_from,
                        'chekin_to': z.chekin_to,
                        'chekout_from': z.chekout_from,
                        'chekout_to': z.chekout_to,
                        'date_creation_from': z.date_creation_from,
                        'date_creation_to': z.date_creation_to,
                        'day_stay_from': z.day_stay_from,
                        'day_stay_to': z.day_stay_to,
                        'id': z.id,
                        'is_relative': z.is_relative,
                        'spo_value': z.spo_value,
                        'age_from': z.age_from,
                        'age_to': z.age_to,
                        'night_number_from': z.night_number_from,
                        'night_number_to': z.night_number_to,
                        'is_blocked': z.blocked_spo,
                        'spo_type': z.spo_type,
                        'showed_name': z.showed_name,
                        'one_time_payement': z.one_time_payement,
                        'sequence': z.sequence
                    }
                    spos.append(spoobj)
            try:
                details.sort(key=lambda item: item['date_from'], reverse=False)
            except:
                pass
            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'spos': spos,
                'id': x.id,
                'model_name': x._name
            }
            other_prices.append(other_price)
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass
        date_filter = datetime.now() + timedelta(days=14)
        if show_spo_cost:
            show_spo_cost = True

        return http.request.render('product_price_computation_carthage_group.object', {
            'page_title': 'Prices',
            'company_id': company_id,

            'object1': obj,
            'object2': obj1,
            'meals': meals,
            'd1': d1,
            'd2': d2,
            'd3': d3,
            'show_spo_cost': show_spo_cost,
            'accomodations': accomodations,
            'donnee': other_prices
        })

    @http.route('/matrix/<model("contract.contract"):obj>/<model("room.prices"):obj1>', auth="user", methods=['POST'],
                website=False,
                )
    def main_post(self, obj, obj1, **kw):
        meals = []
        accomodations = []
        other_prices = []
        d1 = datetime.strptime(kw['d1'], '%Y-%m-%d').date()
        d2 = datetime.strptime(kw['d2'], '%Y-%m-%d').date()
        try:
            request.session['age_max'] = request.session['age_max']
            request.session['age_min'] = request.session['age_min']
        except:
            request.session['age_max'] = 0
            request.session['age_min'] = 0

        try:
            d3 = datetime.strptime(kw['d3'], '%Y-%m-%dT%H:%M:%S')
        except:
            d3 = datetime.strptime(kw['d3'], '%Y-%m-%dT%H:%M')
        request.session['d1'] = d1
        request.session['d2'] = d2
        request.session['d3'] = d3
        show_spo_cost = False
        cell_content = {}
        try:
            show_spo_cost = kw['show_spo_cost']
            request.session['show_spo_cost'] = show_spo_cost
        except:
            request.session['show_spo_cost'] = show_spo_cost
        for x in obj1.meals:
            meals.append(x)

        def myfunc(e):
            return e.meal.sequence

        def myfunc1(e):
            return e.sequence

        #
        meals.sort(key=myfunc1)
        for y in obj1.base_prices:
            if y.accomodation not in accomodations:
                accomodations.append(y.accomodation)
        for x in obj1.other_prices:
            if x.accomodation not in accomodations:
                accomodations.append(x.accomodation)
        accomodations.sort(key=myfunc1, reverse=True)
        mm = []
        for x in obj1.base_prices:
            mm.append(x)
        mm.sort(key=myfunc)
        nn = []
        for x in obj1.other_prices:
            nn.append(x)
        nn.sort(key=myfunc)
        for x in mm:
            details = []
            spos = []
            show_spo = False
            spoobj = {}
            detail = {}
            for y in x.room_prices_detail_dates_id:

                if (y.date_from >= d1 and y.date_to <= d2) or (y.date_from <= d1 and y.date_to >= d1) or (
                        y.date_from <= d2 and y.date_to >= d2) or (y.date_from <= d1 and y.date_to >= d2):
                    detail = {
                        'date_from': y.date_from,
                        'date_to': y.date_to,
                        'age_max': y.age_max,
                        'age_min': y.age_min,
                        'prix': y.price,
                        'is_relative': y.is_relative,
                        'currency': obj1.currency_id.name,
                        'id': y.id,
                        'model_name': y._name,
                        'period': y.date_range.id,
                        'blocked': y.blocked,

                    }
                    details.append(detail)
            try:
                details.sort(key=lambda item: item['date_from'], reverse=False)
            except:
                pass
            for z in x.ac_spos_id:
                if True:
                    if z.chekin_from:
                        if z.chekin_from >= d1 and z.chekin_to <= d2 or z.chekin_from <= d1 and z.chekin_to >= d2:
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1 and z.day_stay_to <= d2 or z.day_stay_from <= d1 and z.day_stay_to >= d2:
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1 and z.chekout_to <= d2:
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1 and z.date_creation_to.date() <= d2 or \
                                z.date_creation_from.date() <= d1 and z.date_creation_to.date() >= d2:
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                # except:
                #     if z.chekin_from:
                #         if z.chekin_from >= d1.date() and z.chekin_to <= d2.date():
                #             show_spo = True
                #     if z.chekout_from:
                #         if z.chekout_from >= d1.date() and z.chekout_to <= d2.date():
                #             show_spo = True
                #     if z.date_creation_from:
                #         if z.date_creation_from >= d1.date() and z.date_creation_to <= d2.date():
                #             show_spo = True
                #     if z.age_from > 0 or z.night_number_from > 0:
                #         show_spo = True
                if show_spo and show_spo_cost:
                    spoobj = {
                        'name': z.spo_config_id.name_spo,
                        'chekin_from': z.chekin_from,
                        'chekin_to': z.chekin_to,
                        'chekout_from': z.chekout_from,
                        'chekout_to': z.chekout_to,
                        'date_creation_from': z.date_creation_from,
                        'date_creation_to': z.date_creation_to,
                        'day_stay_from': z.day_stay_from,
                        'day_stay_to': z.day_stay_to,
                        'is_relative': z.is_relative,
                        'spo_value': z.spo_value,
                        'id': z.id,
                        'age_from': z.age_from,
                        'age_to': z.age_to,
                        'night_number_from': z.night_number_from,
                        'night_number_to': z.night_number_to,
                        'is_blocked': z.blocked_spo,
                        'spo_type': z.spo_type,
                        'showed_name': z.showed_name,
                        'one_time_payement': z.one_time_payement,
                        'sequence': z.sequence
                    }
                    spos.append(spoobj)
            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'spos': spos,
                'id': x.id,
                'model_name': x._name
            }
            other_prices.append(other_price)
        for x in nn:
            details = []
            spos = []
            show_spo = False
            spoobj = {}
            detail = {}
            for y in x.room_prices_detail_dates_id:
                if (y.date_from >= d1 and y.date_to <= d2) or (y.date_from <= d1 and y.date_to >= d1) or (
                        y.date_from <= d2 and y.date_to >= d2) or (y.date_from <= d1 and y.date_to >= d2):
                    detail = {
                        'date_from': y.date_from,
                        'date_to': y.date_to,
                        'age_max': y.age_max,
                        'age_min': y.age_min,
                        'prix': y.price,
                        'is_relative': y.is_relative,
                        'currency': obj1.currency_id.name,
                        'id': y.id,
                        'model_name': y._name,
                        'period': y.date_range.id,
                        'blocked': y.blocked,

                    }
                    details.append(detail)
            try:
                details.sort(key=lambda item: item['date_from'], reverse=False)
            except:
                pass
            for z in x.ac_spos_id:
                try:
                    if z.chekin_from:
                        if z.chekin_from >= d1 and z.chekin_to <= d2 or z.chekin_from <= d1 and z.chekin_to >= d2:
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1 and z.day_stay_to <= d2 or z.day_stay_from <= d1 and z.day_stay_to >= d2:
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1 and z.chekout_to <= d2:
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from.date() >= d1 and z.date_creation_to.date() <= d2 or \
                                z.date_creation_from.date() <= d1 and z.date_creation_to.date() >= d2:
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                except:
                    if z.chekin_from:
                        if z.chekin_from >= d1 and z.chekin_to <= d2 or z.chekin_from <= d1 and z.chekin_to >= d2:
                            show_spo = True
                    if z.chekout_from:
                        if z.chekout_from >= d1 and z.chekout_to <= d2:
                            show_spo = True
                    if z.day_stay_from:
                        if z.day_stay_from >= d1 and z.day_stay_to <= d2 or z.day_stay_from <= d1 and z.day_stay_to >= d2:
                            show_spo = True
                    if z.date_creation_from:
                        if z.date_creation_from >= d1 and z.date_creation_to <= d2 or \
                                z.date_creation_from <= d1 and z.date_creation_to >= d2:
                            show_spo = True
                    if z.age_from > 0 or z.night_number_from > 0:
                        show_spo = True
                if show_spo and show_spo_cost:
                    spoobj = {
                        'name': z.spo_config_id.name_spo,
                        'chekin_from': z.chekin_from,
                        'chekin_to': z.chekin_to,
                        'chekout_from': z.chekout_from,
                        'chekout_to': z.chekout_to,
                        'date_creation_from': z.date_creation_from,
                        'date_creation_to': z.date_creation_to,
                        'day_stay_from': z.day_stay_from,
                        'day_stay_to': z.day_stay_to,
                        'is_relative': z.is_relative,
                        'spo_value': z.spo_value,
                        'id': z.id,
                        'age_from': z.age_from,
                        'age_to': z.age_to,
                        'night_number_from': z.night_number_from,
                        'night_number_to': z.night_number_to,
                        'is_blocked': z.blocked_spo,
                        'spo_type': z.spo_type,
                        'showed_name': z.showed_name,
                        'one_time_payement': z.one_time_payement,
                        'sequence': z.sequence
                    }
                    spos.append(spoobj)
            company_id = False
            try:
                company_id = request.session['company_id']
            except:
                pass
            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'spos': spos,
                'id': x.id,
                'model_name': x._name,

            }
            other_prices.append(other_price)
            if show_spo_cost:
                show_spo_cost = True

        return http.request.render('product_price_computation_carthage_group.object', {
            'page_title': 'Prices',
            'company_id': company_id,
            'object1': obj,
            'object2': obj1,
            'meals': meals,
            'd1': datetime.strptime(kw['d1'], '%Y-%m-%d'),
            'd2': datetime.strptime(kw['d2'], '%Y-%m-%d'),
            'd3': d3,
            'accomodations': accomodations,
            'donnee': other_prices,
            'show_spo_cost': show_spo_cost
        })

    @http.route('/matrix/edit/<model("contract.contract"):obj>/<model("room.prices"):obj1>', auth="user",
                methods=['POST'],
                website=True,
                )
    def edit_price(self, obj, obj1, **kw):
        model_name = kw['model_name']
        record = http.request.env[model_name].search([('id', '=', kw['id'])])
        is_relative = False
        rec = False

        if str(record.date_from) == kw['date_from_edit'] and str(record.date_to) == kw['date_to_edit']:
            try:
                if kw['is_relative'] == 'on':
                    is_relative = True
            except:
                pass
            try:
                record.update({
                    'date_from': kw['date_from_edit'],
                    'date_to': kw['date_to_edit'],
                    'price': float(kw['price_edit']),
                    'is_relative': is_relative,
                    'age_min': kw['age_min_edit'],
                    'age_max': kw['age_max_edit'],
                })
            except:
                record.update({
                    'date_from': kw['date_from_edit'],
                    'date_to': kw['date_to_edit'],
                    'price': float(kw['price_edit']),
                    'is_relative': is_relative,

                })
            rec = record
        else:
            try:
                if kw['is_relative'] == 'on':
                    is_relative = True
            except:
                pass
            try:
                record.update({
                    'date_from': kw['date_from_edit'],
                    'date_to': kw['date_to_edit'],
                    'price': float(kw['price_edit']),
                    'is_relative': is_relative,
                    'age_min': kw['age_min_edit'],
                    'age_max': kw['age_max_edit'],
                })
            except:
                record.update({
                    'date_from': kw['date_from_edit'],
                    'date_to': kw['date_to_edit'],
                    'price': float(kw['price_edit']),
                    'is_relative': is_relative,

                })
            rec = request.env[model_name].ajout_price(record, record.room_prices_detail_id.id)
            record.unlink()

        return http.request.redirect('/matrix/' + str(obj.id) + '/' + str(obj1.id) + '#' + str(rec.id))

    @http.route('/matrix/blocked_date_rec',
                methods=['GET'],
                website=True,
                auth="user",
                )
    def blocked_price(self, **kw):
        model_name = kw['mn']
        record = http.request.env[model_name].search([('id', '=', int(kw['pr']))])
        record.update({
            'blocked': True
        })
        return http.request.redirect('/matrix/' + str(kw['ctr']) + '/' + str(kw['rm']))

    @http.route('/matrix/unblocked_date_rec',
                methods=['GET'],
                website=True,
                auth="user",
                )
    def unblocked_price(self, **kw):
        model_name = kw['mn']
        record = http.request.env[model_name].search([('id', '=', int(kw['pr']))])
        record.update({
            'blocked': False
        })
        return http.request.redirect('/matrix/' + str(kw['ctr']) + '/' + str(kw['rm']))

    @http.route('/matrix/create_price/<model("contract.contract"):obj>/<model("room.prices"):obj1>', methods=['POST'],
                website=True,
                auth="user",
                )
    def create_price(self, obj, obj1, **kw):
        model_name = kw['model_name']
        date_from = datetime.strptime(kw['date_from_create'], '%Y-%m-%d').date()
        date_to = datetime.strptime(kw['date_to_create'], '%Y-%m-%d').date()
        try:
            request.session['age_max'] = kw['age_max_edit']
        except:
            pass
        try:
            request.session['age_min'] = kw['age_min_edit']
        except:
            pass
        rec = False
        if model_name == 'room.prices.detail':
            model_name_date = 'room.prices.detail.dates'

        else:
            model_name_date = 'room.prices.detail.dates.other'
        base_acc = []
        other_acc = []
        for x in obj1.base_prices:
            if x.accomodation.id not in base_acc:
                base_acc.append(x.accomodation.id)
        for y in obj1.other_prices:
            if y.accomodation.id not in other_acc:
                other_acc.append(y.accomodation.id)
        is_relative = False
        record = False
        try:
            if kw['is_relative'] == 'on':
                is_relative = True
        except:
            pass
        # after the creation , the new dates will spread to the other cells in that line ( meals )
        # if the period doesent exist then we need to create it

        is_new_period = False
        """
    so , the trick is very simple , we have 3 cases to manipulate while creating the records : 
    - first case :  the period that we choose is directly inside an old period :
        we remove the link between the old period and the record , we construct our period 
        plus another two periods ( start of old period to our period minus one day , end of our period
        plus one day to the end of the old period ) 
    - second case : a bit more difficult ; the period that we choose is either start with old period and end 
        before it or it start after its start and end with it , we construct only one new period with the
        difference of time and our period of course 
    - third case , our period is on multiple old periods and eating from anywhere :
        we take the first part ( old period start is before or like our period start )
        the second part wich is the last part (  old period end is after or like our end period)
        we take all the periods that are inside 
        we remove the link with the inside periods , we make 2 new periods like the first case 
        and propagate all changes to the rest of work ( base prices , other prices and the column work  
    """

        if True:
            old_record = http.request.env[model_name].search([('id', '=', kw['id'])])
            # search for the first case
            first_case_ids = []
            for x in old_record.room_prices_detail_dates_id:
                first_case_ids.append(x.id)
            search_zone_second_case = http.request.env[model_name_date].search(
                [('id', 'in', first_case_ids), ('date_from', '>=', kw['date_from_create']),
                 ('age_max', '=', kw['age_max_edit']), ('age_min', '=', kw['age_min_edit']),
                 ('date_to', '<=', kw['date_to_create'])])
            search_zone_second_case_left = http.request.env[model_name_date].search(
                [('id', 'in', first_case_ids), ('date_from', '<', kw['date_from_create']),
                 ('age_max', '=', kw['age_max_edit']), ('age_min', '=', kw['age_min_edit']),
                 ('date_to', '>', kw['date_from_create'])])
            search_zone_second_case_right = http.request.env[model_name_date].search(
                [('id', 'in', first_case_ids), ('date_from', '<', kw['date_to_create']),
                 ('age_max', '=', kw['age_max_edit']), ('age_min', '=', kw['age_min_edit']),
                 ('date_to', '>', kw['date_to_create'])])
            the_new_price_with_new_period = {
                'date_from': date_from,
                'date_to': date_to,
                'price': float(kw['price_edit']),
                'is_relative': is_relative,
                'age_min': kw['age_min_edit'],
                'age_max': kw['age_max_edit'],
                'room_prices_detail_id': kw['id'],
            }
            rec = http.request.env[model_name_date].create(the_new_price_with_new_period)
            if search_zone_second_case_left:
                # first_period_obj = {
                #     'frome': search_zone_second_case_left.date_range.frome,
                #     'to': (new_date_range_record.frome - timedelta(days=1)),
                #     'dn': str(search_zone_second_case_left.date_range.frome) + ' // ' + str(
                #         (new_date_range_record.frome - timedelta(days=1))),
                #     'contract_id': obj.id
                #
                # }
                # first_period_rec = http.request.env['room.prices.date.ranges'].create(first_period_obj)
                first_price_obj = {

                    'date_from': search_zone_second_case_left.date_from,
                    'date_to': date_from - timedelta(days=1),
                    'price': search_zone_second_case_left.price,
                    'is_relative': search_zone_second_case_left.is_relative,
                    'age_min': search_zone_second_case_left.age_min,
                    'age_max': search_zone_second_case_left.age_max,
                    'room_prices_detail_id': kw['id'],
                }
                http.request.env[model_name_date].create(first_price_obj)

            if search_zone_second_case_right:
                # second_period_obj = {
                #     'frome': new_date_range_record.to + timedelta(days=1),
                #     'to': search_zone_second_case_right.date_range.to,
                #     'dn': str((new_date_range_record.to + timedelta(days=1))) + ' // ' + str(
                #         search_zone_second_case_right.date_range.to),
                #     'contract_id': obj.id
                #
                # }
                # second_period_rec = http.request.env['room.prices.date.ranges'].create(second_period_obj)
                second_price_obj = {

                    'date_from': date_to + timedelta(days=1),
                    'date_to': search_zone_second_case_right.date_to,
                    'price': search_zone_second_case_right.price,
                    'is_relative': search_zone_second_case_right.is_relative,
                    'age_min': search_zone_second_case_right.age_min,
                    'age_max': search_zone_second_case_right.age_max,
                    'room_prices_detail_id': kw['id'],
                }
                http.request.env[model_name_date].create(second_price_obj)

            search_zone_second_case_right.unlink()
            search_zone_second_case_left.unlink()
            if len(search_zone_second_case) > 0:
                for x in search_zone_second_case:
                    x.unlink()
        # else:
        #     crobj = {
        #         'date_range': date_range_id,
        #         'price': float(kw['price_edit']),
        #         'is_relative': is_relative,
        #         'age_min': kw['age_min_edit'],
        #         'age_max': kw['age_max_edit'],
        #         'room_prices_detail_id': kw['id'],
        #     }
        #     record = http.request.env[model_name_date].create(crobj)
        # todo : test , if it interfere then devide periods

        return http.request.redirect('/matrix/' + str(obj.id) + '/' + str(obj1.id) + '#' + str(rec.id))

    @http.route('/matrix/final/<model("contract.contract"):obj>/<model("room.prices"):obj1>/', auth="user",
                methods=['GET'],
                website=False,
                )
    def final_matrix_get(self, obj, obj1, **kw):
        meals = []
        accomodations = []
        other_prices = []
        cell_content = {}
        show_spo = False
        try:
            show_spo = kw['show_spo']
            request.session['show_spo'] = show_spo
        except:

            show_spo = False
            request.session['show_spo'] = False
        try:
            d1 = datetime.strptime(kw['d1'], '%Y-%m-%d').date()
            d2 = datetime.strptime(kw['d2'], '%Y-%m-%d').date()

            date_filter = datetime.strptime(kw['d3'], '%Y-%m-%dT%H:%M:%S')
            request.session['final-d1'] = d1
            request.session['final-d2'] = d2

            request.session['final-d3'] = date_filter
        except:
            try:
                d1 = request.session['final-d1']
                d2 = request.session['final-d2']
                date_filter = request.session['final-d3']
            except:
                date_filter = datetime.now()
                d1 = datetime.now()
                d2 = date_filter + timedelta(days=14)

        # in the get , days are always 14 so
        days_to_use = (d2 - d1).days
        for x in obj1.meals:
            if x.code != 'BP':
                meals.append(x)

        def myfunc(e):
            return e.meal.sequence

        def myfunc1(e):
            return e.sequence

        kk = 0
        date_list = [d1 + timedelta(days=kk) for kk in range(0, days_to_use)]

        def get_active_spos(price_detail, date_creation, date_checkin, date_checkout, jour_from, jour_to):
            """

            :param price_detail:
            :param date_creation:
            :param date_checkin:
            :param date_checkout:
            :param age:
            :param jour:
            :return: list of active spos_ids
            """
            checkin_bool = True
            checkout_bool = True
            creation_bool = True
            # age_bool = True
            night_number_bool = True
            day_stay_bool = True
            night_number = (date_checkout - date_checkin).days
            active_spos_ids_daily = []
            active_spos_ids_period = []
            res = []
            list_spo = price_detail.ac_spos_id
            if len(list_spo) > 0:
                for x in list_spo:
                    checkin_bool = True
                    checkout_bool = True
                    creation_bool = True
                    # age_bool = True
                    night_number_bool = True
                    day_stay_bool = True
                    if x.one_time_payement is False:

                        if x.spo_config_id.period_chekin:
                            if date_checkin >= x.chekin_from and date_checkin <= x.chekin_to:
                                checkin_bool = True
                            else:
                                checkin_bool = False

                        if x.spo_config_id.period_chekout:
                            if date_checkout >= x.chekout_from and date_checkout <= x.chekout_to:
                                checkout_bool = True
                            else:
                                checkout_bool = False

                        if x.spo_config_id.period_date_creation:
                            if date_creation >= x.date_creation_from and date_creation <= x.date_creation_to:
                                creation_bool = True
                            else:
                                creation_bool = False

                        # if x.spo_config_id.age:
                        #     if age >= x.age_from and age <= x.age_to:
                        #         age_bool = True
                        #     else:
                        #         age_bool = False

                        if x.spo_config_id.night_number:
                            if night_number >= x.night_number_from and night_number <= x.night_number_to:
                                night_number_bool = True
                            else:
                                night_number_bool = False

                        if x.spo_config_id.date_stay:
                            if jour_from >= x.day_stay_from and jour_to <= x.day_stay_to:
                                day_stay_bool = True
                            else:
                                day_stay_bool = False
                        if checkin_bool and checkout_bool and creation_bool and night_number_bool and day_stay_bool:
                            active_spos_ids_daily.append(x.id)
                    else:
                        if x.spo_config_id.period_chekin:
                            if date_checkin >= x.chekin_from and date_checkin <= x.chekin_to:
                                checkin_bool = True
                            else:
                                checkin_bool = False

                        if x.spo_config_id.period_chekout:
                            if date_checkout >= x.chekout_from and date_checkout <= x.chekout_to:
                                checkout_bool = True
                            else:
                                checkout_bool = False

                        if x.spo_config_id.period_date_creation:
                            if date_creation >= x.date_creation_from and date_creation <= x.date_creation_to:
                                creation_bool = True
                            else:
                                creation_bool = False

                        # if x.spo_config_id.age:
                        #     if age >= x.age_from and age <= x.age_to:
                        #         age_bool = True
                        #     else:
                        #         age_bool = False

                        if x.spo_config_id.night_number:
                            if night_number >= x.night_number_from and night_number <= x.night_number_to:
                                night_number_bool = True
                            else:
                                night_number_bool = False

                        if x.spo_config_id.date_stay:
                            if jour_from >= x.day_stay_from and jour_to <= x.day_stay_to:
                                day_stay_bool = True
                            else:
                                day_stay_bool = False
                        if checkin_bool and checkout_bool and creation_bool and night_number_bool and day_stay_bool:
                            active_spos_ids_period.append(x.id)
                res.append(active_spos_ids_daily)
                res.append(active_spos_ids_period)
            else:
                res.append(active_spos_ids_daily)
                res.append(active_spos_ids_period)

            return res

        def get_nn_cumm_spos(active_spos_list_ids):
            """
                just return a combination of non commulable spos little lists
                to be processed later
            :param active_spos_list_ids:
            :return: list of non commulable spos tuples
            """
            spos_rec = http.request.env['spo.values'].search([('id', 'in', active_spos_list_ids)])
            nnccsl = []
            for x in spos_rec:
                if len(x.not_commulable_with) > 0:
                    tmp = []
                    for y in x.not_commulable_with:
                        if y.id not in tmp and y.id in active_spos_list_ids:
                            tmp.append(y.id)
                    tmp.append(x.id)
                    nnccsl.append(tmp)
            return nnccsl

        def get_spos_groups(active_spos_list_ids, nn_comm_spos_tuple_ids):
            """
                if we dont have the case of the non commulability
                just return a normal liste of active spos
            :param nn_comm_spos_tuple_ids:
            :param active_spos_list_ids:
            :return: list of spos groups
            """
            if len(nn_comm_spos_tuple_ids) > 0:
                spos = []
                combo = []
                res = []
                for m in nn_comm_spos_tuple_ids:
                    for x in m:
                        for y in active_spos_list_ids:
                            if y not in m:
                                spos.append(y)

                        combo = []
                        combo = spos
                        combo.append(x)
                        spos = []
                        res.append(combo)
            else:
                res = []
                res.append(active_spos_list_ids)
            if len(active_spos_list_ids) > 0:
                return res
            else:
                return []

        def calculate_spos(ordinary_price, spos_groups_ids):
            """

            :param ordinary_price:
            :param spos_groups_ids:
            :return: the least price calculated from spo groups
            """
            min = 9999999999999999999
            if len(spos_groups_ids) > 0:
                for x in spos_groups_ids:
                    spos = http.request.env['spo.values'].search([('id', 'in', x)], order="sequence Asc")
                    tmp = 0
                    for y in spos:
                        tmp = 0
                        if y.spo_type == 'moins':
                            if y.is_relative:
                                tmp = ordinary_price - ((ordinary_price / 100) * y.spo_value)
                            else:
                                tmp = ordinary_price - y.spo_value
                        else:
                            if y.is_relative:
                                tmp = ordinary_price + ((ordinary_price / 100) * y.spo_value)
                            else:
                                tmp = ordinary_price + y.spo_value
                    if tmp < min:
                        min = tmp
                return min
            else:
                return ordinary_price

        def calculate_single_accomodation(room_price_detail, acc, meal, date_list, age_min=None, age_max=None):
            # TODO insert spo calculation in each day and after
            sum = 0

            if age_min is None and age_max is None:
                for jour in date_list:
                    tmp = 0
                    tm1 = 0
                    base_val = 0
                    base_meal_id = request.env['room.meal'].search([('code', '=', 'BP')]).id
                    base_acc_id = request.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_dbl')
                    if acc.is_base:
                        # get the base price
                        base_price_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if acc.code == 'SGL' and base_prices_date_record.is_relative is True:
                            base_price_record = request.env['room.prices.detail'].search(
                                [('meal.id', '=', base_meal_id), ('accomodation.id', '=', base_acc_id),
                                 ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                                 ])
                            base_prices_date_record = request.env['room.prices.detail.dates'].search(
                                [('room_prices_detail_id', '=', base_price_record.id),
                                 ('date_from', '<=', jour), ('date_to', '>=', jour)])
                            tm1 = tm1 + base_prices_date_record.price
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        # todo insert spo on base modifications here
                        if show_spo:
                            active_spos = get_active_spos(base_price_record, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                        else:
                            base_val = tm1
                        # get the meal price
                        base_price_acc_meal_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        price_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if show_spo:
                            active_spos = get_active_spos(room_price_detail, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                        else:
                            sum = sum + tmp + base_val

                    else:
                        # prepare the dbl on [base price ] accomodatino price
                        base_price_acc_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # prepare the dbl on [base price ] accomodatino price
                        base_price_acc_meal_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # get the base price
                        base_price_record = request.env['room.prices.detail.other'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = request.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if base_prices_date_record.is_relative:
                            tm1 = tm1 + ((base_prices_acc_date_record.price / 100) * base_prices_date_record.price)
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if show_spo:
                            active_spos = get_active_spos(base_price_record, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                        else:
                            base_val = tm1
                        # get the meal price
                        price_record = request.env['room.prices.detail.other'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = request.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/nigh spo here
                        if show_spo:
                            active_spos = get_active_spos(room_price_detail, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                        else:
                            sum = sum + tmp + base_val
            else:
                for jour in date_list:
                    tmp = 0
                    tm1 = 0
                    base_val = 0
                    base_meal_id = request.env['room.meal'].search([('code', '=', 'BP')]).id
                    base_acc_id = request.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_dbl')
                    if acc.is_base:
                        # get the base price
                        base_price_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '=', age_min),
                             ('age_max', '=', age_max)])
                        if acc.code == 'SGL' and base_prices_date_record.is_relative is True:
                            base_price_record = request.env['room.prices.detail'].search(
                                [('meal.id', '=', base_meal_id), ('accomodation.id', '=', base_acc_id),
                                 ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                                 ])
                            base_prices_date_record = request.env['room.prices.detail.dates'].search(
                                [('room_prices_detail_id', '=', base_price_record.id),
                                 ('date_from', '<=', jour), ('date_to', '>=', jour),
                                 ('age_min', '=', age_min),
                                 ('age_max', '=', age_max)])
                            tm1 = tm1 + base_prices_date_record.price
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if show_spo:
                            active_spos = get_active_spos(base_price_record, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                        else:
                            base_val = tm1
                        # get the meal price
                        base_price_acc_meal_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        price_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '=', age_min),
                             ('age_max', '=', age_max)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if show_spo:
                            active_spos = get_active_spos(room_price_detail, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                        else:
                            sum = sum + tmp + base_val
                    else:
                        # prepare the dbl on [base price ] accomodatino price
                        base_price_acc_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        base_price_acc_meal_record = request.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = request.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # get the base price
                        base_price_record = request.env['room.prices.detail.other'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = request.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '=', age_min),
                             ('age_max', '=', age_max)])
                        if base_prices_date_record.is_relative:
                            tm1 = tm1 + ((base_prices_acc_date_record.price / 100) * base_prices_date_record.price)
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if show_spo:
                            active_spos = get_active_spos(base_price_record, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                        else:
                            base_val = tm1
                        # get the meal price
                        price_record = request.env['room.prices.detail.other'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = request.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '=', age_min),
                             ('age_max', '=', age_max)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if show_spo:
                            active_spos = get_active_spos(room_price_detail, date_filter, d1, d2, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                        else:
                            sum = sum + tmp + base_val
            # todo find a way to apply acc/period spo here
            if show_spo:
                active_spos = get_active_spos(room_price_detail, date_filter, d1, d2, d1, d2)
                nnccssppss = get_nn_cumm_spos(active_spos[1])
                sppgroups = get_spos_groups(active_spos[1], nnccssppss)
                sum = calculate_spos(sum, sppgroups)

            return sum

        meals.sort(key=myfunc1)
        for y in obj1.accomodations:
            # if y.accomodation not in accomodations:
            accomodations.append(y)
        accomodations.sort(key=myfunc1, reverse=True)
        mm = []
        for x in obj1.base_prices:
            if x.meal.code != 'BP':
                mm.append(x)
        mm.sort(key=myfunc)
        for x in mm:
            details = []
            price = 0
            tmp = x.accomodation
            age_ranges = []
            objages = {}
            ff = request.env['room.prices.detail.dates'].search([('room_prices_detail_id', '=', x.id)])
            for y in ff:
                objages = {
                    'age_min': y.age_min,
                    'age_max': y.age_max
                }
                if len(age_ranges) == 0:
                    age_ranges.append(objages)
                else:
                    for sdjifgh in age_ranges:

                        if sdjifgh['age_min'] == objages['age_min'] and sdjifgh['age_max'] == objages['age_max']:
                            pass
                        else:
                            age_ranges.append(objages)
            for ric in age_ranges:
                tmp = x.accomodation
                price = 0
                if tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_2_dbl'):
                    price = (price + calculate_single_accomodation(x, tmp, x.meal, date_list)) * 2
                else:
                    while tmp:
                        dbltmp = http.request.env['accomodations'].search([('id', '=', request.env[
                            'ir.model.data'].xmlid_to_res_id(
                            'product_price_computation_carthage_group.accomodation_dbl'))])
                        if tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                                'product_price_computation_carthage_group.accomodation_2_dbl'):
                            price = price + calculate_single_accomodation(x, dbltmp, x.meal, date_list)
                        elif tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                                'product_price_computation_carthage_group.accomodation_dbl'):
                            price = (price + calculate_single_accomodation(x, dbltmp, x.meal, date_list)) * 2
                        else:
                            price = price + calculate_single_accomodation(x, tmp, x.meal, date_list, ric['age_min'],
                                                                          ric['age_max'])
                        tmp = tmp.parent_id
                det = {
                    'price': round(price, 3),
                    'age_range': ric,
                }
                details.append(det)
            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'id': x.id,
                'model_name': x._name
            }
            other_prices.append(other_price)
        # compute the final prices for the given dates
        # take the base price , + supplements ( relative or absolute ) and compute it

        nn = []
        for x in obj1.other_prices:
            if x.meal.code != 'BP':
                nn.append(x)
        nn.sort(key=myfunc)
        for x in nn:
            details = []
            price = 0
            tmp = x.accomodation
            ff = request.env['room.prices.detail.dates.other'].search([('room_prices_detail_id', '=', x.id)])
            age_ranges = []
            objages = {}
            for y in ff:
                objages = {
                    'age_min': y.age_min,
                    'age_max': y.age_max
                }
                if len(age_ranges) == 0:
                    age_ranges.append(objages)
                else:
                    for sdjifgh in age_ranges:
                        if sdjifgh['age_min'] == objages['age_min'] and sdjifgh['age_max'] == objages['age_max']:
                            pass
                        else:
                            age_ranges.append(objages)
            for ric in age_ranges:
                tmp = x.accomodation
                price = 0
                while tmp:
                    dbltmp = http.request.env['accomodations'].search([('id', '=',
                                                                        request.env['ir.model.data'].xmlid_to_res_id(
                                                                            'product_price_computation_carthage_group.accomodation_dbl'))])
                    sgltmp = http.request.env['accomodations'].search([('id', '=', http.request.env[
                        'ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_sgl'))])
                    if tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                            'product_price_computation_carthage_group.accomodation_2_dbl'):
                        price = price + calculate_single_accomodation(x, dbltmp, x.meal, date_list, )
                    elif tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                            'product_price_computation_carthage_group.accomodation_dbl'):
                        price = price + calculate_single_accomodation(x, dbltmp, x.meal, date_list, )
                    elif tmp.id == http.request.env['ir.model.data'].xmlid_to_res_id(
                            'product_price_computation_carthage_group.accomodation_sgl'):
                        price = price + calculate_single_accomodation(x, sgltmp, x.meal, date_list, )
                    else:
                        price = price + calculate_single_accomodation(x, tmp, x.meal, date_list, ric['age_min'],
                                                                      ric['age_max'])
                    tmp = tmp.parent_id
                det = {
                    'price': round(price, 3),
                    'age_range': ric,
                }
                details.append(det)
            other_price = {
                'meal': x.meal.name,
                'accomodation': x.accomodation.code,
                'content': details,
                'id': x.id,
                'model_name': x._name
            }
            other_prices.append(other_price)
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass
        if show_spo:
            show_spo = True
        available_rooms_select = []
        for rr in obj.room_prices:
            available_rooms_select.append({'room_name': rr.room.name, 'id': rr.id, 'price_type': _(rr.prices_type)})

        return http.request.render('product_price_computation_carthage_group.final_matrix', {
            'page_title': 'Final prices ' + obj1.room.name,
            'company_id': company_id,
            'available_rooms_select': available_rooms_select,
            'object1': obj,
            'object2': obj1,
            'meals': meals,
            'd1': d1,
            'd2': d2,
            'd3': date_filter,
            'show_spo': show_spo,
            'accomodations': accomodations,
            'donnee': other_prices
        })

    @http.route('/matrix/copy_price', methods=['GET'],
                website=True,
                auth="none",
                type='http'
                )
    def copy_price(self, **kw):
        model_name_copy = kw['model_name_copy']
        id_copy = int(kw['id_copy'])
        id_paste = int(kw['id_paste'])
        model_name_paste = kw['model_name_paste']
        if model_name_copy == 'room.prices.detail':
            model_name_date_copy = 'room.prices.detail.dates'

        else:
            model_name_date_copy = 'room.prices.detail.dates.other'
        if model_name_paste == 'room.prices.detail':
            model_name_date_paste = 'room.prices.detail.dates'

        else:
            model_name_date_paste = 'room.prices.detail.dates.other'

        # after the creation , the new dates will spread to the other cells in that line ( meals )
        # if the period doesent exist then we need to create it

        old_record = http.request.env[model_name_date_copy].search([('id', '=', id_copy)])
        destination_div = http.request.env[model_name_paste].search([('id', '=', id_paste)])

        # old_record = http.request.env[model_name_copy].search([('id', '=', kw['id'])])
        # search for the first case
        first_case_ids = []
        for x in destination_div.room_prices_detail_dates_id:
            first_case_ids.append(x.id)
        search_zone_second_case = http.request.env[model_name_date_paste].search(
            [('id', 'in', first_case_ids), ('date_from', '>=', old_record.date_from),
             ('age_max', '=', old_record.age_max), ('age_min', '=', old_record.age_min),
             ('date_to', '<=', old_record.date_to)])
        search_zone_second_case_left = http.request.env[model_name_date_paste].search(
            [('id', 'in', first_case_ids), ('date_from', '<', old_record.date_from),
             ('age_max', '=', old_record.age_max), ('age_min', '=', old_record.age_min),
             ('date_to', '>', old_record.date_from)])
        search_zone_second_case_right = http.request.env[model_name_date_paste].search(
            [('id', 'in', first_case_ids), ('date_from', '<', old_record.date_to),
             ('age_max', '=', old_record.age_max), ('age_min', '=', old_record.age_min),
             ('date_to', '>', old_record.date_to)])
        obj_new_record = {
            'room_prices_detail_id': id_paste,
            'display_name': old_record.display_name,
            'date_from': old_record.date_from,
            'date_to': old_record.date_to,
            'price': old_record.price,
            'is_relative': old_record.is_relative,
            'age_min': old_record.age_min,
            'age_max': old_record.age_max

        }
        new_record = http.request.env[model_name_date_paste].create(obj_new_record)
        if search_zone_second_case_left:
            # first_period_obj = {
            #     'frome': search_zone_second_case_left.date_range.frome,
            #     'to': (new_date_range_record.frome - timedelta(days=1)),
            #     'dn': str(search_zone_second_case_left.date_range.frome) + ' // ' + str(
            #         (new_date_range_record.frome - timedelta(days=1))),
            #     'contract_id': obj.id
            #
            # }
            # first_period_rec = http.request.env['room.prices.date.ranges'].create(first_period_obj)
            first_price_obj = {

                'date_from': search_zone_second_case_left.date_from,
                'date_to': old_record.date_from - timedelta(days=1),
                'price': search_zone_second_case_left.price,
                'is_relative': search_zone_second_case_left.is_relative,
                'age_min': search_zone_second_case_left.age_min,
                'age_max': search_zone_second_case_left.age_max,
                'room_prices_detail_id': id_paste,
            }
            http.request.env[model_name_date_paste].create(first_price_obj)

        if search_zone_second_case_right:
            # second_period_obj = {
            #     'frome': new_date_range_record.to + timedelta(days=1),
            #     'to': search_zone_second_case_right.date_range.to,
            #     'dn': str((new_date_range_record.to + timedelta(days=1))) + ' // ' + str(
            #         search_zone_second_case_right.date_range.to),
            #     'contract_id': obj.id
            #
            # }
            # second_period_rec = http.request.env['room.prices.date.ranges'].create(second_period_obj)
            second_price_obj = {

                'date_from': old_record.date_to + timedelta(days=1),
                'date_to': search_zone_second_case_right.date_to,
                'price': search_zone_second_case_right.price,
                'is_relative': search_zone_second_case_right.is_relative,
                'age_min': search_zone_second_case_right.age_min,
                'age_max': search_zone_second_case_right.age_max,
                'room_prices_detail_id': id_paste,
            }
            http.request.env[model_name_date_paste].create(second_price_obj)

        search_zone_second_case_right.unlink()
        search_zone_second_case_left.unlink()
        if len(search_zone_second_case) > 0:
            for x in search_zone_second_case:
                x.unlink()

        # todo : test , if it interfere then devide periods

    @http.route('/matrix/copy_price_masse', methods=['GET'],
                website=True,
                auth="none",
                type='http'
                )
    def copymasse_price(self, **kw):

        if kw['model_name_copy'] == 'room.prices.detail':
            name_copy = 'room.prices.detail.dates'
        else:
            name_copy = 'room.prices.detail.dates.other'
        if kw['model_name_paste'] == 'room.prices.detail':
            name_paste = 'room.prices.detail.dates'
        else:
            name_paste = 'room.prices.detail.dates.other'
        search_resultat = request.env[name_copy].search(
            [('room_prices_detail_id', '=', int(kw['id_copy']))])

        for record in search_resultat:
            request.env[name_paste].ajout_price(record, int(kw['id_paste']))

    @http.route('/matrix/create_spo/<model("contract.contract"):obj>/<model("room.prices"):obj1>', methods=['POST'],
                website=True,
                auth="user",
                )
    def create_spo(self, obj, obj1, **kw):
        modal_name = kw['model_name']
        spo_select_config = kw['period_edit_select']
        spo_select_type = kw['spo_type_id']
        spo_config = http.request.env['spo.configuration'].search([('id', '=', int(spo_select_config))])
        is_relative_value = False
        one_time_payment = False
        tmp = spo_config.name_spo + ' '
        try:
            if kw['one_type_payment'] == 'on':
                one_time_payment = True
        except:
            one_time_payment = False
        try:
            sequence = kw['priority_create']
        except:
            sequence = None

        try:
            date_chekin_from = datetime.strptime(kw['checkin_from_create'], '%Y-%m-%d').date()
            date_chekin_to = datetime.strptime(kw['checkin_to_create'], '%Y-%m-%d').date()
            tmp = tmp + 'chIN: ' + datetime.strftime(date_chekin_from, '%m.%d.%y')
            tmp = tmp + ' '
        except:
            date_chekin_from = None
            date_chekin_to = None
        try:
            date_chekout_from = datetime.strptime(kw['checkout_from_create'], '%Y-%m-%d').date()
            date_chekout_to = datetime.strptime(kw['checkout_to_create'], '%Y-%m-%d').date()
            tmp = tmp + 'chOUT: ' + datetime.strftime(date_chekout_from, '%m.%d.%y')
            tmp = tmp + ' '
        except:
            date_chekout_from = None
            date_chekout_to = None
        try:
            date_creation_from = datetime.strptime(kw['creation_from_create'], '%Y-%m-%dT%H:%M')
            date_creation_to = datetime.strptime(kw['creation_to_create'], '%Y-%m-%dT%H:%M')
            tmp = tmp + 'cr: ' + datetime.strftime(date_creation_from, '%m.%d.%yT%H:%M')
            tmp = tmp + ' '
        except:
            date_creation_from = None
            date_creation_to = None
        try:
            date_stay_from = datetime.strptime(kw['stay_from_create'], '%Y-%m-%d').date()
            date_stay_to = datetime.strptime(kw['stay_to_create'], '%Y-%m-%d').date()
            tmp = tmp + 'pr: ' + datetime.strftime(date_stay_from, '%m.%d.%y')
            tmp = tmp + ' '
        except:
            date_stay_from = None
            date_stay_to = None
        try:
            age_from = int(kw['age_from_create'])
            age_to = int(kw['age_to_create'])
            tmp = tmp + 'age: ' + str(age_from)
            tmp = tmp + ' '
        except:
            age_from = None
            age_to = None
        try:
            night_number_from = int(kw['night_number_from_create'])
            night_number_to = int(kw['night_number_to_create'])
            tmp = tmp + 'night: ' + str(night_number_from)
            tmp = tmp + ' '
        except:
            night_number_from = None
            night_number_to = None

        try:
            value_spo = float(kw['value_spo_create'])
            tmp = tmp + ' ' + str(value_spo)
            tmp = tmp + ' '
        except:
            value_spo = 0
        try:
            if kw['is_relative'] == 'on':
                is_relative_value = True
                tmp = tmp + '% '

        except:
            is_relative_value = False

        old_record = http.request.env[modal_name].search([('id', '=', int(kw['id']))])

        if modal_name == 'room.prices.detail':
            obj_spo = {
                'spo_config_id': spo_config.id,
                'chekin_from': date_chekin_from,
                'chekin_to': date_chekin_to,
                'chekout_from': date_chekout_from,
                'chekout_to': date_chekout_to,
                'date_creation_from': date_creation_from,
                'date_creation_to': date_creation_to,
                'day_stay_from': date_stay_from,
                'day_stay_to': date_stay_to,
                'age_from': age_from,
                'age_to': age_to,
                'night_number_from': night_number_from,
                'night_number_to': night_number_to,
                'room_prices_detail_id': old_record.id,
                'is_relative': is_relative_value,
                'spo_value': value_spo,
                'blocked_spo': False,
                'showed_name': tmp,
                'spo_type': spo_select_type,
                'one_time_payement': one_time_payment,
                'sequence': sequence

            }
        else:
            obj_spo = {
                'spo_config_id': spo_config.id,
                'chekin_from': date_chekin_from,
                'chekin_to': date_chekin_to,
                'chekout_from': date_chekout_from,
                'chekout_to': date_chekout_to,
                'date_creation_from': date_creation_from,
                'date_creation_to': date_creation_to,
                'day_stay_from': date_stay_from,
                'day_stay_to': date_stay_to,
                'age_from': age_from,
                'age_to': age_to,
                'night_number_from': night_number_from,
                'night_number_to': night_number_to,
                'room_prices_detail_other_id': old_record.id,
                'is_relative': is_relative_value,
                'spo_value': value_spo,
                'blocked_spo': False,
                'showed_name': tmp,
                'spo_type': spo_select_type,
                'one_time_payement': one_time_payment,
                'sequence': sequence

            }

        http.request.env['spo.values'].create(obj_spo)

        return http.request.redirect('/matrix/' + str(obj.id) + '/' + str(obj1.id))

    @http.route('/matrix/edit_spo/<model("contract.contract"):obj>/<model("room.prices"):obj1>', methods=['POST'],
                website=True,
                auth="user",
                )
    def edit_spo(self, obj, obj1, **kw):

        old_record = http.request.env['spo.values'].search([('id', '=', kw['spo_id'])])
        is_relative_value = False
        one_time_payment = False
        kw_spo = []
        spo_ids = []
        spo_ids_tmp = []
        for x in kw.keys():
            if 'spo_commutable' in x:
                kw_spo.append(x)
        for x in kw_spo:
            for y in kw[x].split(','):
                spo_ids_tmp.append(y)
        for x in spo_ids_tmp:
            if x not in old_record.not_commulable_with:
                spo_ids.append(x)

        try:
            sequence = kw['sequence_edit']
        except:
            sequence = None
        try:
            if kw['one_time_payement_edit'] == 'on':
                one_time_payment = True
        except:
            one_time_payment = False
        try:
            date_chekin_from = datetime.strptime(kw['checkin_from_edit'], '%Y-%m-%d').date()
            date_chekin_to = datetime.strptime(kw['checkin_to_edit'], '%Y-%m-%d').date()
        except:
            date_chekin_from = None
            date_chekin_to = None
        try:
            date_chekout_from = datetime.strptime(kw['checkout_from_edit'], '%Y-%m-%d').date()
            date_chekout_to = datetime.strptime(kw['checkout_to_edit'], '%Y-%m-%d').date()
        except:
            date_chekout_from = None
            date_chekout_to = None
        try:
            date_creation_from = datetime.strptime(kw['creation_from_edit'], '%Y-%m-%dT%H:%M:%S')
            date_creation_to = datetime.strptime(kw['creation_to_edit'], '%Y-%m-%dT%H:%M:%S')
        except:
            date_creation_from = None
            date_creation_to = None
        try:
            day_stay_from = datetime.strptime(kw['stay_from_edit'], '%Y-%m-%d').date()
            day_stay_to = datetime.strptime(kw['stay_to_edit'], '%Y-%m-%d').date()
        except:
            day_stay_from = None
            day_stay_to = None
        try:
            age_from = int(kw['age_from_edit'])
            age_to = int(kw['age_to_edit'])
        except:
            age_from = 0
            age_to = 0
        try:
            night_number_from = int(kw['night_number_from_edit'])
            night_number_to = int(kw['night_number_to_edit'])
        except:
            night_number_from = 0
            night_number_to = 0
        try:
            if kw['is_relative_edit'] == 'on':
                is_relative_value = True

        except:
            is_relative_value = False
        try:
            value_spo = float(kw['value_spo_edit'])
        except:
            value_spo = 0
        if len(spo_ids) > 0:
            old_record.update({
                'chekin_from': date_chekin_from,
                'chekin_to': date_chekin_to,
                'chekout_from': date_chekout_from,
                'chekout_to': date_chekout_to,
                'date_creation_from': date_creation_from,
                'date_creation_to': date_creation_to,
                'day_stay_from': day_stay_from,
                'day_stay_to': day_stay_to,
                'age_from': age_from,
                'age_to': age_to,
                'night_number_from': night_number_from,
                'night_number_to': night_number_to,
                'room_prices_detail_other_id': old_record.room_prices_detail_other_id,
                'room_prices_detail_id': old_record.room_prices_detail_id,
                'is_relative': is_relative_value,
                'spo_value': value_spo,
                'not_commulable_with': spo_ids,
                'one_time_payement': one_time_payment,
                'sequence': sequence,
                'spo_type': kw['spo_type_id']
            })
        elif len(spo_ids) == 0:
            old_record.update({
                'chekin_from': date_chekin_from,
                'chekin_to': date_chekin_to,
                'chekout_from': date_chekout_from,
                'chekout_to': date_chekout_to,
                'date_creation_from': date_creation_from,
                'date_creation_to': date_creation_to,
                'day_stay_from': day_stay_from,
                'day_stay_to': day_stay_to,
                'age_from': age_from,
                'age_to': age_to,
                'night_number_from': night_number_from,
                'night_number_to': night_number_to,
                'room_prices_detail_other_id': old_record.room_prices_detail_other_id,
                'room_prices_detail_id': old_record.room_prices_detail_id,
                'is_relative': is_relative_value,
                'spo_value': value_spo,
                'one_time_payement': one_time_payment,
                'sequence': sequence,
                'spo_type': kw['spo_type_id']

                # 'not_commulable_with': spo_ids,
            })
        return http.request.redirect('/matrix/' + str(obj.id) + '/' + str(obj1.id))

    @http.route('/matrix/blocked_spo',
                methods=['GET'],
                website=True,
                auth="user",
                )
    def blocked_spo(self, **kw):
        record = http.request.env['spo.values'].search([('id', '=', int(kw['id']))])
        record.update({
            'blocked_spo': True
        })
        return http.request.redirect('/matrix/' + str(kw['ctr']) + '/' + str(kw['rm']))

    @http.route('/matrix/unblocked_spo',
                methods=['GET'],
                website=True,
                auth="user",
                )
    def unblocked_spo(self, **kw):
        record = http.request.env['spo.values'].search([('id', '=', int(kw['id']))])
        record.update({
            'blocked_spo': False
        })
        return http.request.redirect('/matrix/' + str(kw['ctr']) + '/' + str(kw['rm']))

    @http.route('/matrix/copy_spo', methods=['GET'],
                website=True,
                auth="none",
                type='http'
                )
    def copy_spo(self, **kw):
        id_copy = int(kw['id_copy'])
        id_paste = int(kw['id_paste'])
        model_name_paste = kw['model_name_paste']
        old_record = http.request.env['spo.values'].search([('id', '=', id_copy)])
        if model_name_paste == 'room.prices.detail':
            obj_spo = {
                'spo_config_id': old_record.spo_config_id.id,
                'chekin_from': old_record.chekin_from,
                'chekin_to': old_record.chekin_to,
                'chekout_from': old_record.chekout_from,
                'chekout_to': old_record.chekout_to,
                'date_creation_from': old_record.date_creation_from,
                'date_creation_to': old_record.date_creation_to,
                'day_stay_from': old_record.day_stay_from,
                'day_stay_to': old_record.day_stay_to,
                'age_from': old_record.age_from,
                'age_to': old_record.age_to,
                'night_number_from': old_record.night_number_from,
                'night_number_to': old_record.night_number_to,
                'room_prices_detail_id': id_paste,
                'is_relative': old_record.is_relative,
                'spo_value': old_record.spo_value,
                'spo_type': old_record.spo_type,
                # 'not_commulable_with': old_record.not_commulable_with,
                'showed_name': old_record.showed_name,
                'blocked_spo': old_record.blocked_spo,

            }
        else:
            obj_spo = {
                'spo_config_id': old_record.spo_config_id.id,
                'chekin_from': old_record.chekin_from,
                'chekin_to': old_record.chekin_to,
                'chekout_from': old_record.chekout_from,
                'chekout_to': old_record.chekout_to,
                'date_creation_from': old_record.date_creation_from,
                'date_creation_to': old_record.date_creation_to,
                'day_stay_from': old_record.day_stay_from,
                'day_stay_to': old_record.day_stay_to,
                'age_from': old_record.age_from,
                'age_to': old_record.age_to,
                'night_number_from': old_record.night_number_from,
                'night_number_to': old_record.night_number_to,
                'room_prices_detail_other_id': id_paste,
                'is_relative': old_record.is_relative,
                'spo_value': old_record.spo_value,
                'spo_type': old_record.spo_type,
                # 'not_commulable_with': old_record.not_commulable_with,
                'blocked_spo': old_record.blocked_spo,
                'showed_name': old_record.showed_name,

            }

        rec = http.request.env['spo.values'].create(obj_spo)
        rec.not_commulable_with = old_record.not_commulable_with

    @http.route('/hotel/<model("contract.contract"):obj>/mass_spo', type='http', methods=['GET'], auth="user",
                website=True)
    def mass_spo_insertion(self, obj, **kw):
        """

        :param obj: current contract
        :param kw: optionnal attributes
        :return:
        """
        list_room_prices = obj.room_prices
        list_room_categories = []
        donnee = []
        for rm in list_room_prices:
            if rm.room not in list_room_categories:
                list_room_categories.append(rm.room)
        for x in list_room_categories:
            list_matrix_types = []
            ser = http.request.env['room.prices'].search([('contract_id', '=', obj.id), ('room', '=', x.id)])
            for elmt in ser:
                list_matrix_types.append(elmt.prices_type)
                if elmt.prices_type == 'n':
                    matrix_net = elmt
                if elmt.prices_type == 's':
                    matrix_sale = elmt
                acc_test = []
                meal_test = []
                for z1 in ser[0].accomodations:
                    if z1 not in acc_test:
                        acc_test.append(z1)
                for z2 in ser[0].meals:
                    if z2 not in meal_test:
                        meal_test.append(z2)

            obj_rm_vw = {
                'category_name': '/room/' + str(list_room_prices[0].id),
                'matrix_net': matrix_net,
                'matrix_sale': matrix_sale,
                'acc_av': acc_test,
                'meal_av': meal_test,
            }
            donnee.append(obj_rm_vw)

        try:
            contract = obj.id

            company_id = request.session['company_id']
            request.session['contract_id'] = contract
            return request.render(
                'product_price_computation_carthage_group.mass_spo_insertion', {
                    'contract': obj,
                    'page_title': obj.hotel.name,
                    'company_id': company_id,
                    'donnee': donnee
                }
            )
        except:
            return request.redirect('/home')

    @http.route('/hotel/room/create_mass_spo', type='http', methods=['POST'], auth="user",
                website=True)
    def mass_spo_creation(self, **kw):
        list_key = kw.keys()
        list_matrix_ids = []
        list_destinations = []
        list_acc_baseprice = []
        for lll in http.request.env['accomodations'].search([('is_base', '=', True)]):
            list_acc_baseprice.append(lll.id)
        for ll in list_key:
            if 'matrix' in ll:
                list_matrix_ids.append(int(kw[ll]))
        contract_id = http.request.env['room.prices'].search([('id', '=', list_matrix_ids[0])]).contract_id.id
        for x in list_matrix_ids:
            list_acc_ids = []
            list_meal_ids = []
            for y in list_key:
                if ('acc_mass' + str(x)) in y:
                    list_acc_ids.append(kw[y])
                if ('meal_mass' + str(x)) in y:
                    list_meal_ids.append(kw[y])
            for x1 in list_acc_ids:
                for x2 in list_meal_ids:
                    destination = {
                        'id_matrix': x,
                        'id_acc': x1,
                        'id_meal': x2
                    }
                    list_destinations.append(destination)
                    if (x + 1) in list_matrix_ids:
                        destination1 = {
                            'id_matrix': x + 1,
                            'id_acc': x1,
                            'id_meal': x2
                        }
                        list_destinations.append(destination1)

        is_relative_value = False
        try:
            spo_config = int(kw['spo_config_id'])
        except:
            spo_config = None
        spo_config_elt = http.request.env['spo.configuration'].search([('id', '=', spo_config)])
        tmp = spo_config_elt.name_spo + ' '

        try:
            spo_type = kw['spo_type_id']
        except:
            spo_type = None

        try:
            date_chekin_from = datetime.strptime(kw['checkin_from_create_mass'], '%Y-%m-%d').date()
            date_chekin_to = datetime.strptime(kw['checkin_to_create_mass'], '%Y-%m-%d').date()
            tmp = tmp + 'chIN: ' + datetime.strftime(date_chekin_from, '%m.%d.%y')
            tmp = tmp + '\n'
        except:
            date_chekin_from = None
            date_chekin_to = None
        try:
            date_chekout_from = datetime.strptime(kw['checkout_from_create_mass'], '%Y-%m-%d').date()
            date_chekout_to = datetime.strptime(kw['checkout_to_create_mass'], '%Y-%m-%d').date()
            tmp = tmp + 'chOUT: ' + datetime.strftime(date_chekout_from, '%m.%d.%y')
            tmp = tmp + '\n'
        except:
            date_chekout_from = None
            date_chekout_to = None
        try:
            date_creation_from = datetime.strptime(kw['creation_from_create_mass'], '%Y-%m-%d').date()
            date_creation_to = datetime.strptime(kw['creation_to_create_mass'], '%Y-%m-%d').date()
            tmp = tmp + 'cr: ' + datetime.strftime(date_creation_from, '%m.%d.%yT%H:%M')
            tmp = tmp + '\n'
        except:
            date_creation_from = None
            date_creation_to = None
        try:
            day_stay_from = datetime.strptime(kw['stay_from_create_mass'], '%Y-%m-%d').date()
            day_stay_to = datetime.strptime(kw['stay_to_create_mass'], '%Y-%m-%d').date()
            tmp = tmp + 'pr: ' + datetime.strftime(day_stay_from, '%m.%d.%y')
            tmp = tmp + '\n'
        except:
            day_stay_from = None
            day_stay_to = None
        try:
            age_from = int(kw['age_min_mass'])
            age_to = int(kw['age_max_mass'])
            tmp = tmp + 'age: ' + str(age_from)
            tmp = tmp + '\n'
        except:
            age_from = None
            age_to = None
        try:
            night_number_from = int(kw['number_min_form'])
            night_number_to = int(kw['number_max_form'])
            tmp = tmp + 'night: ' + str(night_number_from)
            tmp = tmp + '\n'
        except:
            night_number_from = None
            night_number_to = None

        try:
            value_spo = float(kw['value_form_mass'])
            tmp = tmp + ' ' + str(value_spo)
            tmp = tmp + '\n'
        except:
            value_spo = None
        try:
            if kw['is_relative_value'] == 'on':
                is_relative_value = True
                tmp = tmp + '% '

        except:
            is_relative_value = False
        for li in list_destinations:

            if int(li['id_acc']) in list_acc_baseprice:
                record_detail = http.request.env['room.prices.detail'].search(
                    [('room_prices_id', '=', int(li['id_matrix'])), ('accomodation', '=', int(li['id_acc'])),
                     ('meal', '=', int(li['id_meal']))])
                obj_create = {
                    'spo_config_id': spo_config,
                    'spo_type': spo_type,
                    'chekin_from': date_chekin_from,
                    'chekin_to': date_chekin_to,
                    'chekout_from': date_chekout_from,
                    'chekout_to': date_chekout_to,
                    'date_creation_from': date_creation_from,
                    'date_creation_to': date_creation_to,
                    'day_stay_from': day_stay_from,
                    'day_stay_to': day_stay_to,
                    'age_from': age_from,
                    'age_to': age_to,
                    'night_number_from': night_number_from,
                    'night_number_to': night_number_to,
                    'room_prices_detail_id': record_detail.id,
                    'is_relative': is_relative_value,
                    'spo_value': value_spo,
                    'blocked_spo': False,
                    'showed_name': tmp,
                    # 'one_time_payement': one_time_payment,
                    # 'sequence': sequence
                }
                http.request.env['spo.values'].create(obj_create)
            else:
                record = http.request.env['room.prices.detail.other'].search(
                    [('room_prices_id', '=', int(li['id_matrix'])), ('accomodation', '=', int(li['id_acc'])),
                     ('meal', '=', int(li['id_meal']))])
                obj_create = {
                    'spo_config_id': spo_config,
                    'spo_type': spo_type,
                    'chekin_from': date_chekin_from,
                    'chekin_to': date_chekin_to,
                    'chekout_from': date_chekout_from,
                    'chekout_to': date_chekout_to,
                    'date_creation_from': date_creation_from,
                    'date_creation_to': date_creation_to,
                    'day_stay_from': day_stay_from,
                    'day_stay_to': day_stay_to,
                    'age_from': age_from,
                    'age_to': age_to,
                    'night_number_from': night_number_from,
                    'night_number_to': night_number_to,
                    'room_prices_detail_other_id': record.id,
                    'is_relative': is_relative_value,
                    'spo_value': value_spo,
                    'blocked_spo': False,
                    'showed_name': tmp,
                    # 'one_time_payement': one_time_payment,
                    # 'sequence': sequence
                }
                http.request.env['spo.values'].create(obj_create)

        return request.redirect('/hotel/' + str(contract_id) + '/mass_spo')

    @http.route('/hotel/<model("contract.contract"):obj>/spo_settings_mass', type='http', methods=['GET'], auth="user",
                website=True)
    def cummul_spo_settings(self, obj, **kw):
        """

        :param obj: current contract
        :param kw: optionnal attributes
        :return:
        """
        spo_names_from = []
        spo_names_to = []
        try:
            contract = obj.id
            for x in obj.room_prices:
                for y in x.base_prices:
                    for z in y.ac_spos_id:
                        if z.showed_name not in spo_names_from:
                            spo_names_from.append(z.showed_name)
                            spo_names_to.append(z.showed_name)
                for y in x.other_prices:
                    for z in y.ac_spos_id:
                        if z.showed_name not in spo_names_from:
                            spo_names_from.append(z.showed_name)
                            spo_names_to.append(z.showed_name)

            company_id = request.session['company_id']
            request.session['contract_id'] = contract
            return request.render(
                'product_price_computation_carthage_group.cummul_modification', {
                    'contract': obj,
                    'page_title': obj.hotel.name,
                    'company_id': company_id,
                    'spos_from': spo_names_from,
                    'spos_to': spo_names_to

                }
            )
        except:
            return request.redirect('/home')

    @http.route('/hotel/room/spo_settings_mass', type='http', methods=['POST'], auth="user",
                website=True)
    def cummul_spo_settings_post(self, **kw):
        """

        :param obj: current contract
        :param kw: optionnal attributes
        :return:
        """
        spo_names_from = []
        spo_names_to = []
        spo_values_from = []
        spo_values_to = []
        spo_names_from = request.httprequest.form.getlist('source')
        spo_names_to = request.httprequest.form.getlist('destination')
        spo_values_from = request.env['spo.values'].search([('showed_name','in',spo_names_from)])
        spo_values_to = request.env['spo.values'].search([('showed_name','in',spo_names_to)])
        spo_values_to_id = []
        for x in spo_values_to:
            spo_values_to_id.append(x.id)
        for spo in spo_values_from:
            for spo_to in spo_values_to:
                query = 'insert into values_values_rel (val1 , val2) values ({0},{1})'.format(spo.id,spo_to.id)
                request._cr.execute(query)


        try:
            contract = request.env['contract.contract'].search([('id', '=', int(request.session['contract_id']))])
            for x in contract.room_prices:
                for y in x.base_prices:
                    for z in y.ac_spos_id:
                        if z.showed_name not in spo_names_from:
                            spo_names_from.append(z.showed_name)
                            spo_names_to.append(z.showed_name)
                for y in x.other_prices:
                    for z in y.ac_spos_id:
                        if z.showed_name not in spo_names_from:
                            spo_names_from.append(z.showed_name)
                            spo_names_to.append(z.showed_name)

            company_id = request.session['company_id']
            request.session['contract_id'] = contract.id
            return request.render(
                'product_price_computation_carthage_group.cummul_modification', {
                    'contract': contract,
                    'page_title': contract.hotel.name,
                    'company_id': company_id,
                    'spos_from': spo_names_from,
                    'spos_to': spo_names_to

                }
            )
        except:
            return request.redirect('/home')

    @http.route('/reservations/get_price/<int:obj>', type='http', methods=['GET'], auth="user", website=True)
    def get_price_only(self, obj, **get):
        res_rec = request.env['ctm.reservation.list'].browse(obj)
        prices_dict = res_rec.calculate_prices(obj)
        res_rec.update({
            'net': prices_dict['net']
        })
        return request.redirect('/reservations/show/' + str(res_rec.id))

    @http.route('/hotel/<model("contract.contract"):obj>/mass_spo_edit', type='http', methods=['GET'], auth="user",
                website=True)
    def mass_spo_edit(self, obj, **kw):
        """

        :param obj: current contract
        :param kw: optionnal attributes
        :return:
        """
        list_room_prices = obj.room_prices
        list_room_detail_prices = []
        list_room_detail_prices_other = []
        list_spo_total = []
        list_spo_show_name = []
        list_spo_final = []
        donnee = []
        for x in obj.room_prices:
            list_room_detail_prices.append(x.base_prices.id)
            list_room_detail_prices_other.append(x.other_prices.id)
        for y in http.request.env['spo.values'].search([('room_prices_detail_id', 'in', list_room_detail_prices)]):
            list_spo_total.append(y)
        for y in http.request.env['spo.values'].search(
                [('room_prices_detail_other_id', 'in', list_room_detail_prices_other)]):
            list_spo_total.append(y)
        for x in list_spo_total:
            if x.showed_name not in list_spo_show_name:
                list_spo_show_name.append(x.showed_name)
        # for x in list_spo_show_name:

        try:
            contract = obj.id

            company_id = request.session['company_id']
            request.session['contract_id'] = contract
            return request.render(
                'product_price_computation_carthage_group.mass_spo_edit', {
                    'contract': obj,
                    'page_title': obj.hotel.name,
                    'company_id': company_id,
                    'donnee': donnee
                }
            )
        except:
            return request.redirect('/home')
