# -*- coding: utf-8 -*-


from odoo import models, fields


class Affectation(models.Model):
    _name = 'excursion.affectation'

    dat = fields.Date('Date excursion', required=True)
    excurson_id = fields.Many2one('excursion.excursion', string="Excursion", required=True)
    guide_principale = fields.Many2one('excursion.guide', string='Guide Principale',
                                       domain=[('etat', '=', 'principale')], required=True)
    guide_doubleur = fields.Many2one('excursion.guide', string='Guide Doubleur', domain=[('etat', '=', 'doubleur')])
    chauffeur = fields.Many2one('ctm.conductor', string='Chauffeur', required=True)
    vehicule = fields.Many2one('fleet.vehicle', String="Vehicule", required=True)
    liste_vente = fields.Many2many('excursion.reservations', string="Liste reservation", required=True)
    liste_camel = fields.Many2many('excursion.reservations', string="Liste Camel", required=True)

    def test(self):
        # lista=[]
        # raise  UserError(self.liste_vente)
        #
        total_pax = 0
        bebe = 0
        adulte = 0
        enfant = 0

        domaine = [('excursion_id', '=', self.excurson_id.id), ('date_m', '=', self.dat),
                   ('chauffeur', '=', self.chauffeur.id), ('vehicule', '=', self.vehicule.id),
                   ('guide_principale', '=', self.guide_principale.id)
                   ]
        rec = self.env['excursion.movementday'].search(domaine)
        idm = 0
        if len(rec) > 0:
            idm = rec[0].id
        else:
            self.env['excursion.movementday'].create(
                {'date_m': self.dat, 'excursion_id': self.excurson_id.id, 'guide_principale': self.guide_principale.id,
                 'numero_guide_principale': self.guide_principale.tel,
                 'guide_doubleur': self.guide_doubleur.id, 'numero_guide_doubleur': self.guide_doubleur.tel,
                 'chauffeur': self.chauffeur.id, 'vehicule': self.vehicule.id,
                 })
            rec = self.env['excursion.movementday'].search(
                [('excursion_id', '=', self.excurson_id.id), ('date_m', '=', self.dat),
                 ('chauffeur', '=', self.chauffeur.id), ('vehicule', '=', self.vehicule.id),
                 ('guide_principale', '=', self.guide_principale.id)])
            idm = rec[0].id

        listm = self.liste_vente
        liste_hotel = []
        for ii in self.liste_camel:
            r = self.env['excursion.reservations'].search([('id', '=', ii.id)])
            r.update({
                'movementday_id': idm,
            })
        for i in listm:
            r = self.env['excursion.reservations'].search([('id', '=', i.id)])
            r.update({
                'movementday_id': idm,
            })
            if i.hotel_id not in liste_hotel:
                liste_hotel.append(i.hotel_id)
                self.env['hotel.depart.config'].create({
                    'hotel': i.hotel_id.id,
                    'movementday_id': idm,
                })

        for z in self.env['excursion.reservations'].search(
                [('movementday_id', '=', idm), ('excursion_id.type_excursion_camel', '=', False)]):
            bebe = bebe + z.inf
            adulte = adulte + z.adulte
            enfant = enfant + z.enfant
        total_pax = adulte + enfant + bebe
        nbre_q_q = total_pax // 6
        if (total_pax % 6) != 0:
            nbre_q_q = nbre_q_q + 1
        r_mov = self.env['excursion.movementday'].search([('id', '=', idm)])
        r_mov.update({
            'nbr_adulte': adulte,
            'nbr_enfant': enfant,
            'nbr_bebe': bebe,
            'pax': total_pax,
            'nbr_q_q': nbre_q_q
        })
        for mm in self.env['excursion.movementday'].search([]):
            all_recs = self.env['excursion.reservations'].search([('movementday_id', '=', mm.id)])
            rep_list_id = []
            for x in all_recs:
                if x.vendeur_id.id not in rep_list_id:
                    rep_list_id.append(x.vendeur_id.id)
            sam = 0
            for y in rep_list_id:
                sam = 0
                obj = {
                    'representative_id': y,
                    'mov_id': mm.id,
                    'nbr_pax': 0,
                }
                for z in all_recs:
                    if z.vendeur_id.id == y and z.excursion_id.type_excursion_camel is False:
                        sam = sam + z.enfant + z.adulte + z.inf
                obj['nbr_pax'] = sam
                self.env['move.repres.info'].create(obj)
