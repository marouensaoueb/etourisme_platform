# -*- coding: utf-8 -*-

from datetime import timedelta, datetime

from odoo import models, fields, api


class TouroperatorInherit(models.Model):
    _inherit = 'tour.operator'

    sequence_config = fields.Many2one('ir.sequence', string="Sequence Config")


class InheritMeals(models.Model):
    _inherit = 'room.meal'

    code = fields.Char(string='Code')
    sequence = fields.Integer('sequence')
    base_price = fields.Boolean('is base price')


class ReservationsInherit(models.Model):
    _inherit = 'ctm.reservation.list'

    @api.onchange('exchange_rate')
    def _set_tnd(self):
        self.tnd_amount = self.net * self.exchange_rate

    accomodation = fields.Many2one('accomodations', string="accomodation")
    res_to_ref = fields.Char('Tour operator code')
    s_date = fields.Date('Sending date')
    sale = fields.Monetary('Sale', digits=(10, 3))
    meal = fields.Many2one('room.meal', string='Meal')
    exchange_rate = fields.Float('taux de change', digits=(10, 3))
    tnd_amount = fields.Float('Montant TND', digits=(10, 3))

    def calculate_prices(self, reservation_id):
        reservation_record = self.env['ctm.reservation.list'].browse(reservation_id)
        contract = self.env['contract.contract'].search(
            [('hotel', '=', reservation_record.hotel_id.id),
             ('mr_id', 'in', reservation_record.touroperator_id.mr_id.id)])
        sale_room = False
        net_room = False
        result = []
        if not contract:
            raise UserWarning('error , no contract found for the res {0}'.format(reservation_record.reservation_number))
        sale_room = self.env['room.prices'].search([('contract_id', '=', contract.id), ('prices_type', '=', 's'),
                                                    ('room', '=', reservation_record.room_category.id)])
        net_room = self.env['room.prices'].search([('contract_id', '=', contract.id), ('prices_type', '=', 'n'),
                                                   ('room', '=', reservation_record.room_category.id)])
        accomodation = reservation_record.accomodation
        meal = reservation_record.meal
        tmp = accomodation
        net_price = 0
        brut_sum = 0
        brut_price = 0
        sale_price = 0
        kk = 0
        days_to_use = (reservation_record.checkout - reservation_record.chekin).days
        date_list = [reservation_record.chekin + timedelta(days=kk) for kk in range(0, days_to_use)]
        ric = []

        def get_active_spos(price_detail, date_creation, date_checkin, date_checkout, jour_from, jour_to, age=None):
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
                    age_bool = True
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
                            if date_creation >= x.date_creation_from.date() and date_creation <= x.date_creation_to.date():
                                creation_bool = True
                            else:
                                creation_bool = False

                        if x.spo_config_id.age:
                            if age:
                                if age >= x.age_from and age <= x.age_to:
                                    age_bool = True
                                else:
                                    age_bool = False
                            else:
                                age_bool = False

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
                        if checkin_bool and checkout_bool and creation_bool and night_number_bool and day_stay_bool and age_bool:
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

                        if x.spo_config_id.age:
                            if age:
                                if age >= x.age_from and age <= x.age_to:
                                    age_bool = True
                                else:
                                    age_bool = False
                            else:
                                age_bool = False

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
                        if checkin_bool and checkout_bool and creation_bool and night_number_bool and day_stay_bool and age_bool:
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
            spos_rec = self.env['spo.values'].search([('id', 'in', active_spos_list_ids)])
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
                    spos = self.env['spo.values'].search([('id', 'in', x)], order="sequence Asc")
                    tmp = ordinary_price
                    for y in spos:

                        if y.spo_type == 'moins':
                            if y.is_relative:
                                tmp = tmp - ((tmp / 100) * y.spo_value)
                            else:
                                tmp = tmp - y.tmp
                        else:
                            if y.is_relative:
                                tmp = tmp + ((tmp / 100) * y.spo_value)
                            else:
                                tmp = tmp + y.spo_value
                    if tmp < min:
                        min = tmp
                return min
            else:
                return ordinary_price

        def calculate_single_accomodation(room_price_detail, acc, meal, date_list, age_min=None, age_max=None):
            # TODO insert spo calculation in each day and after
            sum = 0
            brut_sum = 0

            if age_min is None and age_max is None:
                for jour in date_list:
                    tmp = 0
                    tm1 = 0
                    base_val = 0

                    base_meal_id = self.env['room.meal'].search([('code', '=', 'BP')]).id
                    base_acc_id = self.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_dbl')
                    if acc.is_base:
                        # get the base price
                        base_price_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if acc.code == 'SGL' and base_prices_date_record.is_relative is True:
                            base_price_record = self.env['room.prices.detail'].search(
                                [('meal.id', '=', base_meal_id), ('accomodation', '=', base_acc_id),
                                 ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                                 ])
                            base_prices_date_record = self.env['room.prices.detail.dates'].search(
                                [('room_prices_detail_id', '=', base_price_record.id),
                                 ('date_from', '<=', jour), ('date_to', '>=', jour)])
                            tm1 = tm1 + base_prices_date_record.price
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        # todo insert spo on base modifications here
                        if True:
                            active_spos = get_active_spos(base_price_record, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                            brut_sum = brut_sum + tm1
                        else:
                            base_val = tm1
                            brut_sum = brut_sum + tm1
                        base_price_acc_meal_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # get the meal price
                        price_record = self.env['room.prices.detail'].search(
                            [('meal', '=', meal.id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if True:
                            active_spos = get_active_spos(room_price_detail, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                            brut_sum = brut_sum + tmp
                        else:
                            sum = sum + tmp + base_val
                            brut_sum = brut_sum + tmp

                    else:
                        # prepare the dbl on [base price ] accomodatino price
                        base_price_acc_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=',
                                                              self.env['ir.model.data'].xmlid_to_res_id(
                                                                  'product_price_computation_carthage_group.accomodation_dbl')),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        base_price_acc_meal_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # get the base price
                        base_price_record = self.env['room.prices.detail.other'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = self.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if base_prices_date_record.is_relative:
                            tm1 = tm1 + ((base_prices_acc_date_record.price / 100) * base_prices_date_record.price)
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if True:
                            active_spos = get_active_spos(base_price_record, reservation_record.creation_date,
                                                          reservation_record.chekin,
                                                          reservation_record.checkout, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                            brut_sum = brut_sum + tm1
                        else:
                            base_val = tm1
                            brut_sum = brut_sum + tm1

                        # get the meal price
                        price_record = self.env['room.prices.detail.other'].search(
                            [('meal', '=', meal.id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = self.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/nigh spo here
                        if True:
                            active_spos = get_active_spos(room_price_detail, reservation_record.creation_date,
                                                          reservation_record.chekin,
                                                          reservation_record.checkout, jour, jour)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                            brut_sum = brut_sum + tmp
                        else:
                            sum = sum + tmp + base_val
                            brut_sum = brut_sum + tmp
            else:
                for jour in date_list:
                    tmp = 0
                    tm1 = 0
                    base_val = 0
                    base_meal_id = self.env['room.meal'].search([('code', '=', 'BP')]).id
                    base_acc_id = self.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_dbl')
                    if acc.is_base:
                        # get the base price
                        base_price_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '<=', age_min),
                             ('age_max', '>=', age_max)])
                        if acc.code == 'SGL' and base_prices_date_record.is_relative is True:
                            base_price_record = self.env['room.prices.detail'].search(
                                [('meal.id', '=', base_meal_id), ('accomodation.id', '=', base_acc_id),
                                 ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                                 ])
                            base_prices_date_record = self.env['room.prices.detail.dates'].search(
                                [('room_prices_detail_id', '=', base_price_record.id),
                                 ('date_from', '<=', jour), ('date_to', '>=', jour),
                                 ('age_min', '<=', age_min),
                                 ('age_max', '>=', age_max)])
                            tm1 = tm1 + base_prices_date_record.price
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if True:
                            active_spos = get_active_spos(base_price_record, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour, age_min)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                            brut_sum = brut_sum + tm1
                        else:
                            base_val = tm1
                            brut_sum = brut_sum + tm1
                        # get the meal price
                        base_price_acc_meal_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        price_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '<=', age_min),
                             ('age_max', '>=', age_max)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if True:
                            active_spos = get_active_spos(room_price_detail, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour, age_min)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                            brut_sum = brut_sum + tmp
                        else:
                            sum = sum + tmp + base_val
                            brut_sum = brut_sum + tmp
                    else:
                        # prepare the dbl on [base price ] accomodatino price
                        base_price_acc_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation.id', '=',
                                                              self.env['ir.model.data'].xmlid_to_res_id(
                                                                  'product_price_computation_carthage_group.accomodation_dbl')),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        base_price_acc_meal_record = self.env['room.prices.detail'].search(
                            [('meal.id', '=', meal.id), ('accomodation.id', '=', base_acc_id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_acc_meal_date_record = self.env['room.prices.detail.dates'].search(
                            [('room_prices_detail_id', '=', base_price_acc_meal_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour)])
                        # get the base price
                        base_price_record = self.env['room.prices.detail.other'].search(
                            [('meal.id', '=', base_meal_id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        base_prices_date_record = self.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', base_price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '<=', age_min),
                             ('age_max', '>=', age_max)])
                        if base_prices_date_record.is_relative:
                            tm1 = tm1 + ((base_prices_acc_date_record.price / 100) * base_prices_date_record.price)
                        else:
                            tm1 = tm1 + base_prices_date_record.price
                        if True:
                            active_spos = get_active_spos(base_price_record, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour, age_min)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            base_val = base_val + calculate_spos(tm1, sppgroups)
                            brut_sum = brut_sum + tm1
                        else:
                            base_val = tm1
                            brut_sum = brut_sum + tm1
                        # get the meal price
                        price_record = self.env['room.prices.detail.other'].search(
                            [('meal', '=', meal.id), ('accomodation', '=', acc.id),
                             ('room_prices_id', '=', room_price_detail.room_prices_id.id)
                             ])
                        prices_date_record = self.env['room.prices.detail.dates.other'].search(
                            [('room_prices_detail_id', '=', price_record.id),
                             ('date_from', '<=', jour), ('date_to', '>=', jour), ('age_min', '<=', age_min),
                             ('age_max', '>=', age_max)])
                        if prices_date_record.is_relative:
                            tmp = tmp + ((base_prices_acc_meal_date_record.price / 100) * prices_date_record.price)
                        else:
                            tmp = tmp + prices_date_record.price
                            # todo find a way to apply acc/night spo here
                        if True:
                            active_spos = get_active_spos(room_price_detail, reservation_record.creation_date,
                                                          reservation_record.chekin, reservation_record.checkout, jour,
                                                          jour, age_min)
                            nnccssppss = get_nn_cumm_spos(active_spos[0])
                            sppgroups = get_spos_groups(active_spos[0], nnccssppss)
                            sum = sum + base_val + calculate_spos(tmp, sppgroups)
                            brut_sum = brut_sum + tmp
                        else:
                            sum = sum + tmp + base_val
                            brut_sum = brut_sum + tmp
            # todo find a way to apply acc/period spo here
            if True:
                active_spos = get_active_spos(room_price_detail, reservation_record.creation_date,
                                              reservation_record.chekin, reservation_record.checkout,
                                              reservation_record.chekin, reservation_record.checkout, age_min)
                nnccssppss = get_nn_cumm_spos(active_spos[1])
                sppgroups = get_spos_groups(active_spos[1], nnccssppss)
                sum = calculate_spos(sum, sppgroups)

            return {'brut': brut_sum, 'net': sum}

        for y in reservation_record.reservation_detail:
            if y.age == 0:
                ageobj = {
                    'age': 40,
                }
                ric.append(ageobj)
            elif y.age >= contract.min_enf_age:
                ageobj = {
                    'age': y.age,
                }
                ric.append(ageobj)

        def ages_key(e):
            return e['age']

        ric.sort(key=ages_key)
        i = 0
        while tmp:
            age = ric[i]
            dbltmp = self.env['accomodations'].search([('id', '=', self.env[
                'ir.model.data'].xmlid_to_res_id(
                'product_price_computation_carthage_group.accomodation_dbl'))])
            sgltmp = self.env['accomodations'].search([('id', '=', self.env[
                'ir.model.data'].xmlid_to_res_id(
                'product_price_computation_carthage_group.accomodation_sgl'))])
            if tmp.id == self.env['ir.model.data'].xmlid_to_res_id(
                    'product_price_computation_carthage_group.accomodation_2_dbl'):
                prices_record_net = self.env['room.prices.detail'].search(
                    [('meal', '=', meal.id), ('accomodation', '=', dbltmp.id), ('room_prices_id', '=', net_room.id)]) or \
                                    self.env[
                                        'room.prices.detail.other'].search(
                                        [('meal', '=', meal.id), ('accomodation', '=', tmp.id),
                                         ('room_prices_id', '=', net_room.id)])
            else:
                prices_record_net = self.env['room.prices.detail'].search(
                    [('meal', '=', meal.id), ('accomodation', '=', tmp.id), ('room_prices_id', '=', net_room.id)]) or \
                                    self.env[
                                        'room.prices.detail.other'].search(
                                        [('meal', '=', meal.id), ('accomodation', '=', tmp.id),
                                         ('room_prices_id', '=', net_room.id)])
            prices_record_sale = self.env['room.prices.detail'].search(
                [('meal', '=', meal.id), ('accomodation', '=', tmp.id), ('room_prices_id', '=', sale_room.id)]) or \
                                 self.env[
                                     'room.prices.detail.other'].search(
                                     [('meal', '=', meal.id), ('accomodation', '=', tmp.id),
                                      ('room_prices_id', '=', sale_room.id)])

            if tmp.id == self.env['ir.model.data'].xmlid_to_res_id(
                    'product_price_computation_carthage_group.accomodation_2_dbl'):
                try:
                    net_price = net_price + calculate_single_accomodation(prices_record_net, dbltmp,
                                                                          prices_record_net.meal,
                                                                          date_list, ric[i]['age'], ric[i]['age'])[
                        'net']
                    brut_price = brut_price + calculate_single_accomodation(prices_record_net, dbltmp,
                                                                            prices_record_net.meal,
                                                                            date_list, ric[i]['age'], ric[i]['age'])[
                        'brut']
                except:
                    net_price = net_price + calculate_single_accomodation(prices_record_net, dbltmp,
                                                                          prices_record_net.meal,
                                                                          date_list, )['net']
                    brut_price = brut_price + calculate_single_accomodation(prices_record_net, dbltmp,
                                                                            prices_record_net.meal,
                                                                            date_list, )['brut']
            elif tmp.id == self.env['ir.model.data'].xmlid_to_res_id(
                    'product_price_computation_carthage_group.accomodation_sgl'):
                try:

                    net_price = net_price + calculate_single_accomodation(prices_record_net, sgltmp,
                                                                          prices_record_net.meal,
                                                                          date_list, ric[i]['age'], ric[i]['age'])[
                        'net']
                    brut_price = brut_price + calculate_single_accomodation(prices_record_net, sgltmp,
                                                                            prices_record_net.meal,
                                                                            date_list, ric[i]['age'], ric[i]['age'])[
                        'brut']
                except:
                    net_price = net_price + calculate_single_accomodation(prices_record_net, sgltmp,
                                                                          prices_record_net.meal,
                                                                          date_list, )['net']
                    brut_price = brut_price + calculate_single_accomodation(prices_record_net, sgltmp,
                                                                            prices_record_net.meal,
                                                                            date_list, )['brut']
            else:
                net_price = net_price + calculate_single_accomodation(prices_record_net, tmp,
                                                                      prices_record_net.meal,
                                                                      date_list, ric[i]['age'], ric[i]['age'])['net']
                brut_price = brut_price + calculate_single_accomodation(prices_record_net, tmp,
                                                                        prices_record_net.meal,
                                                                        date_list, ric[i]['age'], ric[i]['age'])['brut']

            i = i + 1
            tmp = tmp.parent_id
        result = {'net': net_price, 'sale': sale_price, 'brut': brut_price}

        return result


class ReservationdetailInherit(models.Model):
    _inherit = 'rooming.list'

    p_number = fields.Char('Passport number')
    sname = fields.Char('Client surname')
    gen = fields.Selection(selection=[('mal', 'Male'), ('fem', 'Female'), ('chd', 'Child')])


class HotelsInherit(models.Model):
    _inherit = 'rooming.hotels'

    rooms = fields.Many2many('room.categories', string='Available rooms')
    meals = fields.Many2many('room.meal', string='available meals')
    allowed_companys = fields.Many2many('res.company', string='Allowed companys')
    state = fields.Many2one('res.country.state', string='State')
    country = fields.Many2one(related='state.country_id', string='Country')
    active = fields.Boolean(default=True, string='Active')
    working_state = fields.Selection(selection=[('a', 'Active'), ('h', 'Hidden')])

    @api.multi
    def change_state(self):
        if self.state == 'a':
            self.update({
                'working_state': 'h'
            })
        else:
            self.update({
                'working_state': 'a'
            })
    # todo : add regions , city , country
    # max_person = fields.Integer('Max persons')
    # min_person = fields.Integer('Min persons')i
    # enf_counted = fields.Boolean('Enf counted ?')


class InheritRooms(models.Model):
    _inherit = 'room.categories'

    # todo : on create generate accomodations

    max_person = fields.Integer('Max persons')
    min_person = fields.Integer('Min persons')
    enf_counted = fields.Boolean('Enf counted ?')
    accomodations = fields.Many2many('accomodations', string='available accomodations', readonly=True)


class RoomPricesDetail(models.Model):
    _name = 'room.prices.detail'

    # todo def set_display_name on create

    # temp = self.accomodation
    # while temp.parent_id:
    #     temp = temp.parent_id
    #     # now search the price of the base price for that meal
    # base_price_rec = self.env['room.prices.detail'].search(
    #     [('meal', '=', self.room_prices_id.contract_id.base_meal.id), ('accomodation', '=', temp.id),
    #      ('room_prices_id', '=', self.room_prices_id.id)])
    # for x in base_price_rec.room_prices_detail_dates_id:
    #     for y in self.room_prices_detail_dates_id:
    #         if x.date_range.id == y.date_range.id:
    #             y.price = (x.price / 100) * self.pprice

    room_prices_id = fields.Many2one('room.prices')
    room_prices_detail_dates_id = fields.One2many('room.prices.detail.dates', 'room_prices_detail_id', string="dates")
    ac_spos_id = fields.One2many('spo.values', 'room_prices_detail_id', string='activated spos')
    pprice = fields.Float('Percentage to apply to prices', digits=(10, 2))
    meal = fields.Many2one('room.meal', 'meal')
    accomodation = fields.Many2one('accomodations', 'accomodation')
    state = fields.Selection(selection=[('d', 'Done'), ('m', 'Missing informations')])

    def apply_value_v1(self):
        for x in self.env['room.prices.detail.dates'].search([('room_prices_detail_id', '=', self.id)]):
            x.price = self.pprice


class RoomPricesDetail(models.Model):
    _name = 'room.prices.detail.other'

    # get the base price accomodation

    # temp = self.accomodation
    # while temp.parent_id:
    #     temp = temp.parent_id
    # # now search the price of the base price for that meal
    # base_price_rec = self.env['room.prices.detail'].search(
    #     [('meal', '=', self.meal.id), ('accomodation', '=', temp.id),
    #      ('room_prices_id', '=', self.room_prices_id.id)])
    # for x in base_price_rec.room_prices_detail_dates_id:
    #     for y in self.room_prices_detail_dates_id:
    #         if x.date_range.id == y.date_range.id:
    #             y.price = (x.price / 100) * self.pprice

    room_prices_id = fields.Many2one('room.prices')
    room_prices_detail_dates_id = fields.One2many('room.prices.detail.dates.other', 'room_prices_detail_id',
                                                  string="dates")
    pprice = fields.Float('Percentage to apply to prices', digits=(10, 2))
    ac_spos_id = fields.One2many('spo.values', 'room_prices_detail_other_id', string='activated spos')
    meal = fields.Many2one('room.meal', 'meal')

    accomodation = fields.Many2one('accomodations', 'accomodation')
    state = fields.Selection(selection=[('d', 'Done'), ('m', 'Missing informations')])

    def apply_value(self):
        for x in self.env['room.prices.detail.dates.other'].search([('room_prices_detail_id', '=', self.id)]):
            x.price = self.pprice


class RoomPricesDetailDates(models.Model):
    _name = 'room.prices.detail.dates'

    date_range = fields.Many2one('room.prices.date.ranges', string="Date range")
    date_from = fields.Date('date from')
    date_to = fields.Date('date to')
    age_min = fields.Float('age min')
    age_max = fields.Float('age max')
    price = fields.Float('price', digits=(10, 3))
    is_relative = fields.Boolean('Is relative')
    room_prices_detail_id = fields.Many2one('room.prices.detail', )
    blocked = fields.Boolean('Blocked')

    def ajout_price(self, obj_copy, id_paste):
        old_record = self.env['room.prices.detail'].search([('id', '=', id_paste)])
        first_case_ids = []
        rec = False
        for s in old_record.room_prices_detail_dates_id:
            first_case_ids.append(s.id)
        search_zone_second_case = self.env['room.prices.detail.dates'].search(
            [('id', 'in', first_case_ids), ('date_from', '>=', obj_copy.date_from),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '<=', obj_copy.date_to)])
        search_zone_second_case_left = self.env['room.prices.detail.dates'].search(
            [('id', 'in', first_case_ids), ('date_from', '<', obj_copy.date_from),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '>', obj_copy.date_from)])
        search_zone_second_case_right = self.env['room.prices.detail.dates'].search(
            [('id', 'in', first_case_ids), ('date_from', '<', obj_copy.date_to),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '>', obj_copy.date_to)])
        obj_new_record = {
            'room_prices_detail_id': id_paste,
            'display_name': obj_copy.display_name,
            'date_from': obj_copy.date_from,
            'date_to': obj_copy.date_to,
            'price': obj_copy.price,
            'is_relative': obj_copy.is_relative,
            'age_min': obj_copy.age_min,
            'age_max': obj_copy.age_max
        }
        rec = self.env['room.prices.detail.dates'].create(obj_new_record)
        if search_zone_second_case_left:
            first_price_obj = {

                'date_from': search_zone_second_case_left.date_from,
                'date_to': obj_copy.date_from - timedelta(days=1),
                'price': search_zone_second_case_left.price,
                'is_relative': search_zone_second_case_left.is_relative,
                'age_min': search_zone_second_case_left.age_min,
                'age_max': search_zone_second_case_left.age_max,
                'room_prices_detail_id': id_paste,
            }
            self.env['room.prices.detail.dates'].create(first_price_obj)

        if search_zone_second_case_right:
            second_price_obj = {

                'date_from': obj_copy.date_to + timedelta(days=1),
                'date_to': search_zone_second_case_right.date_to,
                'price': search_zone_second_case_right.price,
                'is_relative': search_zone_second_case_right.is_relative,
                'age_min': search_zone_second_case_right.age_min,
                'age_max': search_zone_second_case_right.age_max,
                'room_prices_detail_id': id_paste,
            }
            self.env['room.prices.detail.dates'].create(second_price_obj)
            search_zone_second_case_right.unlink()
        search_zone_second_case_left.unlink()
        if len(search_zone_second_case) > 0:
            for x in search_zone_second_case:
                x.unlink()
        return rec


class RoomPricesDetailDates(models.Model):
    _name = 'room.prices.detail.dates.other'

    date_range = fields.Many2one('room.prices.date.ranges', string="Date range")
    date_from = fields.Date('date from')
    date_to = fields.Date('date to')
    age_min = fields.Float('age min')
    age_max = fields.Float('age max')
    price = fields.Float('price', digits=(10, 3))
    is_relative = fields.Boolean('Is relative')
    room_prices_detail_id = fields.Many2one('room.prices.detail.other', )
    blocked = fields.Boolean('Blocked')

    def ajout_price(self, obj_copy, id_paste):
        old_record = self.env['room.prices.detail.other'].search([('id', '=', id_paste)])

        first_case_ids = []
        for s in old_record.room_prices_detail_dates_id:
            first_case_ids.append(s.id)
        search_zone_second_case = self.env['room.prices.detail.dates.other'].search(
            [('id', 'in', first_case_ids), ('date_from', '>=', obj_copy.date_from),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '<=', obj_copy.date_to)])
        search_zone_second_case_left = self.env['room.prices.detail.dates.other'].search(
            [('id', 'in', first_case_ids), ('date_from', '<', obj_copy.date_from),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '>', obj_copy.date_from)])
        search_zone_second_case_right = self.env['room.prices.detail.dates.other'].search(
            [('id', 'in', first_case_ids), ('date_from', '<', obj_copy.date_to),
             ('age_max', '=', obj_copy.age_max), ('age_min', '=', obj_copy.age_min),
             ('date_to', '>', obj_copy.date_to)])
        obj_new_record = {
            'room_prices_detail_id': id_paste,
            'display_name': obj_copy.display_name,
            'date_from': obj_copy.date_from,
            'date_to': obj_copy.date_to,
            'price': obj_copy.price,
            'is_relative': obj_copy.is_relative,
            'age_min': obj_copy.age_min,
            'age_max': obj_copy.age_max
        }
        rec = self.env['room.prices.detail.dates.other'].create(obj_new_record)
        if search_zone_second_case_left:
            first_price_obj = {

                'date_from': search_zone_second_case_left.date_from,
                'date_to': obj_copy.date_from - timedelta(days=1),
                'price': search_zone_second_case_left.price,
                'is_relative': search_zone_second_case_left.is_relative,
                'age_min': search_zone_second_case_left.age_min,
                'age_max': search_zone_second_case_left.age_max,
                'room_prices_detail_id': id_paste,
            }
            self.env['room.prices.detail.dates.other'].create(first_price_obj)

        if search_zone_second_case_right:
            second_price_obj = {

                'date_from': obj_copy.date_to + timedelta(days=1),
                'date_to': search_zone_second_case_right.date_to,
                'price': search_zone_second_case_right.price,
                'is_relative': search_zone_second_case_right.is_relative,
                'age_min': search_zone_second_case_right.age_min,
                'age_max': search_zone_second_case_right.age_max,
                'room_prices_detail_id': id_paste,
            }
            self.env['room.prices.detail.dates.other'].create(second_price_obj)
            search_zone_second_case_right.unlink()
        search_zone_second_case_left.unlink()
        if len(search_zone_second_case) > 0:
            for x in search_zone_second_case:
                x.unlink()
        return rec


class RoomPricesDetail(models.Model):
    _name = 'room.prices.detail.transient'

    # todo def set_display_name on create

    t_id = fields.Many2one('room.prices.transient')
    date_range = fields.Many2one('room.prices.date.ranges', string="Date range")
    price = fields.Float('price', digits=(10, 3))
    spo = fields.Many2many('rooming.rule', string='spo available')


class RoomPricesDetailsgl(models.Model):
    _name = 'room.prices.detail.sgl.transient'

    # todo def set_display_name on create

    t_id_sgl = fields.Many2one('room.prices.transient')
    date_range = fields.Many2one('room.prices.date.ranges', string="Date range")
    price = fields.Float('price', digits=(10, 3))
    spo = fields.Many2many('rooming.rule', string='spo available')


class RoomPrices(models.Model):
    _name = 'room.prices'
    _rec_name = 'room'

    contract_id = fields.Many2one('contract.contract')
    room = fields.Many2one('room.categories', string='Room')
    accomodations = fields.Many2many('accomodations', string='availabe accomodations')
    meals = fields.Many2many('room.meal', string='avaible meals')
    currency_id = fields.Many2one('res.currency', string='currency')
    room_qty = fields.Integer('room quantities')
    room_places = fields.Integer('room places')
    is_hostel = fields.Boolean('is Hostel')
    min = fields.Integer('min')
    max = fields.Integer('max')
    base_prices = fields.One2many('room.prices.detail', 'room_prices_id', string='Base prices')
    other_prices = fields.One2many('room.prices.detail.other', 'room_prices_id', string='Other prices')
    change_url = fields.Char('Edit prices in matrix')
    prices_type = fields.Selection(selection=[('s', 'Sale'), ('n', 'Net')])
    can_generate_finals_net = fields.Boolean('Can generate Net Final prices')
    can_generate_finals_sale = fields.Boolean('Can generate Sale Final prices')
    enf_counted = fields.Boolean('enf counted ?')

    # todo def check for alerts


class RoomPricesTransient(models.Model):
    _name = 'room.prices.transient'

    # todo def generate base/other prices for accomodations
    def sandgop(self):
        # create the space in prices and then go for entering the base prices , now if we checked fill other accom
        # just do it ^_^
        # 1) create the room prices object

        obj = {
            'contract_id': self.contract_id.id,
            'room': self.room.id,
            'display_name': str(self.room.name),
            'currency_id': self.currency_id.id
        }
        room_record = self.env['room.prices'].create(obj)
        room_record.accomodations = self.av_acc

        room_record.change_url = '/matrix/' + str(self.contract_id.id) + '/' + str(room_record.id)
        for x in self.env['contract.contract'].search([('id', '=', self.contract_id.id)]).meals:
            obj1 = {
                'room_prices_id': room_record.id,
                'display_name': self.room.name,
                'meal': x.id,
                'accomodation': self.accomodation.id,
                'room_prices_detail_dates_id': []
            }
            base_price_detail = self.env['room.prices.detail'].create(obj1)

            for y in self.base_prices:
                obj2 = {
                    'date_range': y.date_range.id,
                    'price': y.price,
                    'room_prices_detail_id': base_price_detail.id,
                    'display_name': str(y.date_range.display_name) + ' - ' + str(y.price)
                }
                base_price_detail_dates = self.env['room.prices.detail.dates'].create(obj2)

        if self.sgl:
            # objsgl = {
            #     'room_prices_id': room_record.id,
            #     'display_name': self.room.name,
            #     'meal': self.meal.id,
            #     'accomodation': self.env['accomodations'].search([('code', '=', 'SGL')]).id,
            #     'room_prices_detail_dates_id': []
            # }
            # base_price_detail_sgl = self.env['room.prices.detail'].create(objsgl)
            # for x in self.sgl_prices:
            #     obj2 = {
            #         'date_range': x.date_range.id,
            #         'price': x.price,
            #         'room_prices_detail_id': base_price_detail_sgl.id,
            #         'display_name': str(x.date_range.display_name) + ' - ' + str(x.price)
            #     }
            #     base_price_detail_dates = self.env['room.prices.detail.dates'].create(obj2)

            for x in self.contract_id.meals:
                # if x.id == self.meal.id:
                #     pass
                # else:
                obj1 = {
                    'room_prices_id': room_record.id,
                    'display_name': self.room.name,
                    'meal': x.id,
                    'accomodation': self.env['accomodations'].search([('code', '=', 'SGL')]).id,
                    'room_prices_detail_dates_id': []
                }
                base_price_detail = self.env['room.prices.detail'].create(obj1)

                for y in self.sgl_prices:
                    obj2 = {
                        'date_range': y.date_range.id,
                        'price': y.price,
                        'room_prices_detail_id': base_price_detail.id,
                        'display_name': str(y.date_range.display_name) + ' - ' + str(y.price)
                    }
                    base_price_detail_dates = self.env['room.prices.detail.dates'].create(obj2)

        if True:
            list_base_price_detail = []
            for x1 in self.av_acc:
                for y in self.env['contract.contract'].search([('id', '=', self.contract_id.id)]).meals:
                    if x1.parent_id and x1.visible_in_prices:
                        obj3 = {
                            'room_prices_id': room_record.id,
                            'display_name': self.room.name,
                            'accomodation': x1.id,
                            'meal': y.id,
                            'room_prices_detail_dates_id': []
                        }
                        base_price_detail_other = self.env['room.prices.detail.other'].create(obj3)
                        list_base_price_detail.append(base_price_detail_other.id)
            for z in list_base_price_detail:
                for y1 in self.env['room.prices.date.ranges'].search([('contract_id', '=', self.contract_id.id)]):
                    obj4 = {
                        'date_range': y1.id,
                        'price': 0,
                        'room_prices_detail_id': z,
                        'display_name': ''

                    }
                    base_price_detail_dates_other = self.env['room.prices.detail.dates.other'].create(obj4)
        return True

    def _set_contract(self):
        return self._context.get('active_ids')[0]

    # todo def set_display_name on create

    def _get_domain(self):
        try:
            contract = self._context.get('active_ids')[0]
            contract_rec = self.env['contract.contract'].search([('id', '=', contract)]).rooms
            listo = []

            for x in contract_rec:
                listo.append(x.id)
            return [('id', 'in', listo)]
        except:
            return [('id', '=', [1])]

    def _init_base_prices(self):
        # get date ranges
        date_r_list = self.env['contract.contract'].search(
            [('id', '=', self._context.get('active_ids')[0])]).date_ranges
        l = []
        for x in date_r_list:
            obj = {
                'date_range': x.id,
                'price': 0,
                'spo': []
            }
            l.append(obj)
        return l

    def _set_meal(self):
        contract = self._context.get('active_ids')[0]
        contract_rec = self.env['contract.contract'].search([('id', '=', contract)])
        return contract_rec.base_meal.id

    def _set_acc(self):
        contract = self._context.get('active_ids')[0]
        contract_rec = self.env['contract.contract'].search([('id', '=', contract)])
        return contract_rec.base_accomodation.id

    # @api.onchange('av_acc')
    # def change_acc(self):
    #     l = []
    #     fl = []
    #     for x in self.av_acc:
    #         l.append(x)
    #         fl.append(x.id)
    #     if len(l) > 0:
    #         for x in l:
    #             tmp = x
    #             while tmp.parent_id:
    #                 if tmp.parent_id not in self.av_acc:
    #                     fl.append(tmp.parent_id.id)
    #                 tmp = tmp.parent_id
    #     self.av_acc = fl

    @api.onchange('max_person', 'min_person')
    def set_accomodations(self):
        accomodations = []
        for m in range(1, self.max_person + 1):
            for n in range(0, self.max_person):
                for k in range(0, self.max_person):
                    if m + n + k <= self.max_person and m + n + k >= self.min_person:
                        for x in self.env['accomodations'].search(
                                [('adult', '=', m), ('child', '=', n), ('inf', '=', k),
                                 ('visible_in_prices', '=', True)]):
                            accomodations.append(x.id)

        self.av_acc = accomodations

    contract_id = fields.Many2one('contract.contract', default=_set_contract, readonly=True)
    room = fields.Many2one('room.categories', string='Room', domain=_get_domain)
    max_person = fields.Integer('Max persons')
    min_person = fields.Integer('Min persons')
    enf_counted = fields.Boolean('Enf counted ?')
    currency_id = fields.Many2one('res.currency', string='currency')
    ac_spos = fields.Many2many('rooming.rule', string='activated spos')
    meal = fields.Many2one('room.meal', string='Base Meal', default=_set_meal, readonly=True)
    av_acc = fields.Many2many('accomodations', string='availabe accomodations')
    accomodation = fields.Many2one('accomodations', string='Base accomodation', default=_set_acc, readonly=True)
    base_prices = fields.One2many('room.prices.detail.transient', 't_id', string='Base prices',
                                  default=_init_base_prices)
    sgl_prices = fields.One2many('room.prices.detail.sgl.transient', 't_id_sgl', string='SGL prices',
                                 default=_init_base_prices)
    gop = fields.Boolean('Generate other accomodations prices')
    sgl = fields.Boolean('Generate SGL accomodations prices')


class ContractInherit(models.Model):
    _inherit = 'contract.contract'

    @api.onchange('hotel')
    def _set_meals(self):
        self.meals = []
        if self.hotel:
            if self.hotel.meals:
                self.meals = self.hotel.meals

    @api.onchange('hotel')
    def _set_rooms(self):
        self.rooms = []
        if self.hotel:
            if self.hotel.rooms:
                self.rooms = self.hotel.rooms

    # def _get_domain2(self):
    #
    #     try:
    #
    #         contract_rec = self.env['room.prices.date.ranges'].search([('contract_id', '=', self.id)])
    #         listo = []
    #
    #         for x in contract_rec:
    #             listo.append(x.id)
    #         return [('id', 'in', listo)]
    #     except:
    #         return [('id', '=', [1])]

    # todo def check for alerts

    base_meal = fields.Many2one('room.meal', 'base meal')
    base_accomodation = fields.Many2one('accomodations', 'base accomodation')
    meals = fields.Many2many('room.meal', string='available meals')
    rooms = fields.Many2many('room.categories', string='available rooms')
    room_prices = fields.One2many('room.prices', 'contract_id', string="room_prices")
    date_ranges = fields.One2many('room.prices.date.ranges', 'contract_id', string="Date ranges")
    cancellation_release = fields.One2many('cancellation.release.policy', 'contract_id',
                                           string="cancellation and release policy")


class DatesRanges(models.Model):
    _name = 'room.prices.date.ranges'
    _rec_name = 'dn'
    _order = 'frome'

    frome = fields.Date('Date from')
    to = fields.Date('Date to')
    dn = fields.Char('Display name')
    contract_id = fields.Many2one('contract.contract')

    @api.model
    def create(self, vals):
        record = super(DatesRanges, self).create(vals)
        record['dn'] = str(record['frome']) + " // " + str(record['to'])
        return record


class Accomodations(models.Model):
    _name = 'accomodations'
    _rec_name = 'code'
    _order = "sequence Desc"

    code = fields.Char('Code')
    codef = fields.Char('Code Final')
    adult = fields.Integer('Adult')
    child = fields.Integer('Child')
    inf = fields.Integer('Infant')
    parent_id = fields.Many2one('accomodations', string="parent id")
    visible_in_prices = fields.Boolean(string="visible_in_prices matrix")
    is_base = fields.Boolean('is base price')
    is_sub_accomodation = fields.Boolean('Is sub accomodation')
    sequence = fields.Integer('sequence')


class AcoomodationPrices(models.Model):
    _name = 'accomodation.prices'
    _rec_name = 'accomodation'

    accomodation = fields.Many2one('accomodations', 'accomodation')
    prix = fields.Float('price')


class CancellationReleasePolicy(models.Model):
    _name = 'cancellation.release.policy'
    _rec_name = 'date_range'

    date_range = fields.Many2one('room.prices.date.ranges', string='date range')
    cancellation = fields.Integer('cancellation')
    release = fields.Integer('release')
    contract_id = fields.Many2one('contract.contract')


class Paystay(models.Model):
    _name = 'spo.paystay'

    stay = fields.Integer('stay')
    pay = fields.Integer('pay')
    spo_values_id = fields.Many2one('spo.values')


class SpoConfig(models.Model):
    _name = 'spo.configuration'
    _rec_name = 'name_spo'

    name_spo = fields.Char('name Spo')
    period_chekin = fields.Boolean('period chekin')
    period_chekout = fields.Boolean('period chekout')
    period_date_creation = fields.Boolean('period date creation')
    age = fields.Boolean('age')
    night_number = fields.Boolean('night number')
    date_stay = fields.Boolean('day stay')
    pay_stay = fields.Boolean('pay stay')
    days_applicability = fields.Selection(selection=[('n', 'Per night'), ('p', 'Period')])


class SpoValues(models.Model):
    _name = 'spo.values'

    spo_config_id = fields.Many2one('spo.configuration', string='spo category')
    chekin_from = fields.Date('chekin from')
    chekin_to = fields.Date('chekin to')
    chekout_from = fields.Date('chekout from')
    chekout_to = fields.Date('chekout to')
    date_creation_from = fields.Datetime('date creation from')
    date_creation_to = fields.Datetime('date creation to')
    age_from = fields.Integer('age from')
    age_to = fields.Integer('age to')
    night_number_from = fields.Integer('night number from')
    night_number_to = fields.Integer('night number to')
    day_stay_from = fields.Date('day stay from')
    day_stay_to = fields.Date('day stay to')
    pay_stay = fields.One2many('spo.paystay', 'spo_values_id', string='pay stay')
    room_prices_detail_id = fields.Many2one('room.prices.detail', )
    room_prices_detail_other_id = fields.Many2one('room.prices.detail.other', )
    is_relative = fields.Boolean('is relative')
    spo_value = fields.Float('value spo')
    spo_type = fields.Selection(selection=[('moins', 'réduction'), ('plus', 'supplément')])
    blocked_spo = fields.Boolean('is blocked')
    not_commulable_with = fields.Many2many('spo.values', column1='val1', column2='val2', relation='values_values_rel',
                                           string='not_commulablbe_with')
    one_time_payement = fields.Boolean('One time payement')
    sequence = fields.Integer('sequence')
    showed_name = fields.Char('Showed name')
    hotel_id = fields.Many2one('rooming.hotels', string='Hotel')

    @api.model
    def create(self, vals_list):
        if vals_list.get('room_prices_detail_id'):
            room_price = self.env['room.prices.detail'].search(
                [('id', '=', vals_list['room_prices_detail_id'])]).room_prices_id.id
        if vals_list.get('room_prices_detail_other_id'):
            room_price = self.env['room.prices.detail.other'].search(
                [('id', '=', vals_list['room_prices_detail_other_id'])]).room_prices_id.id
        contrat_id = self.env['room.prices'].search([('id', '=', room_price)]).contract_id.id
        vals_list['hotel_id'] = self.env['contract.contract'].search([('id', '=', contrat_id)]).hotel.id
        rec = super(SpoValues, self).create(vals_list)
        return rec

    def ajouter_hotel(self):
        for x in self.env['spo.values'].search([]):
            if x.room_prices_detail_id:
                room_price = self.env['room.prices.detail'].search(
                    [('id', '=', x.room_prices_detail_id.id)]).room_prices_id.id
            if x.room_prices_detail_other_id:
                room_price = self.env['room.prices.detail.other'].search(
                    [('id', '=', x.room_prices_detail_other_id.id)]).room_prices_id.id
            contrat_id = self.env['room.prices'].search([('id', '=', room_price)]).contract_id.id
            x.update({'hotel_id': self.env['contract.contract'].search([('id', '=', contrat_id)]).hotel.id})

    def edit_showedname(self):
        for x in self.env['spo.values'].search([]):
            tmp = x.spo_config_id.name_spo + ' '

            if x.chekin_from:
                tmp = tmp + 'chIN: ' + datetime.strftime(x.chekin_from, '%m.%d.%y')
                tmp = tmp + ' '

            if x.chekout_from:
                tmp = tmp + 'chOUT: ' + datetime.strftime(x.chekout_from, '%m.%d.%y')
                tmp = tmp + ' '

            if x.date_creation_from:
                tmp = tmp + 'cr: ' + datetime.strftime(x.date_creation_from, '%m.%d.%yT%H:%M')
                tmp = tmp + ' '

            if x.day_stay_from:
                tmp = tmp + 'pr: ' + datetime.strftime(x.day_stay_from, '%m.%d.%y')
                tmp = tmp + ' '

            if x.age_from:
                tmp = tmp + 'age: ' + str(x.age_from)
                tmp = tmp + ' '

            if x.night_number_from:
                tmp = tmp + 'night: ' + str(x.night_number_from)
                tmp = tmp + ' '

            if x.spo_value:
                tmp = tmp + ' ' + str(x.spo_value)
                tmp = tmp + ' '

            if x.is_relative:
                tmp = tmp + '% '
            x.update({'showed_name': tmp})
