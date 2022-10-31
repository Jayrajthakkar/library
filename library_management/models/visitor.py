from odoo import models, fields, api

class Visitor(models.Model):
	_name = 'visitor.visitor'
	_description = 'This stores data of Visitor'

	name = fields.Char(string='Name' , required=True)
	