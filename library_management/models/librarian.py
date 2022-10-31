from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError

class Librarian(models.Model):
	_name = 'librarian.librarian'
	_description = 'This is master Table to store the Librarians'

	name = fields.Char(string='Name')
	gender = fields.Selection([("male","Male"),("female","Female")],string='Gender' , default='male')
	dob = fields.Date(string='DOB')
	age = fields.Integer(compute='_compute_age',string='AGE',store=True)
	date_of_joining = fields.Date(string='Date of Joining',required=True) 
	current_experience = fields.Float(string="Current Experience", compute='_compute_experience')


	@api.depends('dob')
	def _compute_age(self):
		print('------------------------i---------------------------')
		for rec in self:
			rec.age = 0
			if rec.dob:
				birthDate = rec.dob
				today = date.today()
				age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
 
				rec.age = age
	
	@api.depends('date_of_joining')
	def _compute_experience(self):
		for rec in self:
			rec.current_experience = 0
			if rec.date_of_joining:
				join_date = rec.date_of_joining
				today = date.today()
				experience = today.year - join_date.year -((today.month, today.day) < (join_date.month, join_date.day))
				
				rec.current_experience = experience

	@api.model			
	def default_get(self,vals):
		res = super(Librarian,self).default_get(vals)	
		res['gender'] = 'female'
		return res
		

	@api.constrains('date_of_joining')
	def _check_experience(self):
		for librarian_rec in self:
			
			if  librarian_rec.current_experience <= 2:
				raise ValidationError('Your Exprience Should Be Greater Than Two')	