    # -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Library Management',
    'version' : '1.1',
    'summary': 'Library Management',
    'sequence': 10,
    'description': """Library Management""",
    'depends' : ['sale','mail','contacts','account','product'],
    'data': ['security/ir.model.access.csv',
             'report/action_report_book.xml',
             'report/template_report_book.xml',
             'report/invoice_report_inherit.xml',
             'report/action_report_commission.xml',
             'report/template_report_commission.xml',

             # 'data/add_product.xml',
             # 'data/add_new_product.xml',
             
             'data/template.xml',
             'data/confirm_mail.xml',
             'data/state_server.xml',
             'data/state_cron.xml',
             'data/send_mail.xml',
             'data/sale_mail_inherit.xml',
             'data/sale_server_split.xml',    
             'data/merge_sale_server.xml',    
             'data/sequence_data.xml',    
             
             'wizard/sale_split_wizard.xml',        
             'wizard/vendor_commission_wizard.xml',        
             
             'views/visitor.xml',
             'views/library_management.xml',
             'views/librarian.xml',
             'views/book.xml',
             'views/sale_edit.xml',
             'views/sale_order_view.xml',
             'views/sale_commission.xml'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
