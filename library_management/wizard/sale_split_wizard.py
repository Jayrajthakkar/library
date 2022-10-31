from odoo import models,fields,api

class SaleSplit(models.TransientModel):
	_name='sale.split.wizard'


	name = fields.Char(string='Name')
	product_ids = fields.One2many(string='Product',comodel_name='sale.order.line.wizard',inverse_name='quotation_id')
	
	
	@api.model
	def default_get(self, fields_list):
		res = super(SaleSplit,self).default_get(fields_list)
		vals = self.env['sale.order'].browse(self.env.context.get('order_id'))
		lines = []
		for val in vals.picking_ids.move_ids_without_package: 
			print("_________________________________________vvv",val.product_id.name)
			print("_________________________________________vvvidddddd",val.id)
			line=(0,0,{
					'product_id':val.product_id,
					'hidden_move_id':val

					})
			print("________line",line)
			
			print('picking_id----------------------',val.picking_id)
			lines.append(line)
		res.update({
			'product_ids':lines
			})



		return res
	
	def split_quotation(self):
		sale_id = self.env['sale.order'].browse(self.env.context.get('order_id'))
		transfer = sale_id.env['stock.picking'].create({
			'picking_type_id': 2,
			'location_id': 8,
			'location_dest_id' :10,
			'note' : "note",
			'origin':sale_id.name
			})
		
		print('sale_id---------------',sale_id)
			
		for wiz_line in self.product_ids:
			if wiz_line.split_quotation == True:
				wiz_line.hidden_move_id.write({
					'picking_id':transfer.id
					})

class SaleSplitLine(models.TransientModel):
	_name='sale.order.line.wizard'

	quotation_id = fields.Many2one(string='Quotation',comodel_name='sale.split.wizard')
	product_id = fields.Many2one(string='Product',comodel_name='product.product')
	split_quotation = fields.Boolean(string='Order Split?')
	hidden_move_id =fields.Many2one(string='hidden move ID', comodel_name='stock.move')

