# -*- coding: utf-8 -*-
import xml.etree.ElementTree as Etree
from xml.etree.ElementTree import Element

import requests

from odoo import http


class AdonisIntegration(http.Controller):
    @http.route('/adonis_integration/SearchHotels', methods=['GET'], auth='public')
    def searchhotel(self, **kw):
        checkin_date = kw['checkin_date']

        checkout_date = kw['checkout_date']

        city_id = kw['city_id']

        country_id = kw['country_id']

        nationality = kw['nationality']
        try:
            hotel_id = int(kw['hotel_id'])
        except:
            hotel_id = None

        adult = kw['adult']
        child = kw['child']
        try:
            age_child = kw['age_child']
        except:
            age_child = None

        root = Element('AdonisHotelSearchCriteriaDTO')
        checkInDate = Element('CheckInDate')
        checkInDate.text = checkin_date
        root.append(checkInDate)
        CheckOutDate = Element('CheckOutDate')
        CheckOutDate.text = checkout_date
        root.append(CheckOutDate)
        if hotel_id is not None:
            HotelID = Element('HotelID')
            HotelID.text = str(hotel_id)
        CityID = Element('CityID')
        CityID.text = city_id
        root.append(CityID)
        CountryID = Element('CountryID')
        CountryID.text = country_id
        root.append(CountryID)
        NationalityCode = Element('NationalityCode')
        NationalityCode.text = nationality
        root.append(NationalityCode)
        PaginationData = Element('PaginationData')
        root.append(PaginationData)
        PageNumber = Element('PageNumber')
        PageNumber.text = '1'
        PaginationData.append(PageNumber)
        ItemsPerPage = Element('ItemsPerPage')
        ItemsPerPage.text = '2000'
        PaginationData.append(ItemsPerPage)
        RoomCriteria = Element('RoomCriteria')
        root.append(RoomCriteria)
        RoomCriteriaDTO = Element('RoomCriteriaDTO')
        RoomCriteria.append(RoomCriteriaDTO)
        AdultCount = Element('AdultCount')
        AdultCount.text = adult
        RoomCriteriaDTO.append(AdultCount)
        RoomCount = Element('RoomCount')
        RoomCount.text = '1'
        RoomCriteriaDTO.append(RoomCount)
        ChildCount = Element('ChildCount')
        ChildCount.text = child
        RoomCriteriaDTO.append(ChildCount)
        ChildAges = Element('ChildAges')
        if age_child:
            ChildAges.text = age_child
        RoomCriteriaDTO.append(ChildAges)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/SearchHotels',
                                 data=[('prm_CurrentData', Etree.tostring(root))])

        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])

    @http.route('/adonis_integration/BasketHotels', methods=['GET'], auth='public')
    def baskethotels(self, **kw):
        token_id = kw['token']
        xml_service = kw['xml_service']
        Adonis_Unique_Number = kw['Adonis_Unique_Number']
        root = Element('AdonisHotelBasketCriteriaDTO')
        Token = Element('Token')
        Token.text = token_id
        root.append(Token)
        HotelRoomUniqueNumbers = Element('HotelRoomUniqueNumbers')
        root.append(HotelRoomUniqueNumbers)
        SelectHotelRoomDTO = Element('SelectHotelRoomDTO')
        HotelRoomUniqueNumbers.append(SelectHotelRoomDTO)
        HotelRoomUniqueNumbers1 = Element('HotelRoomUniqueNumbers')
        SelectHotelRoomDTO.append(HotelRoomUniqueNumbers1)
        HotelRoomUniqueNumberDTO = Element('HotelRoomUniqueNumberDTO')
        HotelRoomUniqueNumbers1.append(HotelRoomUniqueNumberDTO)
        XmlServicesUniqueNumber = Element('XmlServicesUniqueNumber')
        XmlServicesUniqueNumber.text = xml_service
        HotelRoomUniqueNumberDTO.append(XmlServicesUniqueNumber)
        AdonisUniqueNumber = Element('AdonisUniqueNumber')
        AdonisUniqueNumber.text = Adonis_Unique_Number
        HotelRoomUniqueNumberDTO.append(AdonisUniqueNumber)
        XmlServicesType = Element('XmlServicesType')
        XmlServicesType.text = 'One'
        HotelRoomUniqueNumberDTO.append(XmlServicesType)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/BasketHotels',
                                 data=[('prm_CurrentData', Etree.tostring(root))])

        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])

    @http.route('/adonis_integration/ConfirmHotels', methods=['GET'], auth='public')
    def confirmhotels(self, **kw):

        root = Element('AdonisHotelConfirmCriteriaDTO')
        ReferenceNumber = Element('ReferenceNumber')
        root.append(ReferenceNumber)
        Token = Element('Token')
        Token.text = 'token'
        root.append(Token)
        PurchaseToken = Element('PurchaseToken')
        root.append(PurchaseToken)
        PurchaseDTO = Element('PurchaseDTO')
        PurchaseToken.append(PurchaseDTO)
        ConfirmPassenger = Element('ConfirmPassenger')
        PurchaseDTO.append(ConfirmPassenger)
        ConfirmPassengerDTO = Element('ConfirmPassengerDTO')
        ConfirmPassenger.append(ConfirmPassengerDTO)
        PurchaseToken1 = Element('PurchaseToken')
        ConfirmPassengerDTO.append(PurchaseToken1)
        PurchaseToken1.text = 'token'
        Occupancy = Element('Occupancy')
        ConfirmPassengerDTO.append(Occupancy)
        AdultCount = Element('AdultCount')
        AdultCount.text = '1'
        Occupancy.append(AdultCount)
        ChildCount = Element('ChildCount')
        ChildCount.text = '0'
        Occupancy.append(ChildCount)
        Passengers = Element('Passengers')
        Occupancy.append(Passengers)
        PassengerDTO = Element('PassengerDTO')
        Passengers.append(PassengerDTO)
        IsLeader = Element('IsLeader')
        IsLeader.text = 'true'
        PassengerDTO.append(IsLeader)
        ID = Element('ID')
        PassengerDTO.append(ID)
        SalutationID = Element('SalutationID')
        SalutationID.text = 'gerhthj'
        PassengerDTO.append(SalutationID)
        Name = Element('Name')
        Name.text = kw['name_client']
        PassengerDTO.append(Name)
        LastName = Element('LastName')
        LastName.text = kw['last_name_client']
        PassengerDTO.append(LastName)
        Age = Element('Age')
        Age.text = kw['Age_client']
        PassengerDTO.append(Age)
        AgeSpecified = Element('AgeSpecified')
        AgeSpecified.text = kw['AgeSpecified']
        PassengerDTO.append(AgeSpecified)
        PassengerType = Element('PassengerType')
        PassengerType.text = kw['PassengerType']
        PassengerDTO.append(PassengerType)
        HotelRoomUniqueNumber = Element('HotelRoomUniqueNumber')
        ConfirmPassengerDTO.append(HotelRoomUniqueNumber)
        XmlServicesUniqueNumber = Element('XmlServicesUniqueNumber')
        HotelRoomUniqueNumber.append(XmlServicesUniqueNumber)
        AdonisUniqueNumber = Element('AdonisUniqueNumber')
        HotelRoomUniqueNumber.append(AdonisUniqueNumber)
        XmlServicesType = Element('XmlServicesType')
        HotelRoomUniqueNumber.append(XmlServicesType)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/ConfirmHotels',
                                 data=[('prm_CurrentData', Etree.tostring(root))])

        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])

    @http.route('/adonis_integration/CancelHotels', methods=['GET'], auth='public')
    def cancelhotels(self, **kw):
        root = Element('AdonisHotelCancelCriteriaDTO')
        FileNumber = Element('FileNumber')
        root.append(FileNumber)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/CancelHotels',
                                 data=[('prm_CurrentData', Etree.tostring(root))])
        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])

    @http.route('/adonis_integration/DetailHotels', methods=['GET'], auth='public')
    def boukingdetails(self, **kw):
        root = Element('AdonisHotelDetailCriteriaDTO')
        FileNumber = Element('FileNumber')
        root.append(FileNumber)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/DetailHotels',
                                 data=[('prm_CurrentData', Etree.tostring(root))])
        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])

    @http.route('/adonis_integration/BookingList', methods=['GET'], auth='public')
    def bookinglist(self, **kw):
        root = Element('AdonisHotelDetailByDatesCriteriaDTO')
        FromDate = Element('FromDate')
        FromDate.text = kw['date_from_search']
        root.append(FromDate)
        ToDate = Element('ToDate')
        ToDate.text = kw['date_to_search']
        root.append(ToDate)
        Credentials = Element('Credentials')
        root.append(Credentials)
        ClientID = Element('ClientID')
        ClientID.text = 'a7d6e735-216d-48f5-af81-62ce36238812'
        Credentials.append(ClientID)
        Username = Element('Username')
        Username.text = 'resp.produit@carthagetravel.com.tn'
        Credentials.append(Username)
        Password = Element('Password')
        Password.text = 'V6IP92'
        Credentials.append(Password)
        response = requests.post('http://xmltest.adonis.com/AdonisServices/BookingList',
                                 data=[('prm_CurrentData', Etree.tostring(root))])
        return http.request.make_response(response.text, [('Content-Type', 'text/xml')])
