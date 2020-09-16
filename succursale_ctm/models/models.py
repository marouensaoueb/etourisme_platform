# -*- coding: utf-8 -*-

from odoo import models, fields , api


class ProductTypes(models.Model):
    _name = "ctm.product.type"

    name = fields.Char('Nom')


class Clts(models.Model):
    _name = "ctm.clts"

    name = fields.Char('Nom')


class PayementMethod(models.Model):
    _name = "ctm.payement.method"

    name = fields.Char('Nom')


class CtmPointofsale(models.Model):
    _name = 'ctm.point.of.sale'

    name = fields.Char('Nom')
    allowed_users = fields.Many2many('res.users', string="Allowed Users")


class SaleReportSuccursale(models.Model):
    _name = "ctm.report.succursale"

    def get_user_pos(self):
        pos_id = self.env['ctm.point.of.sale'].search([('allowed_users', 'in', self._uid)])
        return pos_id

    pos = fields.Many2one('ctm.point.of.sale', string="Point of sale", readonly=True, default=get_user_pos)
    ref = fields.Char('Ref')
    dat = fields.Date('Date')
    client = fields.Char('Nom et Prénom du Client')
    clts = fields.Many2one('ctm.clts', string="Clts")
    ste = fields.Char('STE')
    ccp = fields.Char('CCP')
    product_type = fields.Many2one('ctm.product.type', string="Type de produit")
    hotel_id = fields.Many2one('rooming.hotels', string="Hotel")
    fournisseur = fields.Char(string="Fournisseur")
    currency_id = fields.Many2one('res.currency', string="Devise")
    date_op = fields.Date('Date opération')
    purchase_price = fields.Monetary('Prix d\'achat TTC')
    sale_price = fields.Monetary('Prix de vente TTC')
    marge = fields.Monetary('Marge TTC')
    marge_rate = fields.Float('Tx de marge', digits=(10, 3))
    payement_method = fields.Many2one('ctm.payement.method', string="Mode de paiement")
    paiement = fields.Monetary('Paiement')
    remarque = fields.Text('Remarque')

    @api.model
    def create(self, vals):
        try:
            vals['marge'] = vals['sale_price'] - vals['purchase_price']
            vals['marge_rate'] = vals['marge'] / vals['purchase_price']
        except:
            pass
        rec = super(SaleReportSuccursale, self).create(vals)
        return rec
