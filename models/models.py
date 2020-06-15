# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_is_zero, pycompat
from odoo.addons import decimal_precision as dp
from datetime import date
import os
import base64
from collections import defaultdict

class ResPartner(models.Model):
    _inherit = 'res.partner'

    journal_id = fields.Many2one('account.journal')


#class PurchaseOrder(models.Model):
#	_inherit = 'purchase.order'
#
#	def button_confirm(self):
#		res = super(PurchaseOrder, self).button_confirm()
#		for rec in self:
#			for line in rec.order_line:
#				product_tmpl = line.product_id.product_tmpl_id
#				product_tmpl.with_context(force_company=rec.company_id.id).write({'standard_price': line.price_unit})
#		return res

