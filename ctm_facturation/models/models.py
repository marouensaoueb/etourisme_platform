# -*- coding: utf-8 -*-

from odoo import models, fields


class CtmFacturation(models.Model):
    _name = 'ctm_facturation.ctm_facturation'
    _rec_name = 'number_facture'

    date_facture = fields.Date('date facture')
    type_facture = fields.Selection([('excursion', 'excursion'), ('transfert', 'transfert'), ('sejour', 'sejour')],
                                    string='type facture', default='excursion')
    number_facture = fields.Char("n° facture")
    vendeur_facture = fields.Many2one('res.users', string='vendeur')
    montant_facture = fields.Float('total facture')
    # invoice_res_line_excursion = fields.One2many('invoice_res.line_excursion', 'account_invoice_id_excursion')
    # invoice_res_line_transfert = fields.One2many('invoice_res.line_transfert', 'account_invoice_id_transfert')
    # invoice_res_line_sejour = fields.One2many('invoice_res.line_sejour', 'account_invoice_id_sejour')


# class FacturationExcursion(models.Model):
#     _name = 'ctm_facturation.ctm_facturation'
#     _inherit = 'ctm_facturation.ctm_facturation'
#
#     invoice_res_line_excursion = fields.One2many('invoice_res.line_excursion', 'account_invoice_id_excursion')
#
#
# class InvoiceResLineExcursion(models.Model):
#     _name = 'invoice_res.line_excursion'
#
#     # account_invoice_id_excursion = fields.Many2one('ctm_facturation.ctm_facturation', 'account_invoice_id_excursion')
#     ctm_invoice_id_excursion = fields.Many2one('ctm.invoice', 'ctm_invoice_id_excursion')
#
#     excursion_name = fields.Char('désignations')
#     date_excursion = fields.Date("date d'excursion")
#     vendeur = fields.Char('vendeur')
#     nbre_adulte = fields.Integer("nbre d'adulte")
#     nbre_enfant = fields.Integer("nbre d'enfant")
#     prix_adulte = fields.Float('prix adulte')
#     prix_enfant = fields.Float('prix enfant')
#     montant = fields.Float('Montant')
#
#     # @api.depends('nbre_adulte', 'nbre_enfant', 'prix_adulte', 'prix_enfant')
#     # def _value_montant(self):
#     #     self.montant = self.nbre_adulte * self.prix_adulte + self.nbre_enfant * self.prix_enfant
#
#
# class InvoiceResLineSejour(models.Model):
#     _name = 'invoice_res.line_sejour'
#
#     account_invoice_id_sejour = fields.Many2one('ctm.facturation', 'invoice_res_line_sejour')
#     excursion_name = fields.Char('désignations')
#     date_excursion = fields.Date("date d'excursion")
#     vendeur = fields.Char('vendeur')
#     nbre_adulte = fields.Integer("nbre d'adulte")
#     nbre_enfant = fields.Integer("nbre d'enfant")
#     prix_adulte = fields.Float('prix adulte')
#     prix_enfant = fields.Float('prix enfant')
#     montant = fields.Float('Montant')
#
#
# class InvoiceResLineTransfert(models.Model):
#     _name = 'invoice_res.line_transfert'
#
#     account_invoice_id_transfert = fields.Many2one('ctm.facturation', 'invoice_res_line_transfert')
#     excursion_name = fields.Char('désignations')
#     date_excursion = fields.Date("date d'excursion")
#     vendeur = fields.Char('vendeur')
#     nbre_adulte = fields.Integer("nbre d'adulte")
#     nbre_enfant = fields.Integer("nbre d'enfant")
#     prix_adulte = fields.Float('prix adulte')
#     prix_enfant = fields.Float('prix enfant')
#     montant = fields.Float('Montant')
#
#
# class InvoiceCtm(models.Model):
#     _name = 'ctm.invoice'
#     _inherit = 'account.invoice'
#
#     invoice_res_line_excursion = fields.One2many('invoice_res.line_excursion', 'ctm_invoice_id_excursion')
