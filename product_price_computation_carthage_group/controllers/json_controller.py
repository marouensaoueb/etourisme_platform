# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request


class JSonHandlers(http.Controller):

    @http.route('/get_hotels/<obj>', type='http', methods=['GET'], auth="none", website=True)
    def gethotels(self, obj, **kw):
        country_id = obj
        hotels = request.env['rooming.hotels'].sudo().search([('state', '=', int(country_id))])
        obj = {

        }
        l = []
        for x in hotels:
            obj = {
                'id': x.id,
                'hotel_name': x.name
            }
            l.append(obj)
        content = {
            'hotels': json.dumps(l)
        }
        return request.make_response(json.dumps(l), [('Content-Type', 'application/json')])

    @http.route('/get_accomodations/', type='http', methods=['GET'], auth="none", website=True)
    def getacc(self, **kw):
        min = int(kw['min'])
        max = int(kw['max'])
        accomodations = []
        for m in range(0, max + 1):
            for n in range(0, max):
                for k in range(0, max):
                    if m + n + k <= max and m + n + k >= min:
                        for x in request.env['accomodations'].search(
                                [('adult', '=', m), ('child', '=', n), ('inf', '=', k),
                                 ('visible_in_prices', '=', True)]):
                            obj_acc = {
                                'id': x.id,
                                'accomodation_name': x.code
                            }
                            accomodations.append(obj_acc)

        return request.make_response(json.dumps(accomodations), [('Content-Type', 'application/json')])

    @http.route('/get_accomodations_room/', type='http', methods=['GET'], auth="none", website=True)
    def getacc_room(self, **kw):
        room_id = int(kw['room'])
        room = request.env['room.prices'].search([('id', '=', room_id)])
        min = room.min
        max = room.max
        accomodations = []
        for m in range(1, max + 1):
            for n in range(0, max):
                for k in range(0, max):
                    if m + n + k <= max and m + n + k >= min:
                        for x in request.env['accomodations'].search(
                                [('adult', '=', m), ('child', '=', n), ('inf', '=', k),
                                 ('visible_in_prices', '=', True)]):
                            is_avaible = False
                            if x in room.accomodations:
                                is_avaible = True
                            obj_acc = {
                                'id': x.id,
                                'accomodation_name': x.code,
                                'is_avaible': is_avaible
                            }
                            accomodations.append(obj_acc)

        return request.make_response(json.dumps(accomodations), [('Content-Type', 'application/json')])

    @http.route('/get_meals_room/', type='http', methods=['GET'], auth="none", website=True)
    def getmeals_room(self, **kw):
        meals_id = []
        room_id = int(kw['room'])
        room = request.env['room.prices'].sudo().search([('id', '=', room_id)])

        def myfunc(e):
            return e.sequence

        bb = []
        for x in request.env['room.meal'].sudo().search([]):
            bb.append(x)
        bb.sort(key=myfunc)
        for x in bb:
            is_avaible = False
            if x in room.meals:
                is_avaible = True
            obj_meal = {
                'id': x.id,
                'meal_name': x.name,
                'is_avaible': is_avaible,
                'is_base_price': x.base_price
            }
            meals_id.append(obj_meal)
        return request.make_response(json.dumps(meals_id), [('Content-Type', 'application/json')])

    @http.route('/get_spo/<obj>', type='http', methods=['GET'], auth="none", website=True)
    def get_spo(self, obj, **kw):
        spo_id = obj
        spo_config = request.env['spo.configuration'].sudo().search([('id', '=', int(spo_id))])
        spos = []
        obj_spo = {
            'id': spo_config.id,
            'checkin': spo_config.period_chekin,
            'checkout': spo_config.period_chekout,
            'date_creation': spo_config.period_date_creation,
            'age': spo_config.age,
            'night_number': spo_config.night_number,
            'pay_stay': spo_config.pay_stay,
            'date_stay': spo_config.date_stay,
        }
        spos.append(obj_spo)
        return request.make_response(json.dumps(spos), [('Content-Type', 'application/json')])

    @http.route('/get_spo_edit/<obj>', type='http', methods=['GET'], auth="none", website=True)
    def get_spo_edit(self, obj, **kw):
        room = http.request.env['room.prices'].search([('id', '=', obj)])
        id_courant = kw['id_edit']
        list_spo_val = []
        list_spo_con = []
        list_spo_con_obj = []
        already_chosen = False
        cpt = 0
        sps = http.request.env['spo.values'].search([('id', '=', id_courant)])
        '''
        some cool work to alter this crap job
        '''
        the_chosen_ones = []
        idds = []
        temporary_names_table = []
        choice = False
        if sps.room_prices_detail_id:
            choice = True
        if choice:
            # for b in room.base_prices:
            #     idds.append(b.id)
            idds.append(sps.room_prices_detail_id.id)
            other_spos_in_the_matrix_non_filtered = http.request.env['spo.values'].search(
                [('showed_name', '!=', sps.showed_name),
                 ('room_prices_detail_id.id',
                  'in', idds)])
        else:
            # for b in room.other_prices:
            #     idds.append(b.id)
            idds.append(sps.room_prices_detail_other_id.id)
            other_spos_in_the_matrix_non_filtered = http.request.env['spo.values'].search(
                [('showed_name', '!=', sps.showed_name),
                 (
                     'room_prices_detail_other_id.id',
                     'in', idds)])
        for x in other_spos_in_the_matrix_non_filtered:
            if x.showed_name not in temporary_names_table:
                temporary_names_table.append(x.showed_name)
        for x in temporary_names_table:
            llist = []
            idbs = []
            llnames_list = ''
            if choice:
                idbs.append(sps.room_prices_detail_id.id)
                for y in http.request.env['spo.values'].search(
                        [('room_prices_detail_id.id', 'in', idbs)]):
                    if y.showed_name == x:
                        llist.append(y.id)
                        llnames_list = y.spo_config_id.name_spo
            else:
                idbs.append(sps.room_prices_detail_other_id.id)
                for y in http.request.env['spo.values'].search(
                        [('room_prices_detail_other_id.id', 'in', idbs)]):
                    if y.showed_name == x:
                        llist.append(y.id)
                        llnames_list = y.spo_config_id.name_spo

            # test if we have something like this in this spo
            for sp in sps.not_commulable_with:
                for ii in llist:
                    if sp.id == ii:
                        already_chosen = True
            ob = {
                'id': cpt,
                'tooltip': x,
                'ids': llist,
                'name': llnames_list,
                'allready_chosen': already_chosen,
            }
            the_chosen_ones.append(ob)
            cpt = cpt + 1

        return request.make_response(json.dumps(the_chosen_ones), [('Content-Type', 'application/json')])

    @http.route('/get_hotel_company', type='http', methods=['GET'], auth="none", website=True)
    def hotelbycompany(self, **kw):
        company_id = kw['id']
        company = request.env['res.company'].sudo().search([('id', '=', int(company_id))])
        hotels = request.env['rooming.hotels'].sudo().search([])
        list_hotel = []
        for h in hotels:
            if company in h.allowed_companys:
                obj_hotel = {
                    'hotel_id': h.id,
                    'hotel_name': h.name
                }
                list_hotel.append(obj_hotel)

        return request.make_response(json.dumps(list_hotel), [('Content-Type', 'application/json')])

    @http.route('/get_room_hotel', type='http', methods=['GET'], auth="none", website=True)
    def roombyhotel(self, **kw):
        company_id = int(kw['id_company'])
        hotel_id = int(kw['id_hotel'])
        room_avaible = request.env['contract.contract'].sudo().search(
            [('company_id', '=', company_id), ('hotel', '=', hotel_id)]).rooms
        list_rooms = []
        for h in room_avaible:
            obj_hotel = {
                'room_id': h.id,
                'room_name': h.name
            }
            list_rooms.append(obj_hotel)

        return request.make_response(json.dumps(list_rooms), [('Content-Type', 'application/json')])

    @http.route('/get_meal_accomodation', type='http', methods=['GET'], auth="none", website=True)
    def meal_accbyroom(self, **kw):
        company_id = int(kw['company_id'])
        hotel_id = int(kw['hotel_id'])
        room_id = int(kw['room_id'])
        contract = request.env['contract.contract'].sudo().search(
            [('company_id', '=', company_id), ('hotel', '=', hotel_id)])
        room_prices = request.env['room.prices'].sudo().search(
            [('room', '=', room_id), ('contract_id', '=', contract.id)])[0]
        list_meal = []
        list_acc = []
        for x in room_prices.accomodations:
            acc = {
                'acc_id': x.id,
                'acc_name': x.codef
            }
            list_acc.append(acc)
        for x in room_prices.meals:
            meal = {
                'meal_id': x.id,
                'meal_name': x.name
            }
            list_meal.append(meal)
        list_meal_acc = {
            'list_meal': list_meal,
            'list_acc': list_acc
        }
        return request.make_response(json.dumps(list_meal_acc), [('Content-Type', 'application/json')])
