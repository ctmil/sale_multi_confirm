# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_is_zero, pycompat
from odoo.addons import decimal_precision as dp
from datetime import date
import os
import base64
from collections import defaultdict

class ConfirmSaleOrder(models.TransientModel):
    _name = 'confirm.sale.order'

    def confirm_sale_orders(self):
        order_ids = self.env.context.get('active_ids',[])
        for order_id in order_ids:
            order = self.env['sale.order'].browse(order_id)
            if order.state in ['draft','sent'] and order.amount_total > 0:
                order.action_confirm()
                moves = order._create_invoices()
                for move in moves:
                    if order.partner_id.journal_id and order.partner_id.journal_id.id != move.journal_id.id:
                        move.journal_id = order.partner_id.journal_id.id
                    move.action_post()
        #raise ValidationError('estamos aca %s'%(self.env.context))

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

