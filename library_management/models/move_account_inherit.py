from odoo import models,fields,api

class AccountMove(models.Model):
	_inherit='account.move'


	bank = fields.Char(string='Bank Name')
	number = fields.Char(string='Number')
	commission_invoivce = fields.Boolean(string='Is Commission')


class AccountMove(models.Model):
	_inherit='account.move.line'


	pqr = fields.Char(string='Type') 
	pqrs = fields.Float(string='Amount')

	
	# def create(self,vals):
	# 	unitPrice=super(AccountMove,self).create(vals)
	# 	unitPrice['']
