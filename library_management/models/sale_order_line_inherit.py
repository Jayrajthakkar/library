from odoo import models,fields,api

class SaleOrderLine(models.Model):
	_inherit='sale.order.line'

	pqr = fields.Char(string='Type') 
	pqrs = fields.Float(string='Amount') 

	commission_percentage = fields.Float(string='Commission Percentage')
	commission_value = fields.Float(string='Commission Value',compute='_commission_value')

	@api.onchange('product_id')
	def _commission_percentage(self):
		for order_line in self:
			order_line.commission_percentage = order_line.product_id.commission_percentage


	@api.depends('commission_percentage','price_subtotal')	
	def _commission_value(self):
		print("------------->>>>>>>>",self)

		for order_line in self:
			order_line.commission_value = (order_line.price_subtotal * order_line.commission_percentage)/100


	def _prepare_invoice_line(self,**optional_values):
		vals = super(SaleOrderLine,self)._prepare_invoice_line() 
		
		vals['pqr'] = self.pqr
		vals['pqrs'] = self.pqrs
		 		
		
		return vals




