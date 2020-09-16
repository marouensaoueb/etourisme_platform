# -*- coding: utf-8 -*-
import datetime
import logging

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class hotels(models.Model):
    _name = 'rooming.hotels'
    _rec_name = 'name'

    name = fields.Char('Hotel Name')
    hotel_id = fields.Integer('Hotel ID')
    code_hotel = fields.Char('Code hotel')
    partner_id = fields.Many2one('res.partner', string="Partneaire lié")
    currency_id = fields.Many2one('res.currency', string="Currency")
    star_rating = fields.Selection(
        selection=[('0', ''), ('1', '*'), ('2', '**'), ('3', '***'), ('4', '****'), ('5', '*****')],
        string="star rating")


class reduct(models.Model):
    _name = "rooming.rule"
    _rec_name = "name"
    _order = 'sequence'

    @api.model
    def set_domain(self):
        return [('contract_id', '=', self.contract_id)]

    name = fields.Char('Rule name')
    rule_type = fields.Selection(selection=[('red', 'Reduction'), ('sup', 'supplément')], string="type de rule")
    typee = fields.Selection(selection=[('pr', 'Pourcentage'), ('v', 'Valeur')], string="Type de valeur de rule")
    valeur = fields.Float('Rule value', digits=(10, 3))
    paxes_validity = fields.Selection(selection=[('all', 'ALL PAXES'), ('one', 'ONE PAXE'), ('sp', 'SPECIAL')])
    paxes_validity_applied = fields.Integer('Number of paxes')
    min_pax_enf = fields.Integer('Min kids to apply this rule')
    max_pax_enf = fields.Integer('Max kids to apply this rule ')
    min_pax_adl = fields.Integer('Min adults to apply this rule')
    max_pax_adl = fields.Integer('Max adults to apply this rule ')
    Age = fields.Boolean('Age ?  ')
    age_min = fields.Float('Age min', digits=(10, 2))
    age_max = fields.Float('Age max', digits=(10, 2))
    typechabbrebool = fields.Boolean('Chambre type and category included ?')
    tpye_ch = fields.Many2one('room.types', string="Type de chambre")
    categ_ch = fields.Many2many('room.categories', string='Categorie des chabres')
    contract_id = fields.Many2one('contract.contract')
    datebool = fields.Boolean('By date ?')
    start = fields.Date('Start date')
    end = fields.Date('End date')
    persons_bool = fields.Boolean('Depend to persons ?')
    meal_bool = fields.Boolean('Depends to meals ?')
    creation_date_bool = fields.Boolean('By creation date ?')
    min_creation_date = fields.Date('Min creation date')
    max_creation_date = fields.Date('Max creation date')
    meal = fields.Many2one('room.meal', string="Arrangement")
    season_bool = fields.Boolean('By season')
    night_number_bool = fields.Boolean('Bu night number ? ')
    min_night_number = fields.Integer('Min night number')
    max_night_number = fields.Integer('max nights number ')
    promo_room_bool = fields.Boolean('a promo room reduction? ')
    promo_room = fields.Many2one('room.categories', string='Wich room is in a promo ? ')
    has_non_cummulable = fields.Boolean('Has non commulable recductions ? ')
    # non_commulable_with = fields.Many2many('rooming.rule', string="non commulable with ")
    season = fields.Many2many('seasons', string="Seasons")
    has_base_price_bool = fields.Boolean('Has base price ? ')
    base_price = fields.Many2one('room.categories', string="Base Price room")
    apply_to_invoice_bool = fields.Boolean('Apply on the invoice ? ')
    adultonly = fields.Boolean('Adult only ')
    temp = fields.Integer('Temporatry execution ')
    sequence = fields.Integer('sequence')
    do_nothing = fields.Boolean('is manual')


