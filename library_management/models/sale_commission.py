from odoo import models, fields, api

class Product(models.Model):
	_inherit = 'product.template'


	commission_percentage = fields.Float(string="Commission Percentage",default=5)

