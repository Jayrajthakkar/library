from odoo import models, fields, api
from random import randint
from datetime import datetime, timedelta
from odoo import _
class Book(models.Model):
	_name = 'library.book'
	_description = 'This model stores the data about the Book information'
	_inherit=['mail.thread','mail.activity.mixin']
	_rec_name = 'book_name'


	def _default_random(self):
		return randint(10**(8-1),(10**8)-1)

	sequnce_no = fields.Char(required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
	book_name = fields.Char(string='Name')
	author = fields.Char(string='Author')
	photo = fields.Image(string='Cover Photo')
	state = fields.Selection([("good condition","Good Condition"),("scrapped","Scrapped")],default='good condition',string='State',tracking=True)
	partner_id = fields.Many2many(string='Partner',comodel_name='res.partner')
	sale_history_ids = fields.One2many(string='Sales',comodel_name='sale.history.book',inverse_name='book_id')
	total = fields.Integer(string='total',compute='_compute_total')
	isbn = fields.Integer(string='ISBN',default=_default_random)
	rate = fields.Selection([("star","star"),("low","Low"),("med","Med"),("high","High")],string='Rate')
	status = fields.Selection([("Available","Available"),("Unavailable","Unavailable")])
	user_id = fields.Many2one(string='User',comodel_name='res.users')

	@api.model
	def create(self,vals):
		if vals.get('name', _('New')) == _('New'):
			vals['sequnce_no'] = self.env['ir.sequence'].next_by_code(
           'library.book') or _('New')
		res = super(Book,self).create(vals)
		return res 
	def action_sent_mail(self):
		template_id = self.env.ref('library_management.template_book')
		
		ctx = {
			'default_model': 'library.book',
			'default_res_id': self.ids[0],
			'default_use_template': bool(template_id),
			'default_template_id': template_id.id,
			'default_composition_mode': 'comment',
			'mark_so_as_sent': True,
			'custom_layout': "mail.mail_notification_paynow",
			# 'force_email': True,
			# 'model_description': self.with_context(lang=lang).type_name,
		}
		return {
			'type': 'ir.actions.act_window',
			'view_mode': 'form',
			'res_model': 'mail.compose.message',
			'views': [(False, 'form')],
			'view_id': False,
			'target': 'new',
			'context': ctx,
		}

	def action_direct_sent_mail(self):
		template_id = self.env.ref('library_management.template_book').id
		self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)

	def _compute_total(self):
		for rec in self:
			sum_1 = 0

			for result in rec.sale_history_ids:
				sum_1 = result.subtotal + sum_1
		self.total = sum_1

	def action_cron_sent_mail(self):
		template_id = self.env.ref('library_management.send_mail').id
		self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)

	
	def change_state(self):
		for rec in self:
			if rec.state == 'scrapped':
				rec.state = 'good condition'
				


	def action_state_change(self):
		for state_rec in self:
			self.change_state()
	
	def change_state_cron(self):
		record = self.env['sale.history.book'].search([])
		for state_rec in record: 
			if state_rec.due_date - timedelta(days=2):
				self.action_cron_sent_mail()


	def action_view_salescount(self):
		print('click --------------')

class SalseHistory(models.Model):
	_name='sale.history.book'
	_description = "his model stores the data about the sales information"
	

	book_id = fields.Many2one(comodel_name='library.book',string='Book')
	visitor_id = fields.Many2one(comodel_name='visitor.visitor',string='Visitor')
	partner_id = fields.Many2many(string='Partner',comodel_name='res.partner')
	user_id = fields.Many2one(string='User',comodel_name='res.users')
	borrow_date = fields.Date(string='Borrow Date')
	due_date = fields.Date(string='Due Date')
	quantity = fields.Integer(string='Quantity')
	price = fields.Float(string='Price')
	subtotal=fields.Integer(compute='_compute_total',string='total')


	@api.depends('quantity','price')
	def _compute_total(self):
		for rec in self:
			rec.subtotal=rec.quantity*rec.price

		 # quotations_customers_list = [record.partner_id.id for record in self if record.state == 'draft' ]
   #      print("=================>",quotations_customers_list)