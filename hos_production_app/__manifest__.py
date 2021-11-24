# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Production Application',
    'version' : '14.0.1',
    'summary': 'Invoices & Payments',
    'sequence': -100,
    'description': """this is for monitoring vad production systems to manage its flow """,
    'category': 'Accounting/Accounting',
    'website': 'https://cyber.sys/hospitial',
    'depends' : ['sale','mail'],
    'data': [
    #security -- data -- views --reports
    'security/ir.model.access.csv',
    'views/main_prod_app.xml',   
    'views/add_files_sales.xml', 
    'report/prod_report.xml', 
    'report/production_report.xml', 
      

    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