class reductionappy(models.Model):
    _name = 'reduction.apply'

    @api.model
    def get_domain(self):
        rec = self.env['ctm.reservation.list'].search([('id', 'in', self._context.get('active_ids'))])
        hotel_list = []
        for x in rec:
            hotel_list.append(x.hotel_id.id)
        contract_ids = self.env['contract.contract'].search([('hotel', 'in', hotel_list)])
        contracts_list = []
        for c in contract_ids:
            contracts_list.append(c.id)
        try:

            return contracts_list[0]
        except:
            return []

    contract_id = fields.Many2one('contract.contract', string="Contract", readonly=True, default=get_domain)
    reductions_applied = fields.Char('Formula')
    hotel_id = fields.Many2many('rooming.hotels', string="Hotel")
    date_start = fields.Date(string="Date start")
    date_fin = fields.Date(string="Date fin")
    state = fields.Selection(
        selection=[('info', 'Payé'), ('muted', 'Non payé')], string='etat')

    @api.multi
    def calcule_par_hotel_check_in(self):
        return True

    @api.multi
    def apply_reductions(self):
        active_ids = self.env['ctm.reservation.list'].prepare_reservation()
        formula = self.reductions_applied
        for x in active_ids:
            rec = self.env['ctm.reservation.list'].search([('id', '=', x)])
            if 'net' in formula:
                formula = 'rec.net = '+ formula.replace('net','rec.net')
            if 'brut' in formula:
                formula = 'rec.net = ' + formula.replace('brut','rec.brut')
            exec(formula)

    @api.multi
    def calculatenet(self):

        active_ids = self.env['ctm.reservation.list'].prepare_reservation()
        # fetch the records from the reservation table one by one with the use of the ids
        for x in active_ids:
            result = self.env['ctm.reservation.list'].search([('id','=',x)]).calculate_prices(x)
            self.env['ctm.reservation.list'].search([('id','=',x)]).net = result['net']
            self.env['ctm.reservation.list'].search([('id','=',x)]).brut = result['net']
    @api.multi
    def change_coulour(self):
        active_ids = self.env['ctm.reservation.list'].prepare_reservation()
        for x in active_ids:
            rec = self.env['ctm.reservation.list'].search([('id', '=', x)])
            rec.coloration = self.state


