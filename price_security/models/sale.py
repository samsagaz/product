# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models, api, _


class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        readonly=True,
        string='Product Can modify prices')

    @api.one
    @api.constrains(
        'discount', 'product_can_modify_prices')
    def check_discount(self):
        if (
                self.user_has_groups('price_security.group_restrict_prices')
                and not self.product_can_modify_prices
        ):
            self.env.user.check_discount(
                self.discount,
                self.order_id.pricelist_id.id)


class sale_order(models.Model):
    _inherit = 'sale.order'

    @api.one
    @api.constrains(
        'pricelist_id',
        'payment_term',
        'partner_id')
    def check_priority(self):
        if self.partner_id.property_product_pricelist.sequence < self.pricelist_id.sequence:
            raise Warning(_(
                'Selected pricelist priority can not be higher than pircelist '
                'configured on partner'
            ))
        if self.partner_id.property_payment_term.sequence < self.payment_term.sequence:
            raise Warning(_(
                'Selected payment term priority can not be higher than '
                'payment term configured on partner'
            ))
