from odoo import models, fields, api


class FinalPrices(models.TransientModel):
    _name = 'wizard.finalprices'

    def _get_meals(self):
        try:
            contract = self._context.get('contract')
            contract_rec = self.env['contract.contract'].search([('id', '=', contract)]).meals
            listo = []

            for x in contract_rec:
                listo.append(x.id)
            return [('id', 'in', listo)]

        except:
            return [('id', '=', [1])]

    date_from = fields.Date('date from')
    date_to = fields.Date('date to')
    meal = fields.Many2one('room.meal', string='meal', domain=_get_meals)
    accomodation_price = fields.Many2many('accomodation.prices', string="accomodation prices")

    # @api.onchange('meal')
    # def changer(self):
    #     contract = self._context.get('contract')
    #     rec = self.env['room.prices'].search([('id','=',contract)])[0].contract_id.id
    #     contract_rec = self.env['contract.contract'].search([('id', '=', rec)])