class ctm_rooming_list(models.Model):
    _name = 'rooming.list'
    _rec_name = 'num_reser'

    hotel = fields.Many2one('rooming.hotels', string="Hotel")
    tour_operator = fields.Many2one('tour.operator', string='Tour Opertor')
    active = fields.Boolean('Still working ? ', default=True)
    num_reser = fields.Char('Num reservation')
    id_reservation = fields.Char('ID reservation')
    client_name = fields.Char('Nom de client')
    datenaiss = fields.Date('Date de naissance')
    age = fields.Float('Age', digits=(10, 3))
    room_type = fields.Many2one('room.types', string='Room type')
    room_category = fields.Many2one('room.categories', string='Room category')
    meal = fields.Many2one('room.meal', string='Meal')
    night_number = fields.Integer('Nombre des nuits')
    accomodation = fields.Char('Accomodation')
    checkout = fields.Date('Date de Depart')
    checkin = fields.Date('Date de Arrive')
    status = fields.Char('Status')
    booking_number = fields.Integer('Booking number')
    note = fields.Text('Note')
    creation_date = fields.Date('Creation date')
    reservation_list_id = fields.Many2one('ctm.reservation.list')


    @api.multi
    def prepare_reservation(self):
        return self._context.get('active_ids')

    @api.multi
    def action_transport_open(self):
        """ This opens the xml view specified in xml_id for the current reservation """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('ctm_tools', xml_id)
            res.update(

                domain=[('reservation_id', '=', self.id)]
            )
            return res
        return False

    @api.model
    def aut_function(self):
        import pyodbc
        driver_str = "41.226.13.69,8099"
        cnx1 = pyodbc.connect(
            "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + driver_str + ";Database=ito_main;Uid=sa;Pwd=TnCTMdbSA2018")
        cnx2 = pyodbc.connect(
            "Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.3.so.1.1};Server=" + driver_str + ";Database=ito_main;Uid=sa;Pwd=TnCTMdbSA2018")
        cursor1 = cnx1.cursor()
        cursor2 = cnx2.cursor()
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
                       DG_Notes                                        as Notes,
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
                       DL_SVKey = 1
                       AND     DL_DGKey = DG_Key
                       AND     DG_Code != '#'
                       AND     P1.PR_Key = DL_Code
                        AND     p2.PR_Key = DL_Code
                       AND     TU_Key = TU_TUKey
                       AND     DL_Key = TU_DLKey
                       AND     PK_Key = DG_PackageID
                        and CT_Key = DL_CTKey
                AND DG_CrDate > '2019/03/25' ORDER BY RTRIM(LTRIM(TU_DGCode))	 DESC'''
        cursor1.execute(strx)
        age = 0
        meal = ""
        night_number = 0
        room_type = ""
        room_category = ""
        accomodation = ""
        L = []
        cpt = 0
        for row in cursor1:
            cpt = cpt + 1
            id = int(row[35])
            oid = int(row[37])
            hotel = self.env['rooming.hotels'].search([('hotel_id', '=', id)])
            touroperator = self.env['tour.operator'].search([('ito_id', '=', oid)])
            booking_id = row[36]

            meal = self.env['room.meal'].search([('ito_ID', '=', row[41])]).id
            room_type = self.env['room.types'].search([('ito_ID', '=', row[38])]).id
            room_category = self.env['room.categories'].search([('ito_ID', '=', row[39])]).id
            accomodation = row[40]
            night_number = relativedelta(row[7], row[6]).days
            obj = {
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
                'checkin': str(row[6]),
                'checkout': str(row[7]),
                'hotel': hotel.id,
                'tour_operator': touroperator.id,
                'status': str(row[22]),
                'note': str(row[20]),
                'creation_date': str(row[5]),
                'booking_number': str(row[23])
            }
            # finally insert or update the information in the database
            if (row[2]):
                age = relativedelta(row[6],
                                    row[2]).years
                self.env['rooming.list'].create(
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
                        'checkin': str(row[6]),
                        'checkout': str(row[7]),
                        'hotel': hotel.id,
                        'tour_operator': touroperator.id,
                        'status': str(row[22]),
                        'note': str(row[20]),
                        'creation_date': str(row[5]),
                        'booking_number': str(row[23])
                    })
            else:
                self.env['rooming.list'].create(
                    {
                        'active': True,
                        'num_reser': str(row[3]),
                        'client_name': str(row[0]) + str(row[1]),
                        'checkin': str(row[6]),
                        'checkout': str(row[7]),
                        'hotel': hotel.id,
                        'meal': meal,
                        'room_type': room_type,
                        'room_category': room_category,
                        'accomodation': accomodation,
                        'night_number': night_number,
                        'tour_operator': touroperator.id,
                        'status': str(row[22]),
                        'note': str(row[20]),
                        'creation_date': str(row[5]),
                        'booking_number': str(row[23])
                    })
        cnx1.close()
        cnx2.close()


class CtmReservationlist(models.Model):
    _name = "ctm.reservation.list"
    _rec_name = "reservation_number"
    _description = " the list of reservation that will contain it's rooming list data "

    reservation_number = fields.Char('Reservation number')
    chekin = fields.Date('Check in')
    checkout = fields.Date('check out')
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    currency_id = fields.Many2one('res.currency')
    touroperator_id = fields.Many2one('tour.operator', string="Tour operator")
    pax_adult = fields.Integer('Adults number')
    pax_enfant = fields.Integer('Childrens number')
    bebe = fields.Integer('bébé')
    night_number = fields.Integer('Nights number')
    brut = fields.Monetary('Brut', digits=(10, 3))
    net = fields.Monetary('Net', digits=(10, 3))
    company_id = fields.Many2one('res.company', string='Company')
    fact_hotel = fields.Float('Facturation hotel', digits=(10, 3))
    num_fact_hotel = fields.Char('Num facturation hotel')
    echeance = fields.Date('échèance')
    reste_to_pay = fields.Monetary('Reste a payer', digits=(10, 3))
    note = fields.Char('Note')
    creation_date = fields.Date('Creation date')
    state = fields.Selection(
        selection=[('d', 'Draft'), ('s', 'Request sended'), ('cn', 'Canceled'), ('f', 'Finalized'),
                   ('e', 'Error'),
                    ('c', 'Confirmed')], string='State')
    room_category = fields.Many2one('room.categories', string="Room category")
    room_type = fields.Many2one('room.types', string='Room type')
    reservation_detail = fields.One2many('rooming.list', 'reservation_list_id', string="Reservation Detail")
    belongs_to_company = fields.Boolean('Belong to the user\'s current company', compute="_belong_to_company")
    ecart = fields.Float('Ecart', digits=(10, 3))
    observation = fields.Char('Observation')
    ref_fact_vente = fields.Char('Ref.fact.V')
    mnt_vente = fields.Float('Mnt.fact.V', digits=(10, 3))
    coloration = fields.Selection([('danger','red'),('success','green'),('muted','grey'),('warning','yellow'),('info','blue')])

    @api.onchange('fact_hotel')
    def onchange_fac_amount(self):
        for x in self:
            if x.fact_hotel != 0:
                x.update({
                    'ecart': x.fact_hotel - x.net
                })
            else:
                x.update({
                    'ecart': 0
                })

    @api.multi
    @api.depends('company_id')
    def _belong_to_company(self):
        for reservation in self:
            reservation.belong_to_company = (reservation.company_id.id == self.env.user.company_id.id)

    @api.multi
    def calculatenet(self):
        # get the selected reservation lines ids
        recs = []
        num = 0
        active_ids = self.env['ctm.reservation.list'].prepare_reservation()
        # fetch the records from the reservation table one by one with the use of the ids
        kjdfgj = []
        kjdfgj.append(self.id)
        for x in kjdfgj:
            res = self.calculate_prices(x)
            self.env['ctm.reservation.list'].search([('id','=',x)]).update({
                'net': res['net'],
                'brut':res['brut']
            })

    @api.multi
    def opendetails(self):
        return {

            'type': 'ir.actions.act_window',

            'name': 'ctm.reservation.list',

            'view_type': 'form',

            'view_mode': 'form',

            'res_model': self._name,

            'res_id': self.id,

            'target': 'new',

        }

    @api.multi
    def prepare_reservation(self):
        return self._context.get('active_ids')


class touroperator(models.Model):
    _name = 'tour.operator'
    _rec_name = 'name'
    name = fields.Char('Name')
    ito_id = fields.Integer('ID in ITO')
    company_id = fields.Many2one('res.company', string="Company")
    mr_id = fields.Many2one('res.country', string="Market")
    partner_id = fields.Many2one('res.partner', string="Partneaire lié")


class room_type(models.Model):
    _name = 'room.types'
    _rec_name = 'name'

    name = fields.Char('Room Type Name')
    ito_ID = fields.Integer('ID in ITO')


class room_categ(models.Model):
    _name = 'room.categories'
    _rec_name = 'name'

    name = fields.Char('Room category Name')
    ito_ID = fields.Integer('ID in ITO')


class meal(models.Model):
    _name = 'room.meal'
    _rec_name = 'name'

    name = fields.Char('Meal Name')
    ito_ID = fields.Integer('ID in ITO')


class season(models.Model):
    _name = "seasons"
    _rec_name = "name"

    name = fields.Char('Name of the season', required=True)


class allotement(models.Model):
    _name = "allotement"
    _rec_name = "name"

    name = fields.Char('Nom')
    typee = fields.Selection(selection=[('pr', 'Pourcentage'), ('v', 'Valeur fixe')])
    value = fields.Float('Valeur', digits=(10, 3))


class ContractPrices(models.Model):
    _name = 'contract.prices'

    price = fields.Float(string='Prix', digits=(15, 3), required=True)
    season = fields.Many2one('seasons', string='season')
    date_form = fields.Date('Start date', required=True)
    date_to = fields.Date('Date to', required=True)
    prices_table_id = fields.Many2one('contract.price.line')


class ContractPriceLine(models.Model):
    _name = 'contract.price.line'
    _rec_name = 'display_name'

    @api.model
    @api.onchange('type_chambre')
    def set_name(self):
        if self.categ_chambre:
            self.display_name = self.categ_chambre.name

    type_chambre = fields.Many2many('room.types', string="Room size available", required=True)
    ppp_bool = fields.Boolean('Price per room ?')
    categ_chambre = fields.Many2many('room.categories', string="Room category", required=True)
    prices = fields.One2many('contract.prices', 'prices_table_id', string="Prices")
    contract_id = fields.Many2one('contract.contract')
    display_name = fields.Char(default=set_name, store=True)


class Contract(models.Model):
    _name = 'contract.contract'
    _rec_name = "hotel"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Contract management"

    hotel = fields.Many2one('rooming.hotels', string="Hotel", required=True, track_visibility='onchange')
    date_start = fields.Date('Date start', required=True, track_visibility='onchange')
    date_end = fields.Date('Date end', required=True, track_visibility='onchange')
    base_meal = fields.Many2one('room.meal', string="Arrangement de base", track_visibility='onchange')
    min_adult_age = fields.Float('Min adult age', digits=(2, 2), track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string="Devise", track_visibility='onchange')
    company_id = fields.Many2one('res.company', string="Company")
    mr_id = fields.Many2many('res.country', string="Market")
    echeance = fields.Integer('Echeance', track_visibility='onchange')
    prices_table = fields.One2many('contract.price.line', 'contract_id', string="Prices lines",
                                   track_visibility='onchange')
    reductions_lines = fields.One2many('rooming.rule', 'contract_id', string="Rule lines lines",
                                       track_visibility='onchange')
    state = fields.Selection(selection=[('v', 'Valid'), ('s', 'spos entry'), ('p', 'prices entry')],
                             string="state")
    observation = fields.Text('observation', track_visibility='onchange')
    min_enf_age = fields.Float('Min enf age', digits=(2, 2), track_visibility='onchange')

    @api.multi
    def validate_contract(self):
        return self.update({
            'state': 'v'
        })

    @api.multi
    def prices_contract(self):
        return self.update({
            'state': 'p'
        })

    @api.multi
    def spos_contract(self):
        return self.update({
            'state': 's'
        })
