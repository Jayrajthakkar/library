from odoo import models,fields,api
from odoo.exceptions import ValidationError

class VendorCommission(models.TransientModel):
    _name='vendor.wizard'


    commission_user_id = fields.Many2one(comodel_name='res.users',string='Commission Person')

    def get_commissions(self):

        selected_record_list=[]
        move_rec = self.env['account.move'].search([('partner_id','=',self.commission_user_id.partner_id.id),('move_type','=','in_invoice')])
        
        if not move_rec:
            raise ValidationError("record not found for vendor")
        else:    
            for move_record in move_rec:
                if move_record.commission_invoivce == True:
                    selected_record_list.append(move_record.id)
            return self.env.ref('library_management.action_report_commission').report_action(selected_record_list)

