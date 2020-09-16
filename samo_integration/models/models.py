# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementT
from datetime import datetime

import pyodbc
import requests

from odoo import models, fields, api
from . import aes_encryptor


class Wizard(models.Model):
    _name = "samo.wizard"
    _description = "wizard of integration"

    def curentstamp_xml(self):
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=currentstamp').text
        root = ElementT.fromstring(str(resultat_xml))
        return root[0][0].get('stamp')

    def state_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.state'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.state'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp

        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=state&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp')
            }
            rec_current = self.env['samo.state'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.state'].create(obj)
            else:
                self.env['samo.state'].modifier(rec_current.id, obj)

    def region_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.region'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.region'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=region&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.region'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            if child.get('state'):
                obj.update({
                    'state': self.env['samo.state'].search([('inc', '=', int(child.get('state')))]).id
                })
            if not rec_current:
                self.env['samo.region'].create(obj)
            else:
                self.env['samo.region'].modifier(rec_current.id, obj)

    def town_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.towns'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.towns'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=town&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))

        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),
            }
            if child.get('state'):
                obj.update({
                    'state': self.env['samo.state'].search([('inc', '=', int(child.get('state')))]).id,
                })
            if child.get('region'):
                obj.update({
                    'region': self.env['samo.region'].search([('inc', '=', int(child.get('region')))]).id
                })
            rec_current = self.env['samo.towns'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:

                self.env['samo.towns'].create(obj)
            else:
                self.env['samo.towns'].modifier(rec_current.id, obj)

    def hotelcategory_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.hotelcategory'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.hotelcategory'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=star&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),
            }
            rec_current = self.env['samo.hotelcategory'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:

                self.env['samo.hotelcategory'].create(obj)
            else:
                self.env['samo.hotelcategory'].modifier(rec_current.id, obj)

    def hotel_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.hotel'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.hotel'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=hotel&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }

            if child.get('star'):
                obj.update(
                    {
                        'star': self.env['samo.hotelcategory'].search([('inc', '=', int(child.get('star')))]).id
                    }
                )

            if child.get('town'):
                obj.update(
                    {
                        'town': self.env['samo.towns'].search([('inc', '=', int(child.get('town')))]).id
                    }
                )
            rec_current = self.env['samo.hotel'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:

                self.env['samo.hotel'].create(obj)
            else:
                self.env['samo.hotel'].modifier(rec_current.id, obj)

    def roomtype_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.roomtype'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.roomtype'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=room&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            rec_current = self.env['samo.roomtype'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:

                self.env['samo.roomtype'].create(obj)
            else:
                self.env['samo.roomtype'].modifier(rec_current.id, obj)

    def allocation_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.allocation'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.allocation'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=htplace&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            if child.get('pcount'):
                obj.update({
                    'pcount': int(child.get('pcount'))
                })
            if child.get('adult'):
                obj.update({
                    'adult': int(child.get('adult'))
                })
            if child.get('child'):
                obj.update({
                    'child': int(child.get('child'))
                })
            if child.get('infant'):
                obj.update({
                    'infant': int(child.get('infant'))
                })
            if child.get('age1min'):
                obj.update({
                    'age1min': float(child.get('age1min'))
                })
            if child.get('age1max'):
                obj.update({
                    'age1max': float(child.get('age1max'))
                })
            if child.get('age2min'):
                obj.update({
                    'age2min': float(child.get('age2min'))
                })
            if child.get('age2max'):
                obj.update({
                    'age2max': float(child.get('age2max'))
                })
            if child.get('age3min'):
                obj.update({
                    'age3min': float(child.get('age3min'))
                })
            if child.get('age3max'):
                obj.update({
                    'age3max': float(child.get('age3max'))
                })
            rec_current = self.env['samo.allocation'].search([('inc', '=', int(child.get('inc')))])

            if not rec_current:

                self.env['samo.allocation'].create(obj)
            else:
                self.env['samo.allocation'].modifier(rec_current.id, obj)

    def meal_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.meal'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.meal'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=meal&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.meal'].search([('inc', '=', int(child.get('inc')))])

            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp')
            }
            if not rec_current:

                self.env['samo.meal'].create(obj)
            else:
                self.env['samo.meal'].modifier(rec_current.id, obj)

    def tour_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.tour'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.tour'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=tour&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.tour'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp')
            }
            if not rec_current:
                self.env['samo.tour'].create(obj)
            else:
                self.env['samo.tour'].modifier(rec_current.id, obj)

    def port_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.state'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.state'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=port&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.port'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp')
            }

            if child.get('town'):
                obj.update({
                    'town': self.env['samo.towns'].search([('inc', '=', int(child.get('town')))]).id
                })
            if not rec_current and child.get('status') != 'D':
                self.env['samo.port'].create(obj)
            elif child.get('status') == 'D':
                self.env['samo.port'].supprimer(rec_current.id)
            elif rec_current.stamp != child.get('stamp'):
                self.env['samo.port'].modifier(rec_current.id, obj)

    def freights_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.freights'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.freights'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=freight&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.freights'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),
                'trantype': child.get('trantype')
            }

            if child.get('source'):
                obj.update({
                    'source': self.env['samo.towns'].search([('inc', '=', int(child.get('source')))]).id
                })
            if child.get('srcport'):
                obj.update({
                    'srcport': self.env['samo.port'].search([('inc', '=', int(child.get('srcport')))]).id
                })
            if child.get('target'):
                obj.update({
                    'target': self.env['samo.towns'].search([('inc', '=', int(child.get('target')))]).id
                })
            if child.get('trgport'):
                obj.update({
                    'trgport': self.env['samo.port'].search([('inc', '=', int(child.get('trgport')))]).id
                })
            if not rec_current:
                self.env['samo.freights'].create(obj)
            else:
                self.env['samo.freights'].modifier(rec_current.id, obj)

    def freightsclass_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.freightsclass'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.freightsclass'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=class&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.freightsclass'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp')
            }
            if not rec_current:
                self.env['samo.freightsclass'].create(obj)
            else:
                self.env['samo.freightsclass'].modifier(rec_current.id, obj)

    def release_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.release'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.release'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=release&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            rec_current = self.env['samo.release'].search([('inc', '=', int(child.get('inc')))])
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            if child.get('hotel'):
                obj.update({
                    'hotel': self.env['samo.hotel'].search([('inc', '=', int(child.get('hotel')))]).id
                })
            if child.get('datebeg'):
                obj.update({
                    'datebeg': datetime.strptime(child.get('datebeg'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('dateend'):
                obj.update({
                    'dateend': datetime.strptime(child.get('dateend'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('days'):
                obj.update({
                    'days': int(child.get('days'))
                })
            if not rec_current:
                self.env['samo.release'].create(obj)
            else:
                self.env['samo.release'].modifier(rec_current.id, obj)

    def servtype_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.servtype'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.servtype'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=servtype&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            rec_current = self.env['samo.servtype'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.servtype'].create(obj)
            else:
                self.env['samo.servtype'].modifier(rec_current.id, obj)

    def service_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()
        for x in self.env['samo.service'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.service'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=service&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            if child.get('servtype'):
                obj.update({
                    'servtype': self.env['samo.servtype'].search([('inc', '=', int(child.get('servtype')))]).id
                })
            rec_current = self.env['samo.service'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.service'].create(obj)
            else:
                self.env['samo.service'].modifier(rec_current.id, obj)

    def spos_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()
        for x in self.env['samo.spos'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.spos'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=spos&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        while len(root[0]) > 0:
            for x in self.env['samo.spos'].search([('status', '=', '')]):
                if last_stamp < x.stamp:
                    last_stamp = x.stamp
            for x in self.env['samo.spos'].search([('status', '=', 'D')]):
                if del_stamp < x.stamp:
                    del_stamp = x.stamp
            resultat_xml = requests.get(
                'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=spos&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
            root = ElementT.fromstring(str(resultat_xml))
            for child in root[0]:
                rec_current = self.env['samo.spos'].search([('inc', '=', int(child.get('inc')))])
                obj = {
                    'inc': int(child.get('inc')),
                    'status': child.get('status'),
                    'name': child.get('name'),
                    'lname': child.get('lname'),
                    'alias': child.get('alias'),
                    'stamp': child.get('stamp'),
                    'mixed': child.get('mixed'),
                    'usecontract': child.get('usecontract'),
                    'ebooking': child.get('ebooking'),
                    'usesaleprice': child.get('usesaleprice'),
                    'note': child.get('note'),

                }
                if child.get('number'):
                    obj.update({
                        'number': int(child.get('number')),
                    })
                if child.get('spodate'):
                    obj.update({
                        'spodate': datetime.strptime(child.get('spodate'), '%Y-%m-%dT%H:%M:%S').date(),
                    })
                if int(child.get('number')) == 14348:
                    raise ('found it ! {0}'.format(child.get('inc')))
                if not rec_current:
                    self.env['samo.spos'].create(obj)

                else:
                    self.env['samo.spos'].modifier(rec_current.id, obj)

    def currency_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.currency'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.currency'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        resultat_xml = requests.get(
            'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=currency&laststamp=' + last_stamp + '&delstamp=' + del_stamp).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),
                'name': child.get('name'),
                'lname': child.get('lname'),
                'alias': child.get('alias'),
                'stamp': child.get('stamp'),

            }
            rec_current = self.env['samo.currency'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.currency'].create(obj)
            else:
                self.env['samo.currency'].modifier(rec_current.id, obj)

    def stopsale_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.stopsale'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.stopsale'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        url = 'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=stopsale&laststamp=' + last_stamp + '&delstamp=' + del_stamp
        resultat_xml = requests.post(url, data={'partner_token': self.gettoken_xml()}).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),

                'stamp': child.get('stamp'),
                'note': child.get('note')
            }
            if child.get('hotel'):
                obj.update({
                    'hotel': self.env['samo.hotel'].search([('inc', '=', int(child.get('hotel')))]).id
                })
            if child.get('room'):
                obj.update({
                    'room': self.env['samo.roomtype'].search([('inc', '=', int(child.get('room')))]).id
                })
            if child.get('meal'):
                obj.update({
                    'meal': self.env['samo.meal'].search([('inc', '=', int(child.get('meal')))]).id
                })
            if child.get('htplace'):
                obj.update({
                    'htplace': self.env['samo.allocation'].search([('inc', '=', int(child.get('htplace')))]).id
                })
            if child.get('datebeg'):
                obj.update({
                    'datebeg': datetime.strptime(child.get('datebeg'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('dateend'):
                obj.update({
                    'dateend': datetime.strptime(child.get('dateend'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('issue'):
                obj.update({
                    'issue': datetime.strptime(child.get('issue'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('rqdatebeg'):
                obj.update({
                    'rqdatebeg': datetime.strptime(child.get('rqdatebeg'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('rqdateend'):
                obj.update({
                    'rqdateend': datetime.strptime(child.get('rqdateend'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('checkin'):
                if child.get('checkin') == '1':
                    obj.update({
                        'checkin': True
                    })
            rec_current = self.env['samo.stopsale'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.stopsale'].create(obj)
            else:
                self.env['samo.stopsale'].modifier(rec_current.id, obj)

    def hotelsalepr_xml(self):
        import xlwt
        workbook_creation = xlwt.Workbook()
        del_stamp = self.curentstamp_xml()
        token = self.gettoken_xml()
        for x in self.env['samo.hotel'].search([]):
            last_stamp = '0x0000000000000000'

            test_creation = False
            test_update = False
            nbre_record_create = 0
            nbre_record_update = 0
            body_str = ''
            body_str_update = ''

            for x1 in self.env['samo.hotelsalepr'].search([('hotel', '=', x.id)]):
                if last_stamp < x1.stamp:
                    last_stamp = x1.stamp
            for x1 in self.env['samo.hotelsalepr'].search([('status', '=', 'D'), ('hotel', '=', x.id)]):
                if del_stamp < x1.stamp:
                    del_stamp = x1.stamp
            url = 'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=hotelsalepr&hotel={0}&laststamp='.format(
                x.inc) + last_stamp + '&delstamp=' + del_stamp
            try:
                resultat_xml = requests.post(url, data={'partner_token': token}).text
            except:
                raise UserWarning('something is wrong ')
            root = ElementT.fromstring(str(resultat_xml))
            if len(root[0]) > 1:
                sheet_hotel = workbook_creation.add_sheet(x.name)
                sheet_hotel.write(0, 0, 'inc')
                sheet_hotel.write(0, 1, 'status')
                sheet_hotel.write(0, 2, 'stamp')
                sheet_hotel.write(0, 3, 'itoid')
                sheet_hotel.write(0, 4, 'hotel')
                sheet_hotel.write(0, 5, 'room')
                sheet_hotel.write(0, 6, 'allocation')
                sheet_hotel.write(0, 7, 'meal')
                sheet_hotel.write(0, 8, 'date begin')
                sheet_hotel.write(0, 9, 'date end')
            while len(root[0]) > 1:

                for x1 in self.env['samo.hotelsalepr'].search([('hotel', '=', x.id)]):
                    if last_stamp < x1.stamp:
                        last_stamp = x1.stamp
                for x1 in self.env['samo.hotelsalepr'].search([('status', '=', 'D'), ('hotel', '=', x.id)]):
                    if del_stamp < x1.stamp:
                        del_stamp = x1.stamp
                url = 'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=hotelsalepr&hotel={0}&laststamp='.format(
                    x.inc) + last_stamp + '&delstamp=' + del_stamp
                resultat_xml = requests.post(url, data={'partner_token': token}).text
                root = ElementT.fromstring(str(resultat_xml))
                for child in root[0]:

                    if child.get('inc'):
                        obj = {
                            'inc': int(child.get('inc')),
                            'status': child.get('status'),

                            'stamp': child.get('stamp'),
                            'useascheckin': child.get('useascheckin'),
                            'days': child.get('days'),
                            'spotype': child.get('spotype'),
                            'sposubtype': child.get('sposubtype'),
                            'oncheckin': child.get('oncheckin')

                        }
                        if child.get('hotel'):
                            obj.update({
                                'hotel': self.env['samo.hotel'].search([('inc', '=', int(child.get('hotel')))]).id
                            })
                        if child.get('room'):
                            obj.update({
                                'room': self.env['samo.roomtype'].search([('inc', '=', int(child.get('room')))]).id
                            })
                        if child.get('htplace'):
                            obj.update({
                                'htplace': self.env['samo.allocation'].search(
                                    [('inc', '=', int(child.get('htplace')))]).id
                            })
                        if child.get('rroom'):
                            obj.update({
                                'rroom': self.env['samo.roomtype'].search([('inc', '=', int(child.get('rroom')))]).id
                            })
                        if child.get('rmeal'):
                            obj.update({
                                'rmeal': self.env['samo.meal'].search([('inc', '=', int(child.get('rmeal')))]).id
                            })
                        if child.get('rhtplace'):
                            obj.update({
                                'rhtplace': self.env['samo.allocation'].search(
                                    [('inc', '=', int(child.get('rhtplace')))]).id
                            })
                        if child.get('meal'):
                            obj.update({
                                'meal': self.env['samo.meal'].search([('inc', '=', int(child.get('meal')))]).id
                            })
                        if child.get('spos'):
                            obj.update({
                                'spos': self.env['samo.spos'].search([('inc', '=', int(child.get('spos')))]).id
                            })
                        if child.get('currency'):
                            obj.update({
                                'currency': self.env['samo.currency'].search(
                                    [('inc', '=', int(child.get('currency')))]).id
                            })
                        if child.get('datebeg'):
                            obj.update({
                                'datebeg': datetime.strptime(child.get('datebeg'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('dateend'):
                            obj.update({
                                'dateend': datetime.strptime(child.get('dateend'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('rqdatebeg'):
                            obj.update({
                                'rqdatebeg': datetime.strptime(child.get('rqdatebeg'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('rqdateend'):
                            obj.update({
                                'rqdateend': datetime.strptime(child.get('rqdateend'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('dateinfrom'):
                            obj.update({
                                'dateinfrom': datetime.strptime(child.get('dateinfrom'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('dateoutfrom'):
                            obj.update({
                                'dateoutfrom': datetime.strptime(child.get('dateoutfrom'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('dateintill'):
                            obj.update({
                                'dateintill': datetime.strptime(child.get('dateintill'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('dateouttill'):
                            obj.update({
                                'dateouttill': datetime.strptime(child.get('dateouttill'), '%Y-%m-%dT%H:%M:%S').date()
                            })
                        if child.get('price'):
                            obj.update({
                                'price': float(child.get('price')),
                            })
                        if child.get('discount'):
                            obj.update({
                                'discount': float(child.get('discount')),
                            })
                        if child.get('discountmoney'):
                            obj.update({
                                'discountmoney': float(child.get('discountmoney')),
                            })
                        if child.get('adult'):
                            obj.update({
                                'adult': float(child.get('adult')),
                            })
                        if child.get('child'):
                            obj.update({
                                'child': float(child.get('child')),
                            })
                        if child.get('nobedchild'):
                            obj.update({
                                'nobedchild': float(child.get('nobedchild')),
                            })
                        if child.get('nights'):
                            obj.update({
                                'nights': int(child.get('nights')),
                            })
                        if child.get('rnights'):
                            obj.update({
                                'rnights': int(child.get('rnights')),
                            })
                        if child.get('rqdaysfrom'):
                            obj.update({
                                'rqdaysfrom': int(child.get('rqdaysfrom')),
                            })
                        if child.get('rqdaystill'):
                            obj.update({
                                'rqdaystill': int(child.get('rqdaystill')),
                            })
                        if child.get('nightsfrom'):
                            obj.update({
                                'nightsfrom': int(child.get('nightsfrom')),
                            })
                        if child.get('nightstill'):
                            obj.update({
                                'nightstill': int(child.get('nightstill')),
                            })
                        rec_current = self.env['samo.hotelsalepr'].search([('inc', '=', int(child.get('inc')))])
                        if child.get('status') != "D":
                            if not rec_current:
                                new_record = self.env['samo.hotelsalepr'].create(obj)

                                nbre_record_create = nbre_record_create + 1
                                sheet_hotel.write(nbre_record_create, 0, str(new_record.inc))
                                sheet_hotel.write(nbre_record_create, 1, str(new_record.status))
                                sheet_hotel.write(nbre_record_create, 2, str(new_record.stamp))
                                sheet_hotel.write(nbre_record_create, 3, str(new_record.itoid))
                                sheet_hotel.write(nbre_record_create, 4, str(new_record.hotel.name))
                                sheet_hotel.write(nbre_record_create, 5, str(new_record.room.name))
                                sheet_hotel.write(nbre_record_create, 6, str(new_record.htplace.name))
                                sheet_hotel.write(nbre_record_create, 7, str(new_record.meal.name))
                                sheet_hotel.write(nbre_record_create, 8, str(new_record.datebeg))
                                sheet_hotel.write(nbre_record_create, 9, str(new_record.dateend))
                                body_str = body_str + """
                                    <html>
                                    <table border="1">
                           <tr>
                              <th>Name of attribute</th>
                              <th>New value</th>
                           </tr>
                           <tr>
                              <td>inc</td>
                              <td>{0}</td>
                           </tr>
                           <tr>
                              <td>status</td>
                              <td>{1}</td>
                           </tr>
    
                           <tr>
                              <td>stamp</td>
                              <td>{2}</td>
                           </tr>
                           <tr>
                              <td>ito id</td>
                              <td>{3}</td>
                           </tr>
                           <tr>
                              <td>hotel</td>
                              <td>{4}</td>
                           </tr>
                           <tr>
                              <td>room</td>
                              <td>{5}</td>
                           </tr>
                           <tr>
                              <td>allocation</td>
                              <td>{6}</td>
                           </tr>
                           <tr>
                              <td>meal</td>
                              <td>{7}</td>
                           </tr>
                           <tr>
                              <td>date begin</td>
                              <td>{8}</td>
                           </tr>
                           <tr>
                              <td>date end</td>
                              <td>{9}</td>
                           </tr>
                           <tr>
                              <td>Spo Reservation from</td>
                              <td>{10}</td>
                           </tr>
                           <tr>
                              <td>Spo Reservation till</td>
                              <td>{11}</td>
                           </tr>
                           <tr>
                              <td>Staying nights</td>
                              <td>{12}</td>
                           </tr>
                           <tr>
                              <td>Spos</td>
                              <td>{13}</td>
                           </tr>
                           <tr>
                              <td>Spos type</td>
                              <td>{14}</td>
                           </tr>
                           <tr>
                              <td>Spos subtype</td>
                              <td>{15}</td>
                           </tr>
                           <tr>
                              <td>Spos room type</td>
                              <td>{16}</td>
                              
                           </tr>
                           <tr>
                              <td>Spos allocation</td>
                              <td>{17}</td>
                           </tr>
                           <tr>
                              <td>Spos meal</td>
                              <td>{18}</td>
                           </tr>
                           <tr>
                              <td>Spos rotation night</td>
                              <td>{19}</td>
                           </tr>
                           <tr>
                              <td>price</td>
                              <td>{20}</td>
                           </tr>
                           <tr>
                              <td>Currency</td>
                              <td>{21}</td>
                           </tr>
                           <tr>
                              <td>checkin date from</td>
                              <td>{22}</td>
                           </tr>
                           <tr>
                              <td>checkout date from</td>
                              <td>{23}</td>
                           </tr>
                           <tr>
                              <td>checkin date till</td>
                              <td>{24}</td>
                           </tr>
                           <tr>
                              <td>checkout date till</td>
                              <td>{25}</td>
                           </tr>
                           <tr>
                              <td>discount if percent</td>
                              <td>{26}</td>
                           </tr>
                           <tr>
                              <td>discount in money</td>
                              <td>{27}</td>
                           </tr>
                           <tr>
                              <td>Use as checkin</td>
                              <td>{28}</td>
                           </tr>
                           <tr>
                              <td>Spo Days before check-in from</td>
                              <td>{29}</td>
                           </tr>
                           <tr>
                              <td>Spo Days before check-in till</td>
                              <td>{30}</td>
                           </tr>
                           <tr>
                              <td>Nights from</td>
                              <td>{31}</td>
                           </tr>
                           <tr>
                              <td>Nights till</td>
                              <td>{32}</td>
                           </tr>
                           <tr>
                              <td>spo rotation</td>
                              <td>{33}</td>
                           </tr>
                           <tr>
                              <td>Supplement for adult</td>
                              <td>{34}</td>
                           </tr>
                           <tr>
                              <td>Supplement for child with bed</td>
                              <td>{35}</td>
                           </tr>
                           <tr>
                              <td>Supplement for child without bed</td>
                              <td>{36}</td>
                           </tr>
                           <tr>
                              <td>week days</td>
                              <td>{37}</td>
                           </tr>
                        </table>
                        </html>
                                    """.format(
                                    str(new_record.inc),
                                    str(new_record.status),
                                    str(new_record.stamp),
                                    str(new_record.itoid),
                                    str(new_record.hotel.name),
                                    str(new_record.room.name),
                                    str(new_record.htplace.name),
                                    str(new_record.meal.name),
                                    str(new_record.datebeg),
                                    str(new_record.dateend),
                                    str(new_record.rqdatebeg),
                                    str(new_record.rqdateend),
                                    str(new_record.nights),
                                    str(new_record.spos.name),
                                    str(new_record.spotype),
                                    str(new_record.sposubtype),
                                    str(new_record.rroom.name),
                                    str(new_record.rhtplace.name),
                                    str(new_record.rmeal.name),
                                    str(new_record.rnights),
                                    str(new_record.price),
                                    str(new_record.currency.name),
                                    str(new_record.dateinfrom),
                                    str(new_record.dateoutfrom),
                                    str(new_record.dateintill),
                                    str(new_record.dateouttill),
                                    str(new_record.discount),
                                    str(new_record.discountmoney),
                                    str(new_record.useascheckin),
                                    str(new_record.rqdaysfrom),
                                    str(new_record.rqdaystill),
                                    str(new_record.nightsfrom),
                                    str(new_record.nightstill),
                                    str(new_record.oncheckin),
                                    str(new_record.adult),
                                    str(new_record.child),
                                    str(new_record.nobedchild),
                                    str(new_record.days))
                                test_creation = False

                            else:
                                self.env['samo.hotelsalepr'].modifier(rec_current.id, obj)
                                nbre_record_update = nbre_record_update +1
                                body_str_update = body_str_update + """<html>
                <table border="1">
       <tr>
          <th>Name of attribute</th>
          <th>Old value</th>
          <th>New value</th>
       </tr>
       <tr>
          <td>inc</td>
          <td>{0}</td>
          <td>{1}</td>
       </tr>
       <tr>
          <td>status</td>
          <td>{2}</td>
          <td>{3}</td>
       </tr>
       
       <tr>
          <td>stamp</td>
          <td>{4}</td>
          <td>{5}</td>
       </tr>
       <tr>
          <td>ito id</td>
          <td>{6}</td>
          <td>not exist</td>
       </tr>
       <tr>
          <td>hotel</td>
          <td>{7}</td>
          <td>{8}</td>
       </tr>
       <tr>
          <td>room</td>
          <td>{9}</td>
          <td>{10}</td>
       </tr>
       <tr>
          <td>allocation</td>
          <td>{11}</td>
          <td>{12}</td>
       </tr>
       <tr>
          <td>meal</td>
          <td>{13}</td>
          <td>{14}</td>
       </tr>
       <tr>
          <td>date begin</td>
          <td>{15}</td>
          <td>{16}</td>
       </tr>
       <tr>
          <td>date end</td>
          <td>{17}</td>
          <td>{18}</td>
       </tr>
       <tr>
          <td>Spo Reservation from</td>
          <td>{19}</td>
          <td>{20}</td>
       </tr>
       <tr>
          <td>Spo Reservation till</td>
          <td>{21}</td>
          <td>{22}</td>
       </tr>
       
       <tr>
          <td>price</td>
          <td>{23}</td>
          <td<{24}</td>
          
       </tr>
      
       </tr>
    </table>
    </html>
                """.format(
                                    str(rec_current.inc), str(obj['inc']),
                                    str(rec_current.status), obj['status'],
                                    str(rec_current.stamp), obj['stamp'],
                                    str(rec_current.hotel.name), str(obj['hotel']),
                                    str(rec_current.hotel.name), str(obj['hotel']),
                                    str(rec_current.room.name), str(obj['room']),
                                    str(rec_current.htplace.name), str(obj['htplace']),
                                    str(rec_current.meal.name), str(obj['meal']),
                                    str(rec_current.datebeg), str(obj['datebeg']),
                                    str(rec_current.dateend), str(obj['dateend']),
                                    str(rec_current.rqdatebeg), str(obj['rqdatebeg']),
                                    str(rec_current.rqdateend), str(obj['rqdateend']),

                                    str(rec_current.price), str(obj['price']),

                                )
                                test_update = False

            # IrMailServer = self.env['ir.mail_server']
            # smtp_session = self.env['ir.mail_server'].connect()
            # list_mail = []
            # for mail in self.env['samo.configuration'].search([]):
            #     list_mail.append(mail.mail_name)
            # if test_creation:
            #     # workbook_creation.save('/home/dev01/Bureau/notifications.xlsx')
            #     body_str1 = """Dears , {0} new vals were added in hotel {1} <br></br>""".format(str(nbre_record_create),
            #                                                                                     x.name)
            #
            #     msg1 = IrMailServer.build_email(
            #         email_from='notifications@ctmvoyages.com',
            #         email_to=list_mail,
            #         subject='Price creation',
            #         body=body_str1 + body_str,
            #         object_id=False,
            #         subtype='html',
            #         subtype_alternative='html',
            #         # attachments=['C:\Users\Aouili nizar\Desktop\create_notifications.xlsx']
            #     )
            #     res = IrMailServer.send_email(msg1, smtp_session=smtp_session)
            # if test_update:
            #     # workbook_creation.save('/home/dev01/Bureau/notifications.xlsx')
            #     body_str_update1 = """Dears , {0}  vals were updated in hotel {1} <br></br>""".format(
            #         str(nbre_record_update),
            #         x.name)
            #
            #     msg = IrMailServer.build_email(
            #         email_from='notifications@ctmvoyages.com',
            #         email_to=list_mail,
            #         subject='Price updates',
            #         body=body_str_update1 + body_str_update,
            #         object_id=False,
            #         subtype='html',
            #         subtype_alternative='html',
            #         # attachments=['C:\Users\Aouili nizar\Desktop\create_notifications.xlsx']
            #     )
            #     res = IrMailServer.send_email(msg, smtp_session=smtp_session)
            # # smtp_session.quit()

    def servicesalepr_xml(self):
        last_stamp = '0x0000000000000000'
        del_stamp = self.curentstamp_xml()

        for x in self.env['samo.servicesalepr'].search([('status', '=', '')]):
            if last_stamp < x.stamp:
                last_stamp = x.stamp
        for x in self.env['samo.servicesalepr'].search([('status', '=', 'D')]):
            if del_stamp < x.stamp:
                del_stamp = x.stamp
        url = 'http://89.179.242.39/incoming/export/default.php?samo_action=reference&form=http://samo.ru&type=servicesalepr&laststamp=' + last_stamp + '&delstamp=' + del_stamp
        resultat_xml = requests.post(url, data={'partner_token': self.gettoken_xml()}).text
        root = ElementT.fromstring(str(resultat_xml))
        for child in root[0]:
            obj = {
                'inc': int(child.get('inc')),
                'status': child.get('status'),

                'stamp': child.get('stamp'),
                'pernight': child.get('pernight'),
                'spotype': child.get('spotype'),
                'grouphotel': child.get('grouphotel')

            }
            if child.get('service'):
                obj.update({
                    'service': self.env['samo.service'].search([('inc', '=', int(child.get('service')))]).id
                })
            if child.get('hotel'):
                obj.update({
                    'hotel': self.env['samo.hotel'].search([('inc', '=', int(child.get('hotel')))]).id
                })
            if child.get('townfrom'):
                obj.update({
                    'townfrom': self.env['samo.towns'].search([('inc', '=', int(child.get('townfrom')))]).id
                })
            if child.get('townto'):
                obj.update({
                    'townto': self.env['samo.towns'].search([('inc', '=', int(child.get('townto')))]).id
                })
            if child.get('currency'):
                obj.update({
                    'currency': self.env['samo.currency'].search([('inc', '=', int(child.get('currency')))]).id
                })
            if child.get('price'):
                obj.update({
                    'price': float(child.get('price')),
                })
            if child.get('adultpr'):
                obj.update({
                    'adultpr': float(child.get('adultpr')),
                })
            if child.get('child1pr'):
                obj.update({
                    'child1pr': float(child.get('child1pr')),
                })
            if child.get('age1min'):
                obj.update({
                    'age1min': float(child.get('age1min')),
                })
            if child.get('age1max'):
                obj.update({
                    'age1max': float(child.get('age1max')),
                })
            if child.get('child2pr'):
                obj.update({
                    'child2pr': float(child.get('child2pr')),
                })
            if child.get('age2min'):
                obj.update({
                    'age2min': float(child.get('age2min')),
                })
            if child.get('age2max'):
                obj.update({
                    'age2max': float(child.get('age2max')),
                })
            if child.get('paxfrom'):
                obj.update({
                    'paxfrom': child.get('paxfrom')
                })
            if child.get('paxtill'):
                obj.update({
                    'paxtill': child.get('paxtill')
                })
            if child.get('nights'):
                obj.update({
                    'nights': child.get('nights')
                })
            if child.get('datebeg'):
                obj.update({
                    'datebeg': datetime.strptime(child.get('datebeg'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('dateend'):
                obj.update({
                    'dateend': datetime.strptime(child.get('dateend'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('rdatebeg'):
                obj.update({
                    'rdatebeg': datetime.strptime(child.get('rdatebeg'), '%Y-%m-%dT%H:%M:%S').date()
                })
            if child.get('rdateend'):
                obj.update({
                    'rdateend': datetime.strptime(child.get('rdateend'), '%Y-%m-%dT%H:%M:%S').date()
                })
            rec_current = self.env['samo.servicesalepr'].search([('inc', '=', int(child.get('inc')))])
            if not rec_current:
                self.env['samo.servicesalepr'].create(obj)
            else:
                self.env['samo.servicesalepr'].modifier(rec_current.id, obj)

    def gettoken_xml(self):
        pass_word = self.get_password()
        url = 'http://89.179.242.39/incoming/export/default.php?samo_action=auth'
        login = 'Startax'
        resultat_xml = requests.post(url, data={'login': login, 'passwordDigest': pass_word}).text
        try:
            root = ElementT.fromstring(str(resultat_xml))
        except:
            raise UserWarning('something wrong happened')

        return root[0][0].get('partner_token')

    def get_password(self):
        passw = "St@25648"
        key = "c132b4bc6a48e054770af7b1f925d95c"
        obj = aes_encryptor.Main(key=False, password=False)
        passdigest = obj.aesencrypt()

        return passdigest

    def synchronize_all_records(self):
        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select CHN_KEY from Prices_HotelNet"
        hotelsalepr_ito = []
        hotelsalepr_odoo = []
        max_id = 0
        for x in self.env['samo.hotelsalepr'].search([('itoid', '=', False), ('spotype', '!=', 3), ('spotype', '!=', 6)]):
            hotelsalepr_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            hotelsalepr_ito.append({
                'id': row[0],
            })
            if max_id < row[0]:
                max_id = row[0]
        # get assignement last ID before processing :

        assn = 0
        n1 = 0
        n = 0

        t = 0
        for x in hotelsalepr_odoo:
            ass_id = 0
            spo_id = 0
            sql_querry = "select ID from Assignment"
            cursor1.execute(sql_querry)
            for row in cursor1:
                if ass_id < row[0]:
                    ass_id = row[0]
            sql_querry = "select SPO_KEY from SPOLIST"
            cursor1.execute(sql_querry)
            for row in cursor1:
                if spo_id < row[0]:
                    spo_id = row[0]
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                n1 = ass_id + 1
                # some tests to make sure all relations already in the table assignement with that partner
                # test if there is a link between the partner and the accomodation if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 3 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.htplace.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (3,{0},{1},{2})'''.format(x.hotel.itoid, x.htplace.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                # test if there is a link between the partner and the room category if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 2 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.room.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (2,{0},{1},{2})'''.format(x.hotel.itoid, x.room.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                # test if there is a link between the partner and the meal if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 4 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.meal.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (4,{0},{1},{2})'''.format(x.hotel.itoid, x.meal.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1

                # some adjustement to some variables to fit ito format or foreign key
                rtkey = 0
                ad = x.htplace.adult
                if ad == 1:
                    rtkey = 24
                if ad == 2:
                    rtkey = 1
                if ad == 3:
                    rtkey = 25
                if ad == 4:
                    rtkey = 26
                if ad == 5:
                    rtkey = 28
                if ad == 6:
                    rtkey = 62
                # test if there is a link between the partner and the room type if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 1 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, rtkey)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (1,{0},{1},{2})'''.format(x.hotel.itoid, rtkey, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                week = 'null'
                formula = "Price = {0}".format(x.price)
                dateinfrom = 'null'
                if x.dateinfrom:
                    dateinfrom = datetime.strftime(x.dateinfrom, "%d/%m/%Y")
                dateintill = 'null'
                if x.dateintill:
                    dateintill = datetime.strftime(x.dateintill, "%d/%m/%Y")
                # some checks for spo to insert them later inside the boo :')
                # if no spo in the samo rec ; generate spo , create it and link it with the price
                spostr = ""
                spo_type = 1
                if x.spos.number == 0:
                    spo_id = 0

                # else just get the id of the spo and link it ( supposebly it's already synchronized)
                else:
                    spo_id = x.spos.itoid
                queryy = '''insert into Prices_HotelNet 
                (CHN_NETTO,
                 CHN_RATENETTO, 
                 CHN_DATEBEGIN, 
                 CHN_DATEEND, 
                 CHN_RELDAYS, 
                 CHN_RCKEY, 
                 CHN_RTKEY, 
                 CHN_PRKEY, 
                 CHN_PNKEY, 
                 CHN_SPKEY, 
                 CHN_KEY, 
                 CHN_CONTRACTPRKEY, 
                 CHN_TYPE, 
                 CHN_WEEK, 
                 CHN_ACKEY, 
                 CHN_SPOKEY, 
                 CHN_MRKEY, 
                 CHN_DurationMin, 
                 CHN_DurationMax, 
                 CHN_FillFormula, 
                 CHN_FreeNights, 
                 CHN_BookingDateBegin, 
                 CHN_BookingDateEnd, 
                 CHN_BookingCode) 
                values (
                {0} ,'{1}' ,'{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, {10},
                {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, '{19}', {20},
                {21}, {22}, {23}
                );
                '''.format(x.price,
                           x.currency.alias,
                           datetime.strftime(x.datebeg, "%d/%m/%Y"),
                           datetime.strftime(x.dateend, "%d/%m/%Y"),
                           7,
                           x.room.itoid,
                           rtkey,
                           x.hotel.itoid,
                           x.meal.itoid,
                           spo_id,
                           n,
                           x.hotel.itoid,
                           1,
                           week,
                           x.htplace.itoid,
                           spo_id,
                           12,
                           x.nightsfrom,
                           x.nightstill,
                           formula,
                           'null',
                           dateinfrom,
                           dateintill,
                           'null')
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        sql_querry = '''update Keys set ID = {0} where Key_TABLE = 'Prices_HotelNet' '''.format(n + 1)
        cursor1.execute('commit;')


class State(models.Model):
    _name = "samo.state"
    _rec_name = "name"
    _description = "list of states"

    inc = fields.Integer('id in samo')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    itoid = fields.Char('ID in ITO')

    def supprimer(self, id):
        rec_unlink = self.env['samo.state'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        filename = '/home/dev01/Bureau/notifications.xlsx'
        contentfileemail = open(filename)
        rec_update = self.env['samo.state'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = IrMailServer.connect()
        msg = IrMailServer.build_email(
            email_from='notification@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration state',
            # body='state update data , id in ito =' + str(rec_update.itoid),
            body="""<html>
            <table border="1">
   <tr>
      <th>Name of attribute</th>
      <th>Old value</th>
      <th>New value</th>
   </tr>
   <tr>
      <td>inc</td>
      <td>{0}</td>
      <td>{1}</td>
   </tr>
   <tr>
      <td>status</td>
      <td>{2}</td>
      <td>{3}</td>
   </tr>
   <tr>
      <td>name</td>
      <td>{4}</td>
      <td>{5}</td>
   </tr>
   <tr>
      <td>lname</td>
      <td>{6}</td>
      <td>{7}</td>
   </tr>
   <tr>
      <td>alias</td>
      <td>{8}</td>
      <td>{9}</td>
   </tr>
   <tr>
      <td>stamp</td>
      <td>{10}</td>
      <td>{11}</td>
   </tr>
   <tr>
      <td>ito id</td>
      <td>{12}</td>
      <td>not exist</td>
   </tr>
   
</table>
</html>
            """.format(str(rec_update.inc), str(obj['inc']), str(rec_update.status), obj['status'],
                       str(rec_update.name), obj['name'], str(rec_update.lname), obj['lname'],
                       str(rec_update.alias), obj['alias'], str(rec_update.stamp), obj['stamp'], rec_update.itoid),
            object_id=False,
            subtype='html',
            subtype_alternative='plain',
            attachments=[(filename,contentfileemail,'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')])
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        ####################################################
        sql_querry = "select CN_KEY,CN_NAME from country"
        states_ito = []
        states_odoo = []
        max_id = 0
        n = 0
        for x in self.env['samo.state'].search([('id', 'in', self._context.get('active_ids'))]):
            states_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            states_ito.append({
                'id': row[0],
                'name': row[1]
            })
            if max_id < row[0]:
                max_id = row[0]
        for x in states_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = "insert into country (CN_KEY,CN_NAME) values ({0},'{1}');commit;".format((n), x.name)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > '0':
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'COUNTRY';commit;'''.format(n + 1)
        cursor1.execute(queryy)
        ##################################################


class Region(models.Model):
    _name = "samo.region"
    _rec_name = "name"
    _description = "list of regions"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    state = fields.Many2one("samo.state", string='state')

    def supprimer(self, id):
        rec_unlink = self.env['samo.region'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.region'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='region update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):
        import pyodbc
        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select RG_KEY,RG_NAME from region"
        regions_ito = []
        regions_odoo = []
        max_id = 0
        for x in self.env['samo.region'].search([('id', 'in', self._context.get('active_ids'))]):
            regions_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            regions_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in regions_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into REGION 
                (RG_KEY,RG_NAME,RG_CODE,RG_CNKEY,RG_ShowInHotelSearch,RG_ShowInTransferSearch,RG_ShowInExcursionSearch,
                 RG_ShowInTourSearch) 
                values ({0},'{1}','',{2},DEFAULT, DEFAULT, DEFAULT, DEFAULT);
                commit;'''.format((n), x.name, x.state.itoid)
                try:
                    cursor1.execute(queryy)
                except:
                    raise UserWarning('error in query : {0}'.format(queryy))
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'REGION';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Towns(models.Model):
    _name = "samo.towns"
    _rec_name = "name"
    _description = "list of towns"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    state = fields.Many2one('samo.state', string='state')
    region = fields.Many2one('samo.region', string='region')

    def supprimer(self, id):
        rec_unlink = self.env['samo.towns'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.towns'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='towns update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):
        import pyodbc
        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select CT_KEY,CT_NAME from CITYDICTIONARY"
        towns_ito = []
        towns_odoo = []
        max_id = 0
        for x in self.env['samo.towns'].search([('id', 'in', self._context.get('active_ids'))]):
            towns_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            towns_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in towns_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into CITYDICTIONARY 
                (CT_CNKEY, CT_KEY, CT_NAME, CT_CODE, CT_APKEY, CT_RGKEY, CT_PrintOrder) 
                values ({0},{1},'{2}','',0, {3}, NULL );
                '''.format(x.state.itoid, n, x.name, x.region.itoid)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'CITYDICTIONARY';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class HotelCategory(models.Model):
    _name = "samo.hotelcategory"
    _rec_name = "name"
    _description = "list of hotel categories"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.hotelcategory'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.hotelcategory'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='hotel category update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):
        import pyodbc
        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select COH_KEY,COH_NAME from CATEGORIESOFHOTEL"
        hotelcategory_ito = []
        hotelcategory_odoo = []
        max_id = 0
        for x in self.env['samo.hotelcategory'].search([('id', 'in', self._context.get('active_ids'))]):
            hotelcategory_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            hotelcategory_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in hotelcategory_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into CATEGORIESOFHOTEL 
                (COH_KEY,COH_NAME) 
                values ({0},'{1}' );
                '''.format(n, x.name)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'CATEGORIESOFHOTEL';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class RoomType(models.Model):
    _name = 'samo.roomtype'
    _rec_name = "name"
    _description = "list of room types"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.roomtype'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.roomtype'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='room type update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):
        import pyodbc
        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select RC_KEY,RC_NAME from ROOMCATEGORY"
        roomtype_ito = []
        roomtype_odoo = []
        max_id = 0
        for x in self.env['samo.roomtype'].search([('id', 'in', self._context.get('active_ids'))]):
            roomtype_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            roomtype_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in roomtype_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into ROOMCATEGORY 
                (RC_KEY,RC_NAME) 
                values ({0},'{1}' );
                '''.format(n, x.name, x.name)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'ROOMCATEGORY';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Allocation(models.Model):
    _name = 'samo.allocation'
    _rec_name = "name"
    _description = "list of room types"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    pcount = fields.Integer('pcount')
    adult = fields.Integer('adult')
    child = fields.Integer('child')
    infant = fields.Integer('infant')
    age1min = fields.Float('age1min')
    age1max = fields.Float('age1max')
    age2min = fields.Float('age2min')
    age2max = fields.Float('age2max')
    age3min = fields.Float('age3min')
    age3max = fields.Float('age3max')

    def supprimer(self, id):
        rec_unlink = self.env['samo.allocation'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.allocation'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='allocation update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select AC_KEY,AC_NAME from ACCOMODATION"
        allocation_ito = []
        allocation_odoo = []
        max_id = 0
        for x in self.env['samo.allocation'].search([('id', 'in', self._context.get('active_ids'))]):
            allocation_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            allocation_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in allocation_odoo:
            if (x.itoid is None) or (x.itoid == 0):
                n = max_id + 1
                queryy = '''insert into ACCOMODATION 
                (AC_KEY,AC_NAME , AC_CODE , AC_UNICODE , AC_NADMAIN, AC_NCHMAIN, AC_PERROOM,AC_NADEXTRA,AC_NCHEXTRA) 
                values ({0},'{1}','{2}','{3}',{4},{5},1,0,0 );
                '''.format(n, x.name, x.name, x.name, x.adult, x.child)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'ACCOMODATION';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Meal(models.Model):
    _name = 'samo.meal'
    _rec_name = "name"
    _description = "list of meal types"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.meal'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.meal'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='meal update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select PN_KEY,PN_NAME from PANSION"
        meal_ito = []
        meal_odoo = []
        max_id = 0
        for x in self.env['samo.meal'].search([('id', 'in', self._context.get('active_ids'))]):
            meal_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            meal_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in meal_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into PANSION 
                (PN_KEY, PN_NAME) 
                values ({0},'{1}' );
                '''.format(n, x.name)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'PANSION';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Tour(models.Model):
    _name = 'samo.tour'
    _rec_name = "name"
    _description = "list of tour"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.tour'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.tour'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='tour update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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


class Port(models.Model):
    _name = 'samo.port'
    _rec_name = "name"
    _description = "list of port"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    town = fields.Many2one('samo.towns', string='town')

    def supprimer(self, id):
        rec_unlink = self.env['samo.port'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.port'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='port update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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


class Freights(models.Model):
    _name = 'samo.freights'
    _rec_name = "name"
    _description = "list of frights"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in itoid')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    trantype = fields.Integer('transport type')
    source = fields.Many2one('samo.towns', string='departure town')
    srcport = fields.Many2one('samo.port', string='departure port')
    target = fields.Many2one('samo.towns', string='arrival town')
    trgport = fields.Many2one('samo.port', string='arrival port')

    def supprimer(self, id):
        rec_unlink = self.env['samo.freights'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.freights'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='freights update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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


class ClassOffright(models.Model):
    _name = 'samo.freightsclass'
    _rec_name = "name"
    _description = "list of class freights"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.freightsclass'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.freightsclass'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='freights class update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)


class Hotel(models.Model):
    _name = 'samo.hotel'
    _rec_name = "name"
    _description = "list of hotels"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    star = fields.Many2one('samo.hotelcategory', string='star')
    town = fields.Many2one('samo.towns', string='town')

    def supprimer(self, id):
        rec_unlink = self.env['samo.hotel'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.hotel'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='hotel update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select PR_KEY, PR_NAME from _Partners"
        sql_querry1 = "select ID from Assignment"
        hotel_ito = []
        hotel_odoo = []
        max_id = 0
        max_id1 = 0
        for x in self.env['samo.hotel'].search([('id', 'in', self._context.get('active_ids'))]):
            hotel_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            hotel_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        cursor1.execute(sql_querry1)
        for row in cursor1:
            if max_id1 < row[0]:
                max_id1 = row[0]
        for x in hotel_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                n1 = max_id1 + 1
                queryy = '''insert into _Partners 
                (PR_KEY , PR_NAME, PR_ALTKEY, PR_CTKEY, PR_IsActive, PR_COHKEY, PR_MRKEY,PR_IsPublished) 
                values ({0},'{1}',2,{2}, 1 , {3} ,12,1);
                '''.format(n, str(x.name).replace("'", " "), x.town.itoid, x.star.itoid)
                queryy1 = '''insert into Assignment 
                (ID,I_MasterID,I_SlaveID,I_Type) 
                values ({0},{1},1,8);
                '''.format(n1, n)

                cursor1.execute(queryy)
                cursor1.execute(queryy1)

                x.itoid = n
                max_id = n
                max_id1 = n1
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'PARTNERS';commit;'''.format(n + 1)
        cursor1.execute(queryy)
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1 + 1)
        cursor1.execute(queryy)


class Stopsale(models.Model):
    _name = 'samo.stopsale'
    _rec_name = "inc"
    _description = "list of stopsale"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")

    stamp = fields.Char('stamp')
    datebeg = fields.Date('Begin date of stopsale')
    dateend = fields.Date('End date of stopsale')
    hotel = fields.Many2one('samo.hotel', string='hotel')
    room = fields.Many2one('samo.roomtype', string='type of room')
    htplace = fields.Many2one('samo.allocation', string='allocation type')
    meal = fields.Many2one('samo.meal', string='meal')
    checkin = fields.Boolean('Is checkin stopsale')
    issue = fields.Date('Issue date')
    rqdatebeg = fields.Date('Reservation date from')
    rqdateend = fields.Date('Reservation date till')
    note = fields.Char('Description')

    def supprimer(self, id):
        rec_unlink = self.env['samo.stopsale'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.stopsale'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='stop sale update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select SSL_KEY from STOPSALELIST"
        stopsale_ito = []
        stopsale_odoo = []
        max_id = 0
        for x in self.env['samo.stopsale'].search([('id', 'in', self._context.get('active_ids'))]):
            stopsale_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            stopsale_ito.append({
                'id': row[0],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in stopsale_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into STOPSALELIST 
                (SSL_KEY, SSL_HDKEY, SSL_RCKEY, SSL_DATEBEGIN, SSL_DATEEND, SSL_PRKEY, SSL_RTKEY, SSL_TYPE) 
                values ({0},{1},{2},'{3}','{4}',{5},{6},{7});
                '''.format(n, x.hotel.itoid, x.room.itoid,
                           datetime.strftime(x.datebeg, "%d/%m/%Y"),
                           datetime.strftime(x.dateend, "%d/%m/%Y"), 0, 0, 0)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'STOPSALELIST';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Release(models.Model):
    _name = 'samo.release'
    _rec_name = "name"
    _description = "list of release"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    datebeg = fields.Date('Begin date')
    dateend = fields.Date('End date')
    hotel = fields.Many2one('samo.hotel', string='hotel')
    days = fields.Integer('Count of days')

    def supprimer(self, id):
        rec_unlink = self.env['samo.release'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.release'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='release update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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


class Servtype(models.Model):
    _name = 'samo.servtype'
    _rec_name = "name"
    _description = "list of service types"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.servtype'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.servtype'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='service type update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select I_Value,V_Name from Constant where I_Type = 7 "
        servtype_ito = []
        servtype_odoo = []
        max_id = 0
        for x in self.env['samo.servtype'].search([('id', 'in', self._context.get('active_ids'))]):
            servtype_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            servtype_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in servtype_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into Constant 
                (I_Value,V_Name,I_Type) 
                values ({0},'{1}',7 );
                '''.format(n, x.lname, )
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')


class Service(models.Model):
    _name = 'samo.service'
    _rec_name = "name"
    _description = "list of services"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    servtype = fields.Many2one('samo.servtype', string='service type')

    def supprimer(self, id):
        rec_unlink = self.env['samo.service'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.service'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='service update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select SL_KEY,SL_NAME from SERVICELIST"
        service_ito = []
        service_odoo = []
        max_id = 0
        for x in self.env['samo.service'].search([('id', 'in', self._context.get('active_ids'))]):
            service_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            service_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in service_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into SERVICELIST 
                (SL_KEY,SL_NAME,SL_SVKEY,SL_RootPoint) 
                values ({0},'{1}',{2} ,0);
                '''.format(n, x.name, x.servtype.itoid)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'SERVICELIST';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Spos(models.Model):
    _name = 'samo.spos'
    _rec_name = "number"
    _description = "list of spos"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')
    spodate = fields.Date('date of issue SPO')
    usecontract = fields.Char('use contract')
    mixed = fields.Char('mixed')
    ebooking = fields.Char('ebooking')
    usesaleprice = fields.Char('usesaleprice')
    note = fields.Char('note')
    number = fields.Integer('number')

    def supprimer(self, id):
        rec_unlink = self.env['samo.spos'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.spos'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='spos update data , number =' + str(rec_update.number ),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select SPO_KEY from SPOLIST"
        service_ito = []
        service_odoo = []
        max_id = 0
        for x in self.env['samo.spos'].search([('id', 'in', self._context.get('active_ids'))]):
            service_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            service_ito.append({
                'id': row[0],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in service_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                types = 0
                # if x.rotation == 0:
                #     types = 0
                # if x.rotation == 1:
                #     types = 1
                # else:
                #     types = 0
                note = ''
                if x.note == '':
                    note = "null"
                queryy = '''insert into SPOLIST 
                (SPO_KEY, 
                SPO_SVKEY, 
                SPO_NUMBER, 
                
                SPO_COMMENT, 
                SPO_MRKEY, 
                SPO_CREATEDATE, 
                SPO_Remark,
                SPO_TYPE,
                SPO_ISBRUTTO
                ) 
                values ({0},'{1}',{2}  ,'{3}',{4} ,'{5}' ,'{6}',{7},{8});
                '''.format(n, 1, x.number, note, 12, datetime.strftime(x.spodate, "%d/%m/%Y"), note, 0, 0)
                cursor1.execute(queryy)
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        cursor1.execute('commit;')
        queryy = '''update Keys set ID = {0} where Key_TABLE = 'SPOLIST';commit;'''.format(n + 1)
        cursor1.execute(queryy)


class Currency(models.Model):
    _name = 'samo.currency'
    _rec_name = "name"
    _description = "list of currency"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in samo')
    status = fields.Char("status")
    name = fields.Char("name")
    lname = fields.Char('lname')
    alias = fields.Char('alias')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.currency'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.currency'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='currency update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select ID,V_Code from Currency"
        currency_ito = []
        currency_odoo = []
        max_id = 0
        for x in self.env['samo.currency'].search([('id', 'in', self._context.get('active_ids'))]):
            currency_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            currency_ito.append({
                'id': row[0],
                'name': row[1],

            })
            if max_id < row[0]:
                max_id = row[0]
        for x in currency_odoo:
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                queryy = '''insert into Currency 
                (V_Code,V_ISOCode,V_Name) 
                values ('{0}','{1}' ,'{2}');commit;
                '''.format(x.alias, x.alias, x.lname)
                cursor1.execute(queryy)
                queryy1 = '''select ID from Currency where V_Code = '{0}'
                '''.format(x.alias)
                cursor1.execute(queryy1)
                for c in cursor1:
                    x.itoid = int(c[0])
                # fetch its ito_id
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass


class Hotelsalepr(models.Model):
    _name = 'samo.hotelsalepr'
    _rec_name = "inc"
    _description = "list of currency"

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    town = fields.Char(related="hotel.town.name", string="Town")
    status = fields.Char("status")
    stamp = fields.Char('stamp')
    hotel = fields.Many2one('samo.hotel', string='hotel')
    room = fields.Many2one('samo.roomtype', string='room type')
    htplace = fields.Many2one('samo.allocation', string='allocation')
    meal = fields.Many2one('samo.meal', string='meal')
    datebeg = fields.Date('Begin of price season')
    dateend = fields.Date('End of price season')
    rqdatebeg = fields.Date('Spo Reservation from ')
    rqdateend = fields.Date('Spo Reservation till')
    nights = fields.Integer('Staying nights')
    spos = fields.Many2one('samo.spos', string='spos')
    spotype = fields.Selection(
        selection=[('1', 'Standard'), ('2', 'Check-in'), ('3', 'Rotation'), ('4', 'Accommodation'), ('5', 'Meal plan'),
                   ('6', 'Discount')], string='spo type')
    sposubtype = fields.Selection(
        selection=[('1', 'Calculate without first dates'), ('2', 'Calculate without last dates'),
                   ('3', 'Calculate as average value'), ('4', 'Calculate without min price from the edge'),
                   ('5', 'Calculate without max price from the edge')],
        string='spo subtype')
    rroom = fields.Many2one('samo.roomtype', string='Spo room type')
    rhtplace = fields.Many2one('samo.allocation', string='Spo allocation')
    rmeal = fields.Many2one('samo.meal', string='Spo meal')
    rnights = fields.Integer('SPO “Rotation” night')
    price = fields.Float('price')
    currency = fields.Many2one('samo.currency', string='currency')
    dateinfrom = fields.Date('Check-in date from')
    dateoutfrom = fields.Date('Check-out date from')
    dateintill = fields.Date('Check-in date till')
    dateouttill = fields.Date('Check-out date till')
    discount = fields.Float('Discount if percent')
    discountmoney = fields.Float('Discount in money')
    useascheckin = fields.Char('useascheckin')
    rqdaysfrom = fields.Integer('Spo Days before check-in from')
    rqdaystill = fields.Integer('Spo Days before check-in till')
    nightsfrom = fields.Integer('Nights from')
    nightstill = fields.Integer('Nights till')
    oncheckin = fields.Selection(selection=[('0', 'By period'), ('1', 'By check-in')], string='spo rotation')
    adult = fields.Float('Supplement for adult')
    child = fields.Float('Supplement for child with bed')
    nobedchild = fields.Float('Supplement for child without bed')
    days = fields.Char('week days')

    def supprimer(self, id):
        rec_unlink = self.env['samo.hotelsalepr'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.hotelsalepr'].sudo().search([('id', '=', id)])

        #         liste = []
        #         for email_to in self.env['samo.configuration'].search([]):
        #             liste.append(email_to.mail_name)
        #         IrMailServer = self.env['ir.mail_server']
        #         smtp_session = self.env['ir.mail_server'].connect()
        #         msg = IrMailServer.build_email(
        #             email_from='notifications@ctmvoyages.com',
        #             email_to=liste,
        #             subject='Prices updates',
        #             body="""<html>
        #             <table border="1">
        #    <tr>
        #       <th>Name of attribute</th>
        #       <th>Old value</th>
        #       <th>New value</th>
        #    </tr>
        #    <tr>
        #       <td>inc</td>
        #       <td>{0}</td>
        #       <td>{1}</td>
        #    </tr>
        #    <tr>
        #       <td>status</td>
        #       <td>{2}</td>
        #       <td>{3}</td>
        #    </tr>
        #
        #    <tr>
        #       <td>stamp</td>
        #       <td>{4}</td>
        #       <td>{5}</td>
        #    </tr>
        #    <tr>
        #       <td>ito id</td>
        #       <td>{6}</td>
        #       <td>not exist</td>
        #    </tr>
        #    <tr>
        #       <td>hotel</td>
        #       <td>{7}</td>
        #       <td>{8}</td>
        #    </tr>
        #    <tr>
        #       <td>room</td>
        #       <td>{9}</td>
        #       <td>{10}</td>
        #    </tr>
        #    <tr>
        #       <td>allocation</td>
        #       <td>{11}</td>
        #       <td>{12}</td>
        #    </tr>
        #    <tr>
        #       <td>meal</td>
        #       <td>{13}</td>
        #       <td>{14}</td>
        #    </tr>
        #    <tr>
        #       <td>date begin</td>
        #       <td>{15}</td>
        #       <td>{16}</td>
        #    </tr>
        #    <tr>
        #       <td>date end</td>
        #       <td>{17}</td>
        #       <td>{18}</td>
        #    </tr>
        #    <tr>
        #       <td>Spo Reservation from</td>
        #       <td>{19}</td>
        #       <td>{20}</td>
        #    </tr>
        #    <tr>
        #       <td>Spo Reservation till</td>
        #       <td>{21}</td>
        #       <td>{22}</td>
        #    </tr>
        #
        #    <tr>
        #       <td>price</td>
        #       <td>{23}</td>
        #       <td<{24}</td>
        #
        #    </tr>
        #
        #    </tr>
        # </table>
        # </html>
        #             """.format(
        #                 str(rec_update.inc), str(obj['inc']),
        #                 str(rec_update.status), obj['status'],
        #                 str(rec_update.stamp), obj['stamp'],
        #                 str(rec_update.hotel.name), str(obj['hotel']),
        #                 str(rec_update.hotel.name), str(obj['hotel']),
        #                 str(rec_update.room.name), str(obj['room']),
        #                 str(rec_update.htplace.name), str(obj['htplace']),
        #                 str(rec_update.meal.name), str(obj['meal']),
        #                 str(rec_update.datebeg), str(obj['datebeg']),
        #                 str(rec_update.dateend), str(obj['dateend']),
        #                 str(rec_update.rqdatebeg), str(obj['rqdatebeg']),
        #                 str(rec_update.rqdateend), str(obj['rqdateend']),
        #
        #                 str(rec_update.price), str(obj['price']),
        #
        #             ),
        #
        #             object_id=False,
        #             subtype='plain',
        #             subtype_alternative='plain')
        #         res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        #         smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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
        sql_querry = "select CHN_KEY from Prices_HotelNet"
        hotelsalepr_ito = []
        hotelsalepr_odoo = []
        max_id = 0
        for x in self.env['samo.hotelsalepr'].search([('id', 'in', self._context.get('active_ids'))]):
            hotelsalepr_odoo.append(x)
        cursor1.execute(sql_querry)
        for row in cursor1:
            hotelsalepr_ito.append({
                'id': row[0],
            })
            if max_id < row[0]:
                max_id = row[0]
        # get assignement last ID before processing :

        assn = 0
        n1 = 0
        n = 0

        t = 0
        for x in hotelsalepr_odoo:
            ass_id = 0
            spo_id = 0
            sql_querry = "select ID from Assignment"
            cursor1.execute(sql_querry)
            for row in cursor1:
                if ass_id < row[0]:
                    ass_id = row[0]
            sql_querry = "select SPO_KEY from SPOLIST"
            cursor1.execute(sql_querry)
            for row in cursor1:
                if spo_id < row[0]:
                    spo_id = row[0]
            if x.itoid is None or x.itoid == 0:
                n = max_id + 1
                n1 = ass_id + 1
                # some tests to make sure all relations already in the table assignement with that partner
                # test if there is a link between the partner and the accomodation if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 3 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.htplace.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (3,{0},{1},{2})'''.format(x.hotel.itoid, x.htplace.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                # test if there is a link between the partner and the room category if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 2 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.room.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (2,{0},{1},{2})'''.format(x.hotel.itoid, x.room.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                # test if there is a link between the partner and the meal if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 4 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, x.meal.itoid)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (4,{0},{1},{2})'''.format(x.hotel.itoid, x.meal.itoid, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1

                # some adjustement to some variables to fit ito format or foreign key
                rtkey = 0
                ad = x.htplace.adult
                if ad == 1:
                    rtkey = 24
                if ad == 2:
                    rtkey = 1
                if ad == 3:
                    rtkey = 25
                if ad == 4:
                    rtkey = 26
                if ad == 5:
                    rtkey = 28
                if ad == 6:
                    rtkey = 62
                # test if there is a link between the partner and the room type if no insert it
                t = 0
                sql_querry = '''select id 
                from Assignment 
                where I_Type = 1 and  I_MasterID = {0} and I_SlaveID = {1}'''.format(x.hotel.itoid, rtkey)
                cursor1.execute(sql_querry)
                for ass in cursor1:
                    if ass[0]:
                        t = t + 1
                if t == 0:
                    sql_querry = '''insert into 
                  Assignment 
                ( I_Type ,I_MasterID , I_SlaveID,ID )
                values 
                (1,{0},{1},{2})'''.format(x.hotel.itoid, rtkey, n1)
                    cursor1.execute(sql_querry)
                    queryy = '''update Keys set ID = {0} where Key_TABLE = 'ASSIGNMENT';commit;'''.format(n1)
                    cursor1.execute(queryy)
                    ass_id = ass_id + 1
                    n1 = n1 + 1
                week = 'null'
                formula = "Price = {0}".format(x.price)
                dateinfrom = 'null'
                if x.dateinfrom:
                    dateinfrom = datetime.strftime(x.rqdatebeg, "%d/%m/%Y")
                dateintill = 'null'
                if x.dateintill:
                    dateintill = datetime.strftime(x.rqdatebeg, "%d/%m/%Y")
                # some checks for spo to insert them later inside the boo :')
                # if no spo in the samo rec ; generate spo , create it and link it with the price
                spostr = ""
                spo_type = 1
                if x.spos.number == 0:
                    spo_id = 0

                # else just get the id of the spo and link it ( supposebly it's already synchronized)
                else:
                    spo_id = x.spos.itoid
                queryy = '''insert into Prices_HotelNet 
                (CHN_NETTO,
                 CHN_RATENETTO, 
                 CHN_DATEBEGIN, 
                 CHN_DATEEND, 
                 CHN_RELDAYS, 
                 CHN_RCKEY, 
                 CHN_RTKEY, 
                 CHN_PRKEY, 
                 CHN_PNKEY, 
                 CHN_SPKEY, 
                 CHN_KEY, 
                 CHN_CONTRACTPRKEY, 
                 CHN_TYPE, 
                 CHN_WEEK, 
                 CHN_ACKEY, 
                 CHN_SPOKEY, 
                 CHN_MRKEY, 
                 CHN_DurationMin, 
                 CHN_DurationMax, 
                 CHN_FillFormula, 
                 CHN_FreeNights, 
                 CHN_BookingDateBegin, 
                 CHN_BookingDateEnd, 
                 CHN_BookingCode) 
                values (
                {0} ,'{1}' ,'{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, {10},
                {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, '{19}', {20},
                {21}, {22}, {23}
                );
                '''.format(x.price,
                           x.currency.alias,
                           datetime.strftime(x.datebeg, "%d/%m/%Y"),
                           datetime.strftime(x.dateend, "%d/%m/%Y"),
                           7,
                           x.room.itoid,
                           rtkey,
                           x.hotel.itoid,
                           x.meal.itoid,
                           spo_id,
                           n,
                           x.hotel.itoid,
                           1,
                           week,
                           x.htplace.itoid,
                           spo_id,
                           12,
                           x.nightsfrom,
                           x.nightstill,
                           formula,
                           'null',
                           dateinfrom,
                           dateintill,
                           'null')
                try:
                    cursor1.execute(queryy)
                except:
                    raise UserWarning('error in the request {0} with samo id :  '.format(queryy))
                x.itoid = n
                max_id = n
            elif x.itoid > 0:
                # queryy = "update country set name = {1} where CN_KEY = {0}".format(x.ito_id, x.name)
                # cursor1.execute(queryy)
                pass
        sql_querry = '''update Keys set ID = {0} where Key_TABLE = 'Prices_HotelNet' '''.format(n + 1)
        cursor1.execute('commit;')


class Servicesalepr(models.Model):
    _name = 'samo.servicesalepr'
    _rec_name = 'inc'

    inc = fields.Integer('id in samo')
    itoid = fields.Integer('id in ito')
    status = fields.Char('status')
    service = fields.Many2one('samo.service', string='service')
    hotel = fields.Many2one('samo.hotel', string='hotel')
    grouphotel = fields.Char('ID of hotel group')
    townfrom = fields.Many2one('samo.towns', string='town from')
    townto = fields.Many2one('samo.towns', string='town to')
    datebeg = fields.Date('Begin of price season')
    dateend = fields.Date('End of price season')
    paxfrom = fields.Integer('Minimum pax count')
    paxtill = fields.Integer('Maximum pax count')
    nights = fields.Integer('Nights count')
    pernight = fields.Selection(selection=[('0', 'Price per day'), ('1', 'Price per night')], string='Type of price')
    price = fields.Float('Price of whole service')
    adultpr = fields.Float('Price for adult')
    child1pr = fields.Float('Price for first child')
    age1min = fields.Float('Minimum age of first child')
    age1max = fields.Float('Maximum age of first child')
    child2pr = fields.Float('Price for second child')
    age2min = fields.Float('Minimum age of second child')
    age2max = fields.Float('Maximum age of second child')
    currency = fields.Many2one('samo.currency', string='currency')
    rdatebeg = fields.Date('Reservation from')
    rdateend = fields.Date('Reservation till')
    spotype = fields.Selection(selection=[('1', 'Standard price'), ('2', 'Check-in price')], string='Type of SPO')
    stamp = fields.Char('stamp')

    def supprimer(self, id):
        rec_unlink = self.env['samo.servicesalepr'].sudo().search([('id', '=', id)])
        rec_unlink.sudo().unlink()

    def modifier(self, id, obj):
        rec_update = self.env['samo.servicesalepr'].sudo().search([('id', '=', id)])
        list = []
        for email_to in self.env['samo.configuration'].search([]):
            list.append(email_to.mail_name)
        IrMailServer = self.env['ir.mail_server']
        smtp_session = self.env['ir.mail_server'].connect()
        msg = IrMailServer.build_email(
            email_from='marouen@ctmvoyages.com',
            email_to=list,
            subject='notification samo integration',
            body='service sale price update data , id in ito =' + str(rec_update.itoid),
            object_id=False,
            subtype='plain',
            subtype_alternative='plain')
        res = IrMailServer.send_email(msg, smtp_session=smtp_session)
        smtp_session.quit()
        rec_update.update(obj)

    @api.multi
    def synchronize_manual_selected(self):

        server_url = 'DESKTOP-544S3EQ\SQLEXPRESS'
        login = 'sa'
        password = 'TnCTMdbSA2018'
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


class MailConfiguration(models.Model):
    _name = 'samo.configuration'

    mail_name = fields.Char('mail of notification')
    last_timestamp = fields.Char('last stamp')
    last_timestamp = fields.Char('del stamp')
