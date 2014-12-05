#This file is part stock_shipment_weight module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

from trytond.pool import Pool
from .shipment import *
from .move import *


def register():
    Pool.register(
        ShipmentOut,
        ShipmentOutReturn,
        Move,
        module='stock_shipment_weight', type_='model')
