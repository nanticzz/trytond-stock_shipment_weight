#This file is part stock_shipment_weight module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pyson import Eval, Id
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOut', 'ShipmentOutReturn']
__metaclass__ = PoolMeta


class ShipmentOut:
    __name__ = 'stock.shipment.out'
    weight_uom = fields.Many2One('product.uom', 'Weight Uom',
        domain=[('category', '=', Id('product', 'uom_cat_weight'))],
        states={
            'readonly': Eval('state') != 'draft',
        }, depends=['state'])
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')
    weight = fields.Float('Weight', digits=(16, Eval('weight_digits', 2)),
        states={
            'readonly': Eval('state') != 'draft',
        }, depends=['state', 'weight_digits'])
    weight_lines = fields.Function(fields.Float('Weight of Moves',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_lines')
    weight_func = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_func')

    @fields.depends('weight_uom', 'inventory_moves')
    def on_change_with_weight_lines(self, name=None):
        return self.sum_weights()

    @fields.depends('weight', 'weight_uom', 'inventory_moves')
    def on_change_with_weight_func(self, name=None):
        if self.weight:
            return self.weight
        return self.weight_lines

    def sum_weights(self):
        Uom = Pool().get('product.uom')

        weight = 0.0
        for line in self.inventory_moves:
            if line.quantity and line.product and line.product.weight:
                from_uom = line.product.weight_uom
                to_uom = self.weight_uom or line.product.weight_uom
                weight += Uom.compute_qty(from_uom, line.product.weight *
                    line.quantity, to_uom, round=False)
        return weight

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2


class ShipmentOutReturn:
    __name__ = 'stock.shipment.out.return'
    weight_uom = fields.Many2One('product.uom', 'Weight Uom',
            states={
                'readonly': Eval('state') != 'draft',
            }, depends=['state'])
    weight_digits = fields.Function(fields.Integer('Weight Digits'),
        'on_change_with_weight_digits')
    weight = fields.Float('Weight', digits=(16, Eval('weight_digits', 2)),
            states={
                'readonly': Eval('state') != 'draft',
            }, depends=['state', 'weight_digits'])
    weight_lines = fields.Function(fields.Float('Weight of Moves',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_lines')
    weight_func = fields.Function(fields.Float('Weight',
            digits=(16, Eval('weight_digits', 2)),
            depends=['weight_digits']), 'on_change_with_weight_func')

    @fields.depends('weight_uom', 'inventory_moves')
    def on_change_with_weight_lines(self, name=None):
        return self.sum_weights()

    @fields.depends('weight', 'weight_uom', 'inventory_moves')
    def on_change_with_weight_func(self, name=None):
        if self.weight:
            return self.weight
        return self.weight_lines

    def sum_weights(self):
        Uom = Pool().get('product.uom')

        weight = 0.0
        for line in self.incoming_moves:
            if line.quantity and line.product and line.product.weight:
                from_uom = line.product.weight_uom
                to_uom = self.weight_uom or line.product.weight_uom
                weight += Uom.compute_qty(from_uom, line.product.weight *
                    line.quantity, to_uom, round=False)
        return weight

    @fields.depends('weight_uom')
    def on_change_with_weight_digits(self, name=None):
        if self.weight_uom:
            return self.weight_uom.digits
        return 2
