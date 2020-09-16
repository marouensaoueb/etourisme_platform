# -*- coding: utf-8 -*-

import json
from datetime import datetime

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug.urls import url_decode, iri_to_uri

import odoo
from odoo.addons.web.controllers.main import Home
from odoo import http
from odoo.http import request
from odoo.tools.translate import _

PPG = 20  # Products Per Page
PPR = 4  # Products Per Row


def redirect_with_hash(*args, **kw):
    """
        .. deprecated:: 8.0

        Use the ``http.redirect_with_hash()`` function instead.
    """
    return http.redirect_with_hash(*args, **kw)


def abort_and_redirect(url):
    r = request.httprequest
    response = werkzeug.utils.redirect(url, 302)
    response = r.app.get_response(r, response, explicit_session=False)
    werkzeug.exceptions.abort(response)


db_monodb = http.db_monodb


def ensure_db(redirect='/web/database/selector'):
    # This helper should be used in web client auth="none" routes
    # if those routes needs a db to work with.
    # If the heuristics does not find any database, then the users will be
    # redirected to db selector or any url specified by `redirect` argument.
    # If the db is taken out of a query parameter, it will be checked against
    # `http.db_filter()` in order to ensure it's legit and thus avoid db
    # forgering that could lead to xss attacks.
    db = request.params.get('db') and request.params.get('db').strip()

    # Ensure db is legit
    if db and db not in http.db_filter([db]):
        db = None

    if db and not request.session.db:
        # User asked a specific database on a new session.
        # That mean the nodb router has been used to find the route
        # Depending on installed module in the database, the rendering of the page
        # may depend on data injected by the database route dispatcher.
        # Thus, we redirect the user to the same page but with the session cookie set.
        # This will force using the database route dispatcher...
        r = request.httprequest
        url_redirect = werkzeug.urls.url_parse(r.base_url)
        if r.query_string:
            # in P3, request.query_string is bytes, the rest is text, can't mix them
            query_string = iri_to_uri(r.query_string)
            url_redirect = url_redirect.replace(query=query_string)
        request.session.db = db
        abort_and_redirect(url_redirect)

    # if db not provided, use the session one
    if not db and request.session.db and http.db_filter([request.session.db]):
        db = request.session.db

    # if no database provided and no database in session, use monodb
    if not db:
        db = db_monodb(request.httprequest)

    # if no db can be found til here, send to the database selector
    # the database selector will redirect to database manager if needed
    if not db:
        werkzeug.exceptions.abort(werkzeug.utils.redirect(redirect, 303))

    # always switch the session to the computed db
    if db != request.session.db:
        request.session.logout()
        abort_and_redirect(request.httprequest.url)

    request.session.db = db


