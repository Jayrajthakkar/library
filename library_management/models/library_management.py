from odoo import models, fields, api

class LibraryManagement(models.Model):
	_name = 'library.management'
	_description = 'This is master table to store the Libraries'

	name = fields.Char(string='Name')
	property_type = fields.Selection([("public","Public"),("private","Private")],string='Type')
	librarians_ids = fields.Many2many(comodel_name = 'librarian.librarian',string='Librarians')




	