# -*- coding: utf-8 -*-

import datetime
import logging

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ito_server_ip = fields.Char('ITO SERVER IP', default="41.226.13.69,8099")
    ito_server_port = fields.Integer('ITO SERVER PORT')
    ito_server_login = fields.Char('ITO SERVER LOGIN', default="sa")
    ito_server_password = fields.Char('PASSWORD', default="TnCTMdbSA2018")


class WizardGetRoomingList(models.TransientModel):
    _name = "rooming.list.get"
    _description = "Rooming list and sale list importation from ito server"

    @api.model
    def get_server_ip(self):
        return self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_ip

    ito_server_ip = fields.Char('ITO SERVER IP', readonly=True)
    reservation_number = fields.Char('Reservation number')
    date_start = fields.Date('Start')
    date_end = fields.Date('End')
    creation_date_start = fields.Date('Start')
    creation_date_end = fields.Date('End')
    exursion_date = fields.Date('Excursion_date', default=datetime.datetime.today().date())
    hotel = fields.Many2many('rooming.hotels', string="Hotel")
    tickets_from = fields.Integer('Ticket from')
    tickets_to = fields.Integer('Tickets to ')
    tour_operator = fields.Many2many('tour.operator', string="Tour operator")


    @api.multi
    def synchronize_partiel(self):
        # get the tickets
        import pyodbc
        server_url = "192.168.1.241"
        login = "sa"
        password = "TnCTMdbSA2018"
        check_second_driver = False
        try:
            cnx1 = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
        except:
            check_second_driver = True
        if check_second_driver:
            cnx1 = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
        strx = '''
                    SELECT
                    dl_key,
                    DL_Date		 as 'Excursion date', -- wp
                    ( SELECT SL_Name FROM ServiceList WHERE SL_Key = DL_Code )		 as 'Excursion_name', --wp
                    RTRIM(LTRIM(TU_Name)) as 'surname',
                    RTRIM(LTRIM(TU_FirstName))                        as 'Name',
                    TU_BIRTHDAY,
                    tu_key,
                    DG_PRKey        as 'Tour operator', --wp
                    dg_code as ' Booking number ', --wp
                    DL_VoucherNumber as 'Ticket number', --wp
                    (select GU_NAME from GUIDE where GU_KEY = DL_SUBCODE2) as 'guide name', --wp
                    DL_Price * dbo.zf_GetExchangeRate( DL_PriceCurrency, 'USD' , DL_Date, DL_PRKey ) as 'Selling price', --wp
                    (select PR_KEY from Partners where PR_KEY = DL_SUBCODE1)                              as Hotel,
                    ( SELECT CT_Name FROM CityDictionary WHERE CT_Key = DL_SubCode3 )	 as 'CityName', --wp
                    (select RG_name from REGION where RG_KEY = 
                    (select ct_rgkey from CITYDICTIONARY where CT_KEY = DL_SubCode3)) as ' region ', --wp
                    TU_RoomNumber									as 'R.N.', --wp
                    DL_CREATEDATE	,
                    CASE WHEN DL_STKey = 0 THEN 'New'
                               WHEN DL_STKey = 1 THEN 'Waiting confirmation'
                               WHEN DL_STKey = 2 THEN 'cnf'
                               WHEN DL_STKey = 3 THEN 'cncl'
                               WHEN DL_STKey = 4 THEN 'Not confirmed'
                               WHEN DL_STKey = 5 THEN 'cnf'
                               ELSE 'Complementary' END                    as StatusName
                    FROM	DogovorList, DOGOVOR , Turist T,
                    TuristService
                    WHERE
                    DG_KEY = DL_DGKEY 
                    and DL_STKey IN (2,5,3) and
                    DL_SVKey = 4 
                    AND     TU_Key = TU_TUKey
                    AND     DL_Key = TU_DLKey 
                    and DL_VoucherNumber >= {0}
                    and DL_VoucherNumber <= {1}
					and DL_Date >= '2019-01-01'

        '''.format(self.tickets_from, self.tickets_to)
        # find them in extra and correct them
        cursor1.execute(strx)
        for row in cursor1:
            l = self.env['excursion.extra'].sudo().search(
                [('ticket_number', '=', row[9]), ('tu_key', '=', row[6]), ('state', '=', row[17])])
            if len(l) == 0:
                # create em
                adulte = 0
                state = row[17]
                enfant = 0
                inf = 0
                birthday = ''
                dat = str(row[1])
                crdat = str(row[16])
                excursion_id = self.env['excursion.excursion'].sudo().search([('name', '=', row[2])]).id
                datenaiss = row[5] or ''
                # traittement de l'age'
                try:
                    booking_number = str(row[8])
                    booking_number_rec = self.env['ctm.reservation.list'].sudo().search(
                        [('reservation_number', '=', booking_number)])[0]
                    booking_number_arrival_date = booking_number_rec.chekin
                except:
                    booking_number = False
                if datenaiss == '':
                    if str(row[3]) == "Adult1":
                        adulte = adulte + 1
                    elif str(row[3]) == "Adult2":
                        adulte = adulte + 1
                    elif str(row[3]) == "Adult3":
                        adulte = adulte + 1
                    elif str(row[3]) == "Child1":
                        enfant = enfant + 1
                    elif str(row[3]) == "Child2":
                        enfant = enfant + 1
                    elif str(row[3]) == "Child3":
                        enfant = enfant + 1
                    elif str(row[3]) == "Infant1":
                        inf = inf + 1
                    elif str(row[3]) == "Infant2":
                        inf = inf + 1
                    elif str(row[3]) == "Infant3":
                        inf = inf + 1
                    else:
                        adulte = adulte + 1
                else:
                    if booking_number_rec:
                        years = relativedelta(booking_number_arrival_date,
                                              row[5]).years
                        months = relativedelta(booking_number_arrival_date,
                                               row[5]).months
                    else:
                        years = relativedelta(row[1],
                                              row[5]).years
                        months = relativedelta(row[1],
                                               row[5]).months

                    age = years + (months / 12)
                    bebemaxage = self.env['excursion.excursion'].search([('name', '=', row[2])]).bebemaxage
                    enfmaxage = self.env['excursion.excursion'].search([('name', '=', row[2])]).enfmaxage
                    if age >= enfmaxage:
                        adulte = adulte + 1
                    elif bebemaxage <= age < enfmaxage:
                        enfant = enfant + 1
                    elif age < bebemaxage:
                        inf = inf + 1
                tour_operateur = self.env['tour.operator'].sudo().search([('ito_id', '=', int(row[7]))])[0].id

                ticket_number = row[9]
                vendeur_id = self.env['excursion.guide'].sudo().search([('name', '=', row[10])]).id or False
                city_key = self.env['excursion.pointdepart'].sudo().search([('name', '=', row[13])]).id or False
                try:
                    selling_price = float(row[11])
                except:
                    selling_price = 0.0
                region_id = self.env['excursion.emplacement'].sudo().search([('name', '=', row[14])])[0].id or False
                paid_sum = selling_price
                hotel_id = self.env['rooming.hotels'].sudo().search([('hotel_id', '=', int(row[12]))])[0].id
                room_nbr = row[15]
                # look for currency
                tarif = self.env['excursion.tarif.region'].sudo().search(
                    [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
                currency_id = tarif.currency_id.id or self.env['excursion.excursion'].sudo().search(
                    [('name', '=', row[2])]).ito_curency.id
                self.env['excursion.extra'].sudo().create(
                    {
                        'dat': dat,
                        'excursion_id': excursion_id,
                        'adulte': adulte,
                        'enfant': enfant,
                        'inf': inf,
                        'tour_operateur': tour_operateur,
                        'booking_number': booking_number,
                        'ticket_number': ticket_number,
                        'vendeur_id': vendeur_id,
                        'state': state,
                        'hotel_id': hotel_id,
                        'city_key': city_key,
                        'room_nbr': room_nbr,
                        'crdat': crdat,
                        'tu_key': row[6],
                        'region_id': region_id,
                        'currency_id': currency_id

                    }
                )
                if ticket_number:
                    if len(self.env['excursion.reservations'].sudo().search(
                            [('ticket_number', '=', int(ticket_number)), ('vendeur_id', '=', vendeur_id),
                             ('state', '=', row[17])])) == 0:
                        tarif = self.env['excursion.tarif.region'].sudo().search(
                            [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
                        currency_id = tarif.currency_id.id or self.env['excursion.excursion'].sudo().search(
                            [('name', '=', row[2])]).ito_curency.id
                        self.env['excursion.reservations'].sudo().create({
                            'dat': dat,
                            'excursion_id': excursion_id,
                            'adulte': adulte,
                            'enfant': enfant,
                            'inf': inf,
                            'tour_operateur': tour_operateur,

                            'ticket_number': ticket_number,
                            'vendeur_id': vendeur_id,
                            'state': state,
                            'hotel_id': hotel_id,
                            'city_key': city_key,
                            'room_nbr': room_nbr,
                            'crdat': crdat,
                            'tu_key': row[6],
                            'region_id': region_id,
                            'currency_id': currency_id

                        })

            else:
                # delete  em and recreate em
                l.unlink()
                # create em
                adulte = 0
                state = row[17]
                enfant = 0
                inf = 0
                birthday = ''
                dat = str(row[1])
                crdat = str(row[16])
                excursion_id = self.env['excursion.excursion'].sudo().search([('name', '=', row[2])]).id
                datenaiss = row[5] or ''
                # traittement de l'age'
                try:
                    booking_number = str(row[8])
                    booking_number_rec = self.env['ctm.reservation.list'].sudo().search(
                        [('reservation_number', '=', booking_number)])[0]
                    booking_number_arrival_date = booking_number_rec.chekin
                except:
                    booking_number = False
                if datenaiss == '':
                    if str(row[3]) == "Adult1":
                        adulte = adulte + 1
                    elif str(row[3]) == "Adult2":
                        adulte = adulte + 1
                    elif str(row[3]) == "Adult3":
                        adulte = adulte + 1
                    elif str(row[3]) == "Child1":
                        enfant = enfant + 1
                    elif str(row[3]) == "Child2":
                        enfant = enfant + 1
                    elif str(row[3]) == "Child3":
                        enfant = enfant + 1
                    elif str(row[3]) == "Infant1":
                        inf = inf + 1
                    elif str(row[3]) == "Infant2":
                        inf = inf + 1
                    elif str(row[3]) == "Infant3":
                        inf = inf + 1
                    else:
                        adulte = adulte + 1
                else:
                    try:
                        if booking_number_rec:
                            years = relativedelta(booking_number_arrival_date,
                                                  row[5]).years
                            months = relativedelta(booking_number_arrival_date,
                                                   row[5]).months
                        else:
                            years = relativedelta(row[1],
                                                  row[5]).years
                            months = relativedelta(row[1],
                                                   row[5]).months
                    except:
                        years = relativedelta(row[1],
                                              row[5]).years
                        months = relativedelta(row[1],
                                               row[5]).months

                    age = years + (months / 12)
                    bebemaxage = self.env['excursion.excursion'].sudo().search([('name', '=', row[2])]).bebemaxage
                    enfmaxage = self.env['excursion.excursion'].sudo().search([('name', '=', row[2])]).enfmaxage
                    if age >= enfmaxage:
                        adulte = adulte + 1
                    elif bebemaxage <= age < enfmaxage:
                        enfant = enfant + 1
                    elif age < bebemaxage:
                        inf = inf + 1
                tour_operateur = self.env['tour.operator'].sudo().search([('ito_id', '=', int(row[7]))])[0].id

                ticket_number = row[9]
                vendeur_id = self.env['excursion.guide'].sudo().search([('name', '=', row[10])]).id or False
                city_key = self.env['excursion.pointdepart'].sudo().search([('name', '=', row[13])]).id or False
                try:
                    selling_price = float(row[11])
                except:
                    selling_price = 0.0
                region_id = self.env['excursion.emplacement'].sudo().search([('name', '=', row[14])])[0].id or False
                paid_sum = selling_price
                hotel_id = self.env['rooming.hotels'].sudo().search([('hotel_id', '=', int(row[12]))])[0].id
                room_nbr = row[15]
                # look for currency
                tarif = self.env['excursion.tarif.region'].sudo().search(
                    [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
                currency_id = tarif.currency_id.id or self.env['excursion.excursion'].sudo().search(
                    [('name', '=', row[2])]).ito_curency.id
                if len(self.env['excursion.extra'].sudo().search(
                        [('ticket_number', '=', int(ticket_number)), ('vendeur_id', '=', vendeur_id),
                         ('tu_key', '=', row[6]), ('state', '=', row[17])])) == 0:
                    self.env['excursion.extra'].sudo().create(
                        {
                            'dat': dat,
                            'excursion_id': excursion_id,
                            'adulte': adulte,
                            'enfant': enfant,
                            'inf': inf,
                            'tour_operateur': tour_operateur,
                            'booking_number': booking_number,
                            'ticket_number': ticket_number,
                            'vendeur_id': vendeur_id,
                            'state': state,
                            'hotel_id': hotel_id,
                            'city_key': city_key,
                            'room_nbr': room_nbr,
                            'crdat': crdat,
                            'tu_key': row[6],
                            'region_id': region_id,
                            'currency_id': currency_id

                        }
                    )
                if ticket_number:
                    if len(self.env['excursion.reservations'].sudo().search(
                            [('ticket_number', '=', int(ticket_number)), ('vendeur_id', '=', vendeur_id),
                             ('state', '=', row[17])])) == 0:
                        tarif = self.env['excursion.tarif.region'].sudo().search(
                            [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
                        currency_id = tarif.currency_id.id or self.env['excursion.excursion'].sudo().search(
                            [('name', '=', row[2])]).ito_curency.id
                        self.env['excursion.reservations'].sudo().create({
                            'dat': dat,
                            'excursion_id': excursion_id,
                            'adulte': adulte,
                            'enfant': enfant,
                            'inf': inf,
                            'tour_operateur': tour_operateur,
                            'state': state,
                            'ticket_number': ticket_number,
                            'vendeur_id': vendeur_id,
                            'state': state,
                            'hotel_id': hotel_id,
                            'city_key': city_key,
                            'room_nbr': room_nbr,
                            'crdat': crdat,
                            'tu_key': row[6],
                            'region_id': region_id,
                            'currency_id': currency_id

                        })
        cnx1.close()

        # correct reservations according to that
        rng = range(self.tickets_from, self.tickets_to + 1, 1)
        rngl = []
        for r in rng:
            rngl.append(r)
        for x in self.env['excursion.reservations'].sudo().search([('ticket_number', 'in', rngl)]):
            adl = 0
            enf = 0
            nn = 0
            prc = 0
            vendeur_id = 0
            booking_list = []
            booking_list_char = " "
            ext = False
            to = 0
            exc = 0
            curr = 0
            little_list = self.env['excursion.extra'].sudo().search(
                [('ticket_number', '=', x.ticket_number), ('vendeur_id', '=', x.vendeur_id.id),
                 ('excursion_id', '=', x.excursion_id.id), ('state', '=', x.state)])
            if len(little_list) > 0:
                for m in little_list:
                    adl = adl + m.adulte
                    enf = enf + m.enfant
                    nn = nn + m.inf
                    prc = prc + m.selling_price
                    vendeur_id = m.vendeur_id
                    dat = m.dat
                    state = m.state
                    m.res_id = x.id
                    exc = m.excursion_id.id
                    to = m.tour_operateur.id
                    curr = m.currency_id.id
                    if str(m.booking_number) not in booking_list:
                        booking_list.append(str(m.booking_number))
                if x.excursion_id.ppp:
                    prc = prc / (adl + enf + nn)
                for kk in booking_list:
                    booking_list_char = booking_list_char + " , " + kk
                if x.ext25:
                    x.sudo().update({
                        'adulte': adl,
                        'enfant': enf,
                        'inf': nn,
                        'dat': dat,
                        'booking_number': booking_list_char,
                        'excursion_id': exc,
                        'tour_operateur': to,
                        'vendeur_id': vendeur_id,
                        'currency_id': curr,
                        'state': state,
                    })
                if not x.ext25:
                    if x.is_manuel:
                        x.sudo().update({
                            'adulte': adl,
                            'enfant': enf,
                            'inf': nn,
                            'dat': dat,
                            'booking_number': booking_list_char,
                            'excursion_id': exc,
                            'tour_operateur': to,
                            'vendeur_id': vendeur_id,
                            'currency_id': curr,
                            'state': state,
                        })
                    elif not x.is_manuel:
                        x.sudo().update({
                            'adulte': adl,
                            'enfant': enf,
                            'inf': nn,
                            'dat': dat,
                            'booking_number': booking_list_char,
                            'excursion_id': exc,
                            'tour_operateur': to,
                            'selling_price': prc,
                            'vendeur_id': vendeur_id,
                            'currency_id': curr,
                            'state': state,
                        })

    @api.multi
    def fill_hotels(self):
        import pyodbc
        server_url = '192.168.1.241'
        login = 'sa'
        password = 'TnCTMdbSA2018'
        check_second_driver = False
        try:
            cnx = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  PR_Name , PR_Key from ito_main.dbo.Partners')
        except:
            check_second_driver = True
        if check_second_driver:
            cnx = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  PR_Name , PR_Key from ito_main.dbo.Partners')
        for row in cursor:
            # test if the record exist :
            id = row[1]
            idrec = self.env['rooming.hotels'].search([('hotel_id', '=', id)])
            if len(idrec) == 0:
                self.env['rooming.hotels'].create({'name': row[0], 'hotel_id': row[1]})
        cnx.close()

    @api.multi
    def fill_categories(self):
        import pyodbc
        server_url = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_ip
        login = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_login
        password = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_password
        check_second_driver = False
        try:
            cnx = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  RC_NAME , RC_KEY from ito_main.dbo.RoomCategory where RC_KEY != 0')
        except:
            check_second_driver = True
        if check_second_driver:
            cnx = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  RC_NAME , RC_KEY from ito_main.dbo.RoomCategory where RC_KEY != 0')
        for row in cursor:
            # look for the record
            id = row[1]
            idrec = self.env['room.categories'].search([('ito_ID', '=', id)])
            if len(idrec) == 0:
                self.env['room.categories'].create({'name': row[0], 'ito_ID': row[1]})
        cnx.close()

    @api.multi
    def fill_rooms_type(self):
        import pyodbc
        server_url = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_ip
        login = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_login
        password = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_password
        check_second_driver = False
        try:
            cnx = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  RT_COMMENTS , RT_KEY from ito_main.dbo.RoomType where RT_KEY != 0')
        except:
            check_second_driver = True
        if check_second_driver:
            cnx = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  RT_COMMENTS , RT_KEY from ito_main.dbo.RoomType where RT_KEY != 0')
        for row in cursor:
            # search the record in the base
            id = row[1]
            idrec = self.env['room.types'].search([('ito_ID', '=', id)])
            if len(idrec) == 0:
                self.env['room.types'].create({'name': row[0], 'ito_ID': row[1]})
        cnx.close()

    @api.multi
    def fill_meals(self):
        import pyodbc
        server_url = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_ip
        login = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_login
        password = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_password
        check_second_driver = False
        try:
            cnx = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  PN_Name , PN_Key from ito_main.dbo.Pansion where PN_Key != 0')
        except:
            check_second_driver = True
        if check_second_driver:
            cnx = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  PN_Name , PN_Key from ito_main.dbo.Pansion where PN_Key != 0')
        for row in cursor:
            id = row[1]
            idrec = self.env['room.meal'].search([('ito_ID', '=', id)])
            if len(idrec) == 0:
                self.env['room.meal'].create({'name': row[0], 'ito_ID': row[1]})
        cnx.close()

    @api.multi
    def fill_to(self):
        import pyodbc
        server_url = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_ip
        login = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_login
        password = self.env['res.config.settings'].browse(
            self.env['res.config.settings'].search([], order='id desc', limit=1)[0].id).ito_server_password
        check_second_driver = False
        try:
            cnx = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  * from ito_main.dbo.v_TourOperators')
        except:
            check_second_driver = True
        if check_second_driver:
            cnx = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor = cnx.cursor()
            cursor.execute('Select  * from ito_main.dbo.v_TourOperators')
        for row in cursor:
            id = row[0]
            idrec = self.env['tour.operator'].search([('ito_id', '=', id)])
            if len(idrec) == 0:
                self.env['tour.operator'].create({'name': row[1], 'ito_id': row[0]})
        cnx.close()

    @api.multi
    def get_sale_list(self):
        # preparing the connection
        # self._cr.execute("delete from excursion_extra where id != 0 ")
        # TODO function of marouen
        liste_liquide = []
        details_of_excursion = []
        self._cr.execute(
            " select sum(adulte) , sum(enfant) , sum(inf) , ticket_number ,sum(selling_price)   from excursion_extra  group  by ticket_number order by ticket_number  ; ")
        for x in self._cr.fetchall():
            details_of_excursion = []
            obj = {
                'adulte': x[0],
                'enfant': x[1],
                'inf': x[2],
                'ticket_number': x[3],
                'selling_price': x[4],
                'excursion_id': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])
                [0].excursion_id.id,
                'dat': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].dat,
                'crdat': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].crdat,
                'radulte': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].radulte,
                'renfant': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].renfant,
                'rinf': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].rinf,
                'hotel_id': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].hotel_id.id,
                'room_nbr': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].room_nbr,
                'liquidation': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].liquidation,
                'dat_liquidation': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[
                    0].dat_liquidation,
                'currency_id': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].currency_id.id,
                'ext25': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].ext25,
                'ext25amount': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].ext25amount,
                'tu_key': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].tu_key,
                'region_id': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].region_id.id,
                'city_key': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].city_key.id,
                'tour_operateur': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[
                    0].tour_operateur.id,
                'vendeur_id': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[0].vendeur_id.id,
                'booking_number': self.env['excursion.extra'].search([('ticket_number', '=', x[3])])[
                    0].booking_number.id,

            }

            liste_liquide.append(obj)
        for y in liste_liquide:
            if len(self.env['excursion.reservations'].search([('ticket_number', '=', int(y['ticket_number']))])) == 0:
                rec = self.env['excursion.reservations'].create(y)
                for m in self.env['excursion.extra'].search([('ticket_number', '=', int(y['ticket_number']))]):
                    m.res_id = rec.id
            else:
                rec = self.env['excursion.reservations'].search([('ticket_number', '=', int(y['ticket_number']))])
                rec.update(y)
        return True

    @api.multi
    def get_sale_list_auto(self):
        # preparing the connection
        self._cr.execute("delete from excursion_extra where id != 0 ")
        import pyodbc
        server_url = "192.168.1.241"
        login = "sa"
        password = "TnCTMdbSA2018"
        check_second_driver = False
        try:
            cnx1 = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
        except:
            check_second_driver = True
        if check_second_driver:
            cnx1 = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
        today = datetime.datetime.today().date()
        strx = '''
                    SELECT
                    dl_key,
                    DL_Date		 as 'Excursion date', -- wp
                    ( SELECT SL_Name FROM ServiceList WHERE SL_Key = DL_Code )		 as 'Excursion_name', --wp
                    RTRIM(LTRIM(TU_Name)) as 'surname',
                    RTRIM(LTRIM(TU_FirstName))                        as 'Name',
                    TU_BIRTHDAY,
                    tu_key,
                    DG_PRKey        as 'Tour operator', --wp
                    dg_code as ' Booking number ', --wp
                    DL_VoucherNumber as 'Ticket number', --wp
                    (select GU_NAME from GUIDE where GU_KEY = DL_SUBCODE2) as 'guide name', --wp
                    DL_Price * dbo.zf_GetExchangeRate( DL_PriceCurrency, 'USD' , DL_Date, DL_PRKey ) as 'Selling price', --wp
                    (select PR_KEY from Partners where PR_KEY = DL_SUBCODE1)                              as Hotel,
                    ( SELECT CT_Name FROM CityDictionary WHERE CT_Key = DL_SubCode3 )	 as 'CityName', --wp
                    (select RG_name from REGION where RG_KEY = 
                    (select ct_rgkey from CITYDICTIONARY where CT_KEY = DL_SubCode3)) as ' region ', --wp
                    TU_RoomNumber									as 'R.N.', --wp
                    DL_CREATEDATE	,
                    CASE WHEN DL_STKey = 0 THEN 'New'
                               WHEN DL_STKey = 1 THEN 'Waiting confirmation'
                               WHEN DL_STKey = 2 THEN 'cnf'
                               WHEN DL_STKey = 3 THEN 'cncl'
                               WHEN DL_STKey = 4 THEN 'Not confirmed'
                               WHEN DL_STKey = 5 THEN 'cnf'
                               ELSE 'Complementary' END                    as StatusName
                    FROM	DogovorList, DOGOVOR , Turist T,
                    TuristService
                    WHERE
                    DG_KEY = DL_DGKEY 
                    and DL_STKey IN (2,5,3) and
                    DL_SVKey = 4 
                    AND     TU_Key = TU_TUKey
                    AND     DL_Key = TU_DLKey 
                    and dl_date >= '{0}'

        '''.format('2019-05-20')
        cursor1.execute(strx)

        for row in cursor1:
            adulte = 0
            enfant = 0
            inf = 0
            birthday = ''
            state = row[17]
            dat = str(row[1])
            crdat = str(row[16])
            excursion_id = self.env['excursion.excursion'].search([('name', '=', row[2])]).id
            datenaiss = row[5] or ''
            # traittement de l'age'
            try:
                booking_number = str(row[8])
                booking_number_rec = self.env['ctm.reservation.list'].sudo().search(
                    [('reservation_number', '=', booking_number)])[0]
                booking_number_arrival_date = booking_number_rec.chekin
            except:
                booking_number = False
            if datenaiss == '':
                if str(row[3]) == "Adult1":
                    adulte = adulte + 1
                elif str(row[3]) == "Adult2":
                    adulte = adulte + 1
                elif str(row[3]) == "Adult3":
                    adulte = adulte + 1
                elif str(row[3]) == "Child1":
                    enfant = enfant + 1
                elif str(row[3]) == "Child2":
                    enfant = enfant + 1
                elif str(row[3]) == "Child3":
                    enfant = enfant + 1
                elif str(row[3]) == "Infant1":
                    inf = inf + 1
                elif str(row[3]) == "Infant2":
                    inf = inf + 1
                elif str(row[3]) == "Infant3":
                    inf = inf + 1
                else:
                    adulte = adulte + 1
            else:
                if booking_number_rec:
                    years = relativedelta(booking_number_arrival_date,
                                          row[5]).years
                    months = relativedelta(booking_number_arrival_date,
                                           row[5]).months
                else:
                    years = relativedelta(row[1],
                                          row[5]).years
                    months = relativedelta(row[1],
                                           row[5]).months

                age = years + (months / 12)
                bebemaxage = self.env['excursion.excursion'].search([('name', '=', row[2])]).bebemaxage
                enfmaxage = self.env['excursion.excursion'].search([('name', '=', row[2])]).enfmaxage
                if age >= enfmaxage:
                    adulte = adulte + 1
                elif bebemaxage <= age < enfmaxage:
                    enfant = enfant + 1
                elif age < bebemaxage:
                    inf = inf + 1
            tour_operateur = self.env['tour.operator'].search([('ito_id', '=', int(row[7]))])[0].id

            ticket_number = row[9]
            vendeur_id = self.env['excursion.guide'].search([('name', '=', row[10])]).id or False
            city_key = self.env['excursion.pointdepart'].search([('name', '=', row[13])]).id or False
            try:
                selling_price = float(row[11])
            except:
                selling_price = 0.0
            region_id = self.env['excursion.emplacement'].search([('name', '=', row[14])])[0].id or False
            paid_sum = selling_price
            try:

                hotel_id = self.env['rooming.hotels'].search([('hotel_id', '=', int(row[12]))])[0].id
            except:
                hotel_id = False
            room_nbr = row[15]
            # look for currency
            tarif = self.env['excursion.tarif.region'].search(
                [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
            currency_id = tarif.currency_id.id or self.env['excursion.excursion'].search(
                [('name', '=', row[2])]).ito_curency.id
            self.env['excursion.extra'].create(
                {
                    'dat': dat,
                    'excursion_id': excursion_id,
                    'adulte': adulte,
                    'enfant': enfant,
                    'inf': inf,
                    'tour_operateur': tour_operateur,
                    'booking_number': booking_number,
                    'ticket_number': ticket_number,
                    'vendeur_id': vendeur_id,
                    'state': state,
                    'hotel_id': hotel_id,
                    'city_key': city_key,
                    'room_nbr': room_nbr,
                    'crdat': crdat,
                    'tu_key': row[6],
                    'region_id': region_id,
                    'currency_id': currency_id

                }
            )
            if ticket_number:
                if len(self.env['excursion.reservations'].search(
                        [('ticket_number', '=', int(ticket_number)), ('vendeur_id', '=', vendeur_id),
                         ('state', '=', state)])) == 0:
                    tarif = self.env['excursion.tarif.region'].search(
                        [('excursion_id', '=', excursion_id), ('region.id', '=', region_id)])
                    currency_id = tarif.currency_id.id or self.env['excursion.excursion'].search(
                        [('name', '=', row[2])]).ito_curency.id
                    self.env['excursion.reservations'].create({
                        'dat': dat,
                        'excursion_id': excursion_id,
                        'adulte': adulte,
                        'enfant': enfant,
                        'inf': inf,
                        'tour_operateur': tour_operateur,
                        'state': state,
                        'ticket_number': ticket_number,
                        'vendeur_id': vendeur_id,

                        'hotel_id': hotel_id,
                        'city_key': city_key,
                        'room_nbr': room_nbr,
                        'crdat': crdat,
                        'tu_key': row[6],
                        'region_id': region_id,
                        'currency_id': currency_id

                    })
        cnx1.close()
        little_list = []
        adl = 0
        enf = 0
        nn = 0
        prc = 0
        pr = 0
        for x in self.env['excursion.reservations'].search([('liquidation', '=', False)]):
            adl = 0
            enf = 0
            nn = 0
            prc = 0
            vendeur_id = 0
            booking_list = []
            booking_list_char = " "
            ext = False
            to = 0
            exc = 0
            curr = 0
            little_list = self.env['excursion.extra'].search(
                [('ticket_number', '=', x.ticket_number), ('vendeur_id', '=', x.vendeur_id.id),
                 ('excursion_id', '=', x.excursion_id.id), ('state', '=', x.state)])
            if len(little_list) > 0:
                for m in little_list:
                    adl = adl + m.adulte
                    enf = enf + m.enfant
                    nn = nn + m.inf
                    prc = prc + m.selling_price
                    vendeur_id = m.vendeur_id
                    dat = m.dat
                    state = m.state
                    m.res_id = x.id
                    exc = m.excursion_id.id
                    to = m.tour_operateur.id
                    curr = m.currency_id.id
                    if str(m.booking_number) not in booking_list:
                        booking_list.append(str(m.booking_number))
                if x.excursion_id.ppp:
                    prc = prc / (adl + enf + nn)
                for kk in booking_list:
                    booking_list_char = booking_list_char + " , " + kk
                if x.ext25:
                    x.update({
                        'adulte': adl,
                        'enfant': enf,
                        'inf': nn,
                        'dat': dat,
                        'booking_number': booking_list_char,
                        'excursion_id': exc,
                        'tour_operateur': to,
                        'vendeur_id': vendeur_id,
                        'state': state,
                        'currency_id': curr
                    })
                if not x.ext25:
                    if x.is_manuel:
                        x.update({
                            'adulte': adl,
                            'enfant': enf,
                            'inf': nn,
                            'dat': dat,
                            'booking_number': booking_list_char,
                            'excursion_id': exc,
                            'tour_operateur': to,
                            'vendeur_id': vendeur_id,
                            'state': state,
                            'currency_id': curr
                        })
                    elif not x.is_manuel:
                        x.update({
                            'adulte': adl,
                            'enfant': enf,
                            'inf': nn,
                            'dat': dat,
                            'booking_number': booking_list_char,
                            'excursion_id': exc,
                            'tour_operateur': to,
                            'selling_price': prc,
                            'state': state,
                            'vendeur_id': vendeur_id,
                            'currency_id': curr
                        })
        # clean the crap
        for b in self.env['excursion.reservations'].search([]):
            if (len(b.excursion_detail) == 0) and b.liquidation == False and b.is_manuel == False:
                b.unlink()

        return True

    @api.multi
    def get_res_list(self):
        # for x in self.env['rooming.list'].search([]):
        #     date_naiss = x.datenaiss
        #     years = relativedelta(x.checkin,
        #                               x.datenaiss).years
        #     months = relativedelta(x.checkin,
        #                                x.datenaiss).months
        #
        #     age = years + (months/12)
        #     x.write({
        #             'age': age
        #         })
        for y in self.env['ctm.reservation.list'].search([]):
            recs = self.env['rooming.list'].search([('num_reser', '=', y.reservation_number)])
            for x in recs:
                x.write({
                    'reservation_list_id': y.id
                })
        for k in self.env['ctm.reservation.list'].search([]):
            little_list = self.env['rooming.list'].search([('num_reser', '=', k.reservation_number)])
            k.bebe = 0
            k.pax_adult = 0
            k.pax_enfant = 0
            for y in little_list:
                contract_id = self.env['contract.contract'].search(
                    [('hotel', '=', k.hotel_id.id), ('date_start', '<=', k.chekin),
                     ('date_end', '>=', k.chekin)])

                if len(contract_id) == 1:
                    if 2 <= y.age < contract_id.min_adult_age:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < contract_id.min_enf_age:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1
                elif len(contract_id) > 1:
                    contract_id = contract_id[0]
                    if 2 <= y.age < contract_id.min_adult_age:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < contract_id.min_enf_age:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1
                else:
                    if 2 <= y.age < 12:
                        k.pax_enfant = k.pax_enfant + 1
                    elif 0 < y.age < 2:
                        k.bebe = k.bebe + 1
                    elif y.age == 0:
                        k.pax_adult = k.pax_adult + 1
                    else:
                        k.pax_adult = k.pax_adult + 1

        return True

    @api.multi
    def get_rooming_list(self):
        # preparing the connection
        hotels_del = []
        import pyodbc
        server_url = '192.168.1.241'
        login = 'sa'
        password = 'TnCTMdbSA2018'
        check_second_driver = False
        try:
            cnx1 = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.0.so.1.0};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cnx2 = pyodbc.connect(
                "Driver={/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.0.so.1.0};Server=" + server_url +
                ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
            cursor2 = cnx2.cursor()
        except:
            check_second_driver = True
        if check_second_driver:
            cnx1 = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cnx2 = pyodbc.connect(
                "Driver={Sql server};Server=" + server_url + ";Database=ito_main;Uid=" + login + ";Pwd=" + password)
            cursor1 = cnx1.cursor()
            cursor2 = cnx2.cursor()
        where = []
        ch = ''
        ids = []
        ids1 = []
        if self.reservation_number:
            ch = " TU_DGCode = '{0}'".format(self.reservation_number)
            where.append(ch)
        if self.date_start:
            ch = "DL_Date >= '" + str(datetime.datetime.strftime(self.date_start, '%Y-%m-%d')) + "'"
            where.append(ch)
        if self.date_end:
            ch = "DL_Date <= '" + str(datetime.datetime.strftime(self.date_end, '%Y-%m-%d')) + "'"
            where.append(ch)
        if self.creation_date_start:
            ch = "DG_CrDate >= '" + str(datetime.datetime.strftime(self.creation_date_start, '%Y-%m-%d')) + "'"
            where.append(ch)
        if self.creation_date_end:
            ch = "DG_CrDate <= '" + str(datetime.datetime.strftime(self.creation_date_end, '%Y-%m-%d')) + "'"
            where.append(ch)
        if len(self.hotel) > 0:
            for x in self.hotel:
                ids.append(x.hotel_id)
            if len(ids) == 1:
                ids.append(0)
            ch = 'DL_Code in {0}'.format(tuple(ids))
            where.append(ch)
        if len(self.tour_operator) > 0:
            for y in self.tour_operator:
                ids1.append(y.ito_id)

            if len(ids1) == 1:
                ids1.append(0)
            ch = 'DG_PRKey in {0}'.format(tuple(ids1))
            where.append(ch)
        strxx = ""

        strx = '''
                        SELECT
               RTRIM(LTRIM(TU_Name))                            as Surname,
               RTRIM(LTRIM(TU_FirstName))                        as Name,
               TU_Birthday                                        as Birthday,
               RTRIM(LTRIM(TU_DGCode))                            as 'Resv.Nr',
               DG_CommonNumber                                    as 'Common Nr.',
               DG_CrDate                                        as Booked,
               DL_Date                                            as 'C/in',
               DL_DateEnd                                        as 'C/out',
               (SELECT COUNT(1) FROM Turist WHERE TU_DGKey = DG_KEY) as Pax,
               (SELECT CT_Name FROM CityDictionary WHERE CT_Key = P1.PR_CTKey) as City,
               P1.PR_Name                                        as Hotel,
               TU_RoomNumber                                    as 'R.N.',
               dbo.zf_GetShortPartnerName(DG_PRKey)            as 'Tour operator',
               ''                                                as Tourists,
               dbo.zf_GetFreeCancellationTillDate(DL_Key)        as 'FreeCancelTill',
               DG_TotalInvNumber                                as 'Inv. number',
               0                                                as InvSum,
               DG_DueDate                                        as DueDate,
               DG_VoucherNumber                                as 'Voucher nr.',
               DG_HConfNumber                                    as 'Hotel conf nr.',
               DL_Notes                                        as Notes,
               DL_STKey                                        as Status,
               CASE WHEN DL_STKey = 0 THEN 'New'
                               WHEN DL_STKey = 1 THEN 'Waiting confirmation'
                               WHEN DL_STKey = 2 THEN 'Confirmed'
                               WHEN DL_STKey = 3 THEN 'Cancelled'
                               WHEN DL_STKey = 4 THEN 'Not confirmed'
                               WHEN DL_STKey = 5 THEN 'Confirmed'
                               ELSE 'Complementary' END                    as StatusName,
               DG_Key                                            as BookingNo,
               DG_IsLocked                                        as IsLocked,
               DG_AgentReferenceNumber                            as Reference,
               (SELECT PR_Name FROM Partners WHERE PR_Key = DL_LegalEntityID AND PR_Key > 0)  as LegalEntity,
               ''                                                as Net,
               ''                                                as Price,
               ''                                                as Paid,
               (SELECT LastPaymentDate FROM dbo.zf_GetBookingPaymentInfo(DG_Key))    as PaymentDate,
               (SELECT US_Name + ' ' + isnull(US_ShortName, '') FROM UserList WHERE US_Key = DG_ManagerID) as BookingManager,
               (SELECT V_Name FROM PaymentType WHERE ID = DG_PaymentType AND ID > 0) as PaymentType,
               DG_ProformaInvoiceNumber                        as ProformaInvoiceNumber,
               DG_AdditionalInvoiceNumber                        as AdditionalInvoiceNumber,
               P1.PR_Key as hotel_id,
               DG_Key as reservation_id,
               DG_PRKey as touroperatorID,
                 ( SELECT RT_Key FROM RoomType     WHERE RT_Key = DL_SubCode1 ) as 'RoomTypeName',
                   ( SELECT RC_Key                     FROM RoomCategory WHERE RC_Key = DL_SubCode3 ) as 'RoomCategoryName',
                   ( SELECT AC_Key                     FROM Accomodation WHERE AC_Key = DL_ACKey )    as 'AccommodationTypeName',
                   ( SELECT PN_Key                     FROM Pansion      WHERE PN_Key = DL_SubCode2 ) as 'MealTypeName'
               FROM    Dogovor,
                   DogovorList,
                   Turist T,
                   TuristService,
                   Partners P1,
                   Package ,
                    CityDictionary,
                    _Partners p2
               WHERE
               DL_SVKey =  1
              and DL_STKey in (1,2,4,5)
               AND     DL_DGKey = DG_Key
               AND     DG_Code != '#'
               AND     P1.PR_Key = DL_Code
                AND     p2.PR_Key = DL_Code
               AND     TU_Key = TU_TUKey
               AND     DL_Key = TU_DLKey
                and CT_Key = DL_CTKey 
              
                AND     PK_Key = DG_PackageID  
                '''
        if len(where) > 0:
            for something in where:
                strx = strx + '\n AND ' + something
        strx = strx + ' ORDER BY RTRIM(LTRIM(TU_DGCode))	 DESC'
        cursor1.execute(strx)
        age = 0
        meal = ""
        night_number = 0
        room_type = ""
        room_category = ""
        accomodation = ""
        L = []
        cpt = 0
        has_contract = False
        for row in cursor1:
            has_contract = False
            cpt = cpt + 1
            id = int(row[35])
            oid = int(row[37])
            hotel = self.env['rooming.hotels'].search([('hotel_id', '=', id)])[0]
            touroperator = self.env['tour.operator'].search([('ito_id', '=', oid)])[0]
            if len(self.env['contract.contract'].search(
                    [('hotel', '=', hotel.id), ('mr_id', 'in', touroperator.mr_id.id)])) > 0:
                has_contract = True
            if has_contract is True:
                booking_id = row[36]

                meal = self.env['room.meal'].search([('ito_ID', '=', row[41])]).id
                room_type = self.env['room.types'].search([('ito_ID', '=', row[38])]).id
                room_category = self.env['room.categories'].search([('ito_ID', '=', row[39])]).id
                accomodation = row[40]
                night_number = relativedelta(row[7], row[6]).days
                # finally insert the information in the database
                exist = False
                if row[2]:
                    if len(self.env['rooming.list'].search([('datenaiss','=',str(row[2])),('num_reser','=', str(row[3])), ('client_name','=',(str(row[0]) + " " + str(row[1])))])) > 0 :
                        exist = True
                else:
                    if len(self.env['rooming.list'].search([('num_reser','=', str(row[3])), ('client_name','=',(str(row[0]) + " " + str(row[1])))])) > 0 :
                        exist = True
                if exist is True:
                    # TODO : insert extra work code here ( to do updates on old records )
                    pass
                if exist is False:
                    if (row[2]):
                        years = relativedelta(row[6],
                                              row[2]).years
                        months = relativedelta(row[6],
                                               row[2]).months

                        age = years + (months / 12)
                        r = self.env['rooming.list'].create(
                            {
                                'active': True,
                                'num_reser': str(row[3]),
                                'client_name': str(row[0]) + " " + str(row[1]),
                                'datenaiss': str(row[2]),
                                'age': str(age),
                                'meal': meal,
                                'room_type': room_type,
                                'room_category': room_category,
                                'accomodation': accomodation,
                                'night_number': night_number,
                                'checkin': row[6],
                                'checkout': row[7],
                                'hotel': hotel.id,
                                'tour_operator': touroperator.id,
                                'status': str(row[22]),
                                'note': str(row[20]),
                                'creation_date': row[5],
                                'booking_number': row[23]
                            })

                    else:
                        r = self.env['rooming.list'].create(
                            {
                                'active': True,
                                'num_reser': str(row[3]),
                                'client_name': str(row[0]) + " " + str(row[1]),
                                'checkin': row[6],
                                'checkout': row[7],
                                'hotel': hotel.id,
                                'meal': meal,
                                'room_type': room_type,
                                'room_category': room_category,
                                'accomodation': accomodation,
                                'night_number': night_number,
                                'tour_operator': touroperator.id,
                                'status': str(row[22]),
                                'note': str(row[20]),
                                'creation_date': row[5],
                                'booking_number': row[23]
                            })

        cnx1.close()
        cnx2.close()
        # update datas
        contract_id = False
        for x in self.env['ctm.reservation.list'].search([]):
            li = self.env['rooming.list'].search([('num_reser', '=', x.reservation_number)])
            contract_id = self.env['contract.contract'].search(
                 [('hotel', '=', x.hotel_id.id), ('mr_id', 'in', x.touroperator_id.mr_id.id)])
            x.bebe = 0
            x.pax_adult = 0
            x.pax_enfant = 0
            for y in li:
                if y.reservation_list_id is False:
                    y.reservation_list_id = x.id
                    x.note = y.note
                    x.tour_operator = y.tour_operator.id
                    if len(contract_id) > 0:
                        contract_id = contract_id[0]
                        if contract_id.min_enf_age <= y.age < contract_id.min_adult_age:
                            x.pax_enfant = x.pax_enfant + 1
                        elif 0.1 < y.age < contract_id.min_enf_age:
                            x.bebe = x.bebe + 1
                        else:
                            x.pax_adult = x.pax_adult + 1
                    else:
                        if 2 <= y.age < 12:
                            x.pax_enfant = x.pax_enfant + 1
                        elif 0.1 < y.age < 2:
                            x.bebe = x.bebe + 1
                        else:
                            x.pax_adult = x.pax_adult + 1
        # create data
        new_rooming_lists = self.env['rooming.list'].search([('reservation_list_id', '=', False)])
        for x in new_rooming_lists:
            rec = self.env['contract.contract'].search(
                [('hotel', '=', x.hotel.id), ('mr_id', 'in', x.tour_operator.mr_id.id)])
            if len(rec) > 0:
                rec = rec[0]
            currency_id = rec.currency_id.id
            e = rec.echeance
            echance = x.checkout + relativedelta(days=e)
            obj = {
                'reservation_number': x.num_reser,
                'chekin': x.checkin,
                'checkout': x.checkout,
                'hotel_id': x.hotel.id,
                'touroperator_id': x.tour_operator.id,
                'pax_adult': 0,
                'pax_enfant': 0,
                'bebe': 0,
                'meal': x.meal.id,
                'room_category': x.room_category.id,
                'room_type': x.room_type.id,
                'night_number': x.night_number,
                'echeance': echance,
                'currency_id': currency_id,
                'note': x.note,
                'company_id': self.env['tour.operator'].search([('id', '=', x.tour_operator.id)]).company_id.id,
                'creation_date': x.creation_date

            }
            if len(self.env['ctm.reservation.list'].search([('reservation_number', '=', x.num_reser)])) == 0:
                rec = self.env['ctm.reservation.list'].create(obj)
                little_list = self.env['rooming.list'].search([('num_reser', '=', rec.reservation_number)])
                for y in little_list:
                    contract_id = self.env['contract.contract'].search(
                        [('hotel', '=', x.hotel.id), ('mr_id', 'in', x.tour_operator.mr_id.id)])
                    if len(contract_id) > 0:
                        contract_id = contract_id[0]
                        if contract_id.min_enf_age <= y.age < contract_id.min_adult_age:
                            rec.pax_enfant = rec.pax_enfant + 1
                        elif 0.1 < y.age < contract_id.min_enf_age:
                            rec.bebe = rec.bebe + 1
                        else:
                            rec.pax_adult = rec.pax_adult + 1
                    else:
                        if 2 <= y.age < 12:
                            rec.pax_enfant = rec.pax_enfant + 1
                        elif 0.1 < y.age < 2:
                            rec.bebe = rec.bebe + 1
                        else:
                            rec.pax_adult = rec.pax_adult + 1

                    y.reservation_list_id = rec.id
                # accomodation affectation
                is_sgl = False
                accomodations_list = []
                net_room = self.env['room.prices'].search(
                    [('contract_id', '=', contract_id.id), ('prices_type', '=', 'n'),('room','=',rec.room_category.id)])
                for lacc in net_room.accomodations:
                                    if not lacc.is_sub_accomodation:
                                        accomodations_list.append(lacc)
                for acc in accomodations_list:
                    if acc.id == self.env['ir.model.data'].xmlid_to_res_id(
                            'product_price_computation_carthage_group.accomodation_sgl'):
                        is_sgl = True
                if rec.pax_adult == 2 and rec.pax_enfant == 0:
                    rec.accomodation = self.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_2_dbl')
                elif rec.pax_adult == 1 and rec.pax_enfant == 0 and is_sgl:
                    rec.accomodation = self.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_sgl')
                elif rec.pax_adult == 1 and rec.pax_enfant == 0 and not is_sgl:
                    rec.accomodation = self.env['ir.model.data'].xmlid_to_res_id(
                        'product_price_computation_carthage_group.accomodation_dbl')
                else:
                    for acc in accomodations_list:
                        if acc.adult == rec.pax_adult and acc.child == rec.pax_enfant:
                            rec.accomodation = acc.id
                # calculate it of course
                if rec.accomodation and rec.meal:
                    try:
                        calc = rec.calculate_prices(rec.id)
                        rec.brut = calc['net']
                        rec.net = calc['net']
                    except:
                        pass

        return True


class GuideInherit(models.Model):
    _inherit = "excursion.guide"

    sigma_guide_name = fields.Char('sigma guide name')
    sigma_guide_code = fields.Char('sigma guide code')
    sigma_guide_cnt_code = fields.Char('sigma guide cnt code')


class ExcursionInherit(models.Model):
    _inherit = "excursion.excursion"

    sigma_excursion_name = fields.Char('sigma excursion name')
    sigma_excursion_code = fields.Char('sigma excursion code')
    sigma_excursion_cnt_code = fields.Char('sigma excursion cnt code')
