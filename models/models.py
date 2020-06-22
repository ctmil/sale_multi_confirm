# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools import float_is_zero, pycompat
from odoo.addons import decimal_precision as dp
from datetime import date,datetime
import os
import base64
from collections import defaultdict

class AccountMove(models.Model):
    _inherit = 'account.move'

    def create_picking(self):
        if not self.picking_id and self.type == 'out_invoice':
            picking_type_id = self.env['stock.picking.type'].search([('company_id','=',self.company_id.id),('code','=','outgoing')],limit=1)
            if not picking_type_id:
                raise ValidationError('No tiene configurada la entrega')
            location_dest_id = self.env['stock.location'].search([('usage','=','customer')],limit=1)
            if not location_dest_id:
                raise ValidationError('No esta configurada la ubicacion del cliente')
            vals_picking = {
                    'picking_type_id': picking_type_id.id,
                    'scheduled_date': datetime.now(),
                    'origin': self.name,
                    'partner_id': self.partner_id.id,
                    'location_id': picking_type_id.default_location_src_id.id,
                    'location_dest_id': location_dest_id.id,
                    }
            picking_id = self.env['stock.picking'].create(vals_picking)
            self.picking_id = picking_id.id
            for line in self.invoice_line_ids:
                vals_move = {
                        'picking_id': picking_id.id,
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'product_uom_qty': line.quantity,
                        'product_uom': line.product_uom_id.id,
                        'location_id': picking_type_id.default_location_src_id.id,
                        'company_id': self.company_id.id,
                        'location_dest_id': location_dest_id.id,
                        }
                move_id = self.env['stock.move'].create(vals_move)

    picking_id = fields.Many2one('stock.picking',string='Remito')


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

