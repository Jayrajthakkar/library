from odoo import models,fields,api
from datetime import date
from odoo.exceptions import ValidationError
class SaleOrder(models.Model):
	_inherit='sale.order'

	bank = fields.Char(string='Bank Name')
	number = fields.Char(string='Number')
	abc = fields.Char(string='Bank Name')
	abcd = fields.Char(string='Bank Name')
	commission_user_id = fields.Many2one(comodel_name='res.users',string='Commission Person')
	commission_value_total = fields.Float(string='Commission Total',compute='_commission_total') 


	@api.depends('order_line.commission_value')
	def _commission_total(self):
		total = 0
		for commission in self.order_line:
			total += commission.commission_value

		self.commission_value_total= total


	def action_confirm(self):
		invoice_vendor = super(SaleOrder, self).action_confirm()

		move_vals = self.env['account.move'].new({
			'move_type': 'in_invoice',
			'journal_id': 2,
			'partner_id':self.commission_user_id.partner_id.id,
			'company_id': self.company_id.id,
			'invoice_date':date.today(),
			'commission_invoivce':True
		})
		print('-----move_vals',move_vals)
		
		move_vals._onchange_partner_id()
		
		print('-----onchnage',move_vals)
		
		values = move_vals._convert_to_write(move_vals._cache)
		print('-------------',values)
		
		move_rec = self.env['account.move'].create(values)
		


		move_line_vals = self.env['account.move.line'].new({
			'move_id':move_rec.id,
			'product_id':39,
			'price_unit':self.commission_value_total,
			
		})

		print('-------------------',move_line_vals)

		move_line_vals._onchange_product_id()
		
		
		print('--------after-----------',move_line_vals['price_unit'])
		
		move_line_vals.update({
			'price_unit': self.commission_value_total,

			})

		print('--------after-----------',move_line_vals['price_unit'])
		
		# move_line_vals._onchange_price_subtotal()

		values = move_line_vals._convert_to_write(move_line_vals._cache) 
		
		print('values===============',values)
		
		
		move_line_rec = self.env['account.move.line'].create(values)

		for move_line in move_line_rec:
			move_line.price_subtotal = move_line.price_unit*move_line.quantity 

		
		
		move_rec.action_post()


		return invoice_vendor

		

		

	def _prepare_invoice(self):

		# print('-----------',self)
		vals = super(SaleOrder,self)._prepare_invoice()
		vals['bank']=self.bank
		vals['number']=self.number
		return vals

	def action_split(self):
		form_id = self.env.ref('library_management.sale_split_wizard_view_form').id
		# print('----------------',self.order_line.product_id)

	# print('-------------------------------------------------',self.order_line.product_id)
		return {
			 'type': 'ir.actions.act_window',
			 'name': 'Sale Order Form',
			 'view_type': 'form',
			 'view_mode': 'form',
			 'view_id': form_id,
			 'res_model': 'sale.split.wizard',
			 'context': {'order_id':self.id},
			 'target':'new',
			 }


	

	def action_merge(self):
		quotations_customers = []
		for sale_order_record in self:
			if sale_order_record.state == 'draft':
				quotations_customers.append(sale_order_record.partner_id.id)
		
		#Delete Duplicate Customer

		quotations_customers_set = set(quotations_customers)
		print("---------Set-------------",quotations_customers_set)  

		#Single Customer
		if len(quotations_customers_set) == 1:
			sale_order_quotations = self.env['sale.order'].search([('id','in',self.ids),('partner_id','in',quotations_customers),('state','=','draft')])
			print("\n\n\n quotation -------",sale_order_quotations)
			

			order_line_list = []
			for sale_order_record in sale_order_quotations:
				for order_line_rec in sale_order_record.order_line:
					order_line_list.append((0,0,{
										'product_id':order_line_rec.product_id.id,
										'product_uom_qty':order_line_rec.product_uom_qty,
										'price_unit':order_line_rec.price_unit,
										'price_subtotal':order_line_rec.price_subtotal
						}))
		  
				sale_order_record.action_cancel() #cancel selected quotations
			merge_sale_order = self.env['sale.order'].create({
				'partner_id':sale_order_quotations.partner_id.id,
				'order_line':order_line_list,
				})
			merge_sale_order.action_confirm()#new order create direct in sale order state
			return {
					'type': 'ir.actions.act_window',
					'name':'Sale Order',
					'res_model':'sale.order',
					'domain':[('id','=',merge_sale_order.id)],
					'view_mode': 'form',
					'target':'current'
					}
		else:
			raise ValidationError("Cannot merge other customers quotations !!")