class Home(Home):

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        return http.local_redirect('/home', query=request.params, keep_hash=True)

    @http.route('/web/login', type='http', auth="none", sitemap=False)
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, request.params['login'],
                                                   request.params['password'])
                request.params['login_success'] = True
                return http.redirect_with_hash(self._login_redirect(uid, redirect='/home'))
            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # otherwise no real way to test debug mode in template as ?debug =>
        # values['debug'] = '' but that's also the fallback value when
        # missing variables in qweb
        if 'debug' in values:
            values['debug'] = True

        values['page_title'] = 'Login'

        response = request.render('product_price_computation_carthage_group.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @http.route('/home', type='http', methods=['GET'], auth="user", website=True)
    def home(self, choose_partner=False, **kw):
        company_id = False
        try:
            company_id = request.session['company_id']

        except:
            pass
        if choose_partner:
            company_id = False
            return http.request.render('product_price_computation_carthage_group.index',
                                       {'page_title': 'Home', 'company_id': company_id})

        if company_id is False:
            return http.request.render('product_price_computation_carthage_group.index',
                                       {'page_title': 'Home', 'company_id': company_id})
        else:
            return request.redirect('/choose_service')

    @http.route('/home', type='http', methods=['POST'], auth="user", website=True)
    def homepost(self, **kw):
        company_id = False
        try:
            company_id = kw['partner_selection']
            request.session['company_id'] = company_id
        except:
            pass

        if company_id is False:
            return http.request.render('product_price_computation_carthage_group.index',
                                       {'page_title': 'Home', 'company_id': company_id})
        else:
            return request.redirect('/choose_service')

    @http.route('/choose_service', type='http', methods=['GET'], auth="user", website=True)
    def choose_service(self):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/home')
        else:
            return http.request.render('product_price_computation_carthage_group.choose_service',
                                       {'page_title': 'Choose service', 'company_id': company_id})

    @http.route('/prices_contracts', type='http', methods=['GET'], auth="user", website=True)
    def prices_ontracts(self):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/choose_service')
        else:
            return http.request.render('product_price_computation_carthage_group.choose_hotel',
                                       {'page_title': 'Choose hotel', 'company_id': company_id})

    @http.route(['''/reservations''', '''/reservations/page/<int:page>''', ], type='http', methods=['GET'], auth="user",
                website=True)
    def reservations(self, page=0, ppg=False, search=False, sense=False, order=False, **get):
        company_id = False
        domain = []
        searcht = False
        order_by = 'chekin Asc'
        if order:
            if order == '1':
                order_by = 'reservation_number'
            if order == '2':
                order_by = 'chekin'
            if order == '3':
                order_by = 'checkout'
            if order == '4':
                order_by = 'night_number'
            if order == '5':
                order_by = 'brut'
            if order == '6':
                order_by = 'net'
            if order == '7':
                order_by = 'state'
        if sense:
            if sense == '0':
                if 'Asc' in order_by:
                    pass
                elif 'Desc' in order_by:
                    order_by.replace('Dsc', 'Asc')
                else:
                    order_by = order_by + ' ' + 'Asc'
            if sense == '1':
                if 'Desc' in order_by:
                    pass
                elif 'Asc' in order_by:
                    order_by.replace('Asc', 'Desc')
                else:
                    order_by = order_by + ' ' + 'Desc'

        if not search:
            pass
        else:
            pass
            searcht = json.loads(search)
            if searcht['country'] != '0':
                pass
            if searcht['city'] != '0':
                pass
            if searcht['to_id'] != '0':
                domain.append(('touroperator_id', '=', int(searcht['to_id'])))
            if searcht['hotel_id'] != '0':
                domain.append(('hotel_id', '=', int(searcht['hotel_id'])))
            if searcht['check_in_f'] != '':
                domain.append(('chekin', '>=', searcht['check_in_f']))
            if searcht['check_in_t'] != '':
                domain.append(('chekin', '<=', searcht['check_in_t']))
            if searcht['check_out_f'] != '':
                domain.append(('checkout', '>=', searcht['check_out_f']))
            if searcht['check_out_t'] != '':
                domain.append(('checkout', '<=', searcht['check_out_t']))
            if searcht['meal'] != '0':
                domain.append(('meal', '=', int(searcht['meal'])))
            if searcht['room_categ'] != '0':
                domain.append(('room_category', '=', int(searcht['room_categ'])))
            if searcht['accomodation'] != '0':
                domain.append(('accomodation', '=', int(searcht['accomodation'])))
            if searcht['reservation_number'] != '':
                domain.append(('reservation_number', '=', searcht['reservation_number']))
            if searcht['res_to_ref'] != '':
                domain.append(('res_to_ref', '=', searcht['res_to_ref']))
            if searcht['note'] != '':
                domain.append(('note', 'like', searcht['note']))

        if ppg:
            try:
                ppg = int(json.loads(ppg)[1]) - int(json.loads(ppg)[0])
            except:
                try:
                    ppg = int(ppg)
                except:
                    ppg = PPG
            get["ppg"] = ppg
        else:
            ppg = PPG
        try:
            company_id = request.session['company_id']
        except:
            pass
        offset = 0
        if company_id is False:
            return request.redirect('/choose_service')
        else:
            url = '/reservations'

            allowed_companys = []
            if search is not False:
                search = {
                    'search': search
                }
            else:
                search = get
            if order is not False:
                search.update({'order': order})
            if sense is not False:
                search.update({'sense': sense})
            for x in request.env['res.users'].search([('id', '=', request.uid)]).company_ids:
                allowed_companys.append(x.id)
            domain.append(('company_id', 'in', allowed_companys))
            reservations_count = request.env['ctm.reservation.list'].search_count(domain)
            pager = request.website.pager(url=url, total=reservations_count, page=page, step=ppg, scope=7,
                                          url_args=search)

            try:
                offset = int(json.loads(ppg)[0])
            except:
                offset = pager['offset']
            reservations = request.env['ctm.reservation.list'].search(domain, limit=ppg, offset=offset,
                                                                      order=order_by)


            reservations.sorted(key='hotel_id')
            return http.request.render('product_price_computation_carthage_group.reservations_manager',
                                       {'page_title': 'Reservations management',
                                        'company_id': company_id,
                                        'pager': pager,
                                        'reservations': reservations,
                                        'reservations_count': reservations_count,
                                        'allowed_companys': allowed_companys,
                                        'ppg': ppg,
                                        'search': searcht,
                                        'order': int(order),
                                        'sense': int(sense)
                                        })

    @http.route('/choose_product_price', type='http', methods=['GET'], auth="user", website=True)
    def choose_product_price(self):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/choose_service')
        else:
            return http.request.render('product_price_computation_carthage_group.choose_product_price',
                                       {'page_title': 'Choose price product', 'company_id': company_id})

    @http.route('/choose_product_reservation', type='http', methods=['GET'], auth="user", website=True)
    def choose_product_reservation(self):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/choose_service')
        else:
            return http.request.render('product_price_computation_carthage_group.choose_product_reservation',
                                       {'page_title': 'Choose reservation product', 'company_id': company_id})

    @http.route('/reservations/create', type='http', methods=['GET'], auth="user", website=True)
    def create_res(self):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/choose_service')
        else:
            allowed_companys = []
            for x in request.env['res.users'].search([('id', '=', request.uid)]).company_ids:
                allowed_companys.append(x.id)
            return http.request.render('product_price_computation_carthage_group.reservations_create',
                                       {'page_title': 'Create reservation', 'company_id': company_id,
                                        'allowed_companys': allowed_companys, })

    @http.route('/reservations/creation/', type='http', methods=['POST'], auth="user", website=True)
    def new_reservation(self, **kw):
        reservation = json.loads(kw['reservation'])
        list_client = reservation['list_clients']
        touroperator_req = request.env['tour.operator'].search([('id', '=', int(reservation['tour_operator']))])
        seq_to = touroperator_req.sequence_config.next_by_code(touroperator_req.name)
        obj_reservation = {
            'reservation_number': seq_to,
            'chekin': datetime.strptime(reservation['checkin'], '%Y-%m-%d').date(),
            'checkout': datetime.strptime(reservation['checkout'], '%Y-%m-%d').date(),
            'hotel_id': int(reservation['hotel']),
            'touroperator_id': int(reservation['tour_operator']),
            'company_id': int(reservation['company']),
            'note': reservation['note'],
            # 'creation_date': datetime.strptime(reservation['creation_date'], '%Y-%m-%d').date(),
            'room_category': int(reservation['room_category']),
            'accomodation': reservation['accomodation'],
            'res_to_ref': reservation['tour_operator_ref'],
            # 's_date': datetime.strptime(reservation['sending_date'], '%Y-%m-%d').date(),
            'meal': int(reservation['meal']),
            'creation_date': datetime.now(),
            'night_number': reservation['night_number']
        }
        reservation_id = request.env['ctm.reservation.list'].sudo().create(obj_reservation)
        for x in list_client:
            obj_room = {
                'hotel': reservation_id.hotel_id.id,
                'tour_operator': reservation_id.touroperator_id.id,
                'num_reser': reservation_id.reservation_number,
                'client_name': x['name'],
                'sname': x['surname'],
                'datenaiss': datetime.strptime(x['birthday'], '%Y-%m-%d').date(),
                'age': float(x['age']),
                'gen': x['gender'],
                'p_number': x['passeport_number'],
                'reservation_list_id': reservation_id.id
            }
            request.env['rooming.list'].sudo().create(obj_room)

        return request.redirect('/reservations')

    @http.route('/reservations/show/<model("ctm.reservation.list"):reservation>', type='http', methods=['GET'],
                auth="user", website=True)
    def reservation_show(self, reservation, **get):
        company_id = False
        try:
            company_id = request.session['company_id']
        except:
            pass

        if company_id is False:
            return request.redirect('/choose_service')
        else:
            allowed_companys = []
            for x in request.env['res.users'].search([('id', '=', request.uid)]).company_ids:
                allowed_companys.append(x.id)
        return http.request.render('product_price_computation_carthage_group.reservations_show',
                                   {'page_title': reservation.reservation_number, 'company_id': company_id,
                                    'allowed_companys': allowed_companys, 'reservation': reservation})

    @http.route('/reservations/delete', type='http', methods=['GET'],
                auth="user", website=True)
    def delete_reservation(self, id=0, **get):
        res_req = request.env['ctm.reservation.list'].search([('id', '=', id)])
        res_req.unlink()
        return request.redirect('/reservations')
