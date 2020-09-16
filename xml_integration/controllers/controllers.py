# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

from odoo import http
from odoo.http import request


class XmlIntegration(http.Controller):
    @http.route('/xml_integration/contract/<model("contract.contract"):obj>', auth='public')
    def index(self, obj, **kw):
        contract = obj
        root = Element('contract')
        tree = ElementTree(root)
        root.set('id', str(obj.id))
        name_hotel = Element('hotel')
        root.append(name_hotel)
        name_hotel.text = str(obj.hotel.name)
        name_company = Element('company')
        root.append(name_company)
        name_company.text = str(obj.company_id.name)
        for room in obj.room_prices:
            room_category = Element('room')
            room_category.set('name', str(room.room.name))
            room_category.set('type', str(room.prices_type))
            for acc in room.accomodations:
                accomodation = Element('accomodation')
                accomodation.set('name', str(acc.code))

                for ml in room.meals:
                    meal = Element('meal')
                    meal.set('name', str(ml.name))
                    accomodation.append(meal)
                    if acc.is_base is True:
                        romm_detail = http.request.env['room.prices.detail'].search(
                            [('room_prices_id', '=', room.id), ('meal', '=', ml.id), ('accomodation', '=', acc.id)])
                        for dt in http.request.env['room.prices.detail.dates'].search(
                                [('room_prices_detail_id', '=', romm_detail.id)]):
                            periode = Element('periode')
                            date_from = Element('date_from')
                            periode.append(date_from)
                            date_from.text = str(dt.date_from)
                            date_to = Element('date_to')
                            periode.append(date_to)
                            date_to.text = str(dt.date_to)
                            age_max = Element('age_max')
                            age_max.text = str(dt.age_max)
                            periode.append(age_max)
                            age_min = Element('age_min')
                            age_min.text = str(dt.age_min)
                            periode.append(age_min)
                            price = Element('price')
                            price.text = str(dt.price)
                            periode.append(price)
                            blocked = Element('blocked')
                            blocked.text = str(dt.blocked)
                            periode.append(blocked)
                            is_relative = Element('is_relative')
                            is_relative.text = str(dt.is_relative)
                            periode.append(is_relative)
                            meal.append(periode)

                    else:
                        romm_detail_other = http.request.env['room.prices.detail.other'].search(
                            [('room_prices_id', '=', room.id), ('meal', '=', ml.id), ('accomodation', '=', acc.id)])
                        for dt in http.request.env['room.prices.detail.dates.other'].search(
                                [('room_prices_detail_id', '=', romm_detail_other.id)]):
                            periode = Element('periode')
                            date_from = Element('date_from')
                            periode.append(date_from)
                            date_from.text = str(dt.date_from)
                            date_to = Element('date_to')
                            periode.append(date_to)
                            date_to.text = str(dt.date_to)
                            age_max = Element('age_max')
                            age_max.text = str(dt.age_max)
                            periode.append(age_max)
                            age_min = Element('age_min')
                            age_min.text = str(dt.age_min)
                            periode.append(age_min)
                            price = Element('price')
                            price.text = str(dt.price)
                            periode.append(price)
                            blocked = Element('blocked')
                            blocked.text = str(dt.blocked)
                            periode.append(blocked)
                            is_relative = Element('is_relative')
                            is_relative.text = str(dt.is_relative)
                            periode.append(is_relative)
                            meal.append(periode)
                    if acc.is_base is True:
                        romm_detail = http.request.env['room.prices.detail'].search(
                            [('room_prices_id', '=', room.id), ('meal', '=', ml.id), ('accomodation', '=', acc.id)])
                        for sp in http.request.env['spo.values'].search(
                                [('room_prices_detail_id', '=', romm_detail.id)]):
                            spo = Element('spo')
                            spo.set('name', str(sp.showed_name))
                            meal.append(spo)
                    else:
                        romm_detail = http.request.env['room.prices.detail.other'].search(
                            [('room_prices_id', '=', room.id), ('meal', '=', ml.id), ('accomodation', '=', acc.id)])
                        for sp in http.request.env['spo.values'].search(
                                [('room_prices_detail_other_id', '=', romm_detail.id)]):
                            spo = Element('spo')
                            spo.set('name', str(sp.showed_name))
                            meal.append(spo)

                room_category.append(accomodation)
            root.append(room_category)

        # print(etree.tostring(root))
        xml = b'<?xml version="1.0" encoding="UTF-8"?>'
        xml = xml + etree.tostring(root)
        xmlhttpheaders = [('Content-Type', 'text/xml'),
                          ('Content-Length', len(xml))]

        return request.make_response(xml, headers=xmlhttpheaders)

    @http.route('/xml_integration/xml_integration/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('xml_integration.listing', {
            'root': '/xml_integration/xml_integration',
            'objects': http.request.env['xml_integration.xml_integration'].search([]),
        })

    @http.route('/xml_integration/xml_integration/objects/<model("xml_integration.xml_integration"):obj>/',
                auth='public')
    def object(self, obj, **kw):
        return http.request.render('xml_integration.object', {
            'object': obj
        })
