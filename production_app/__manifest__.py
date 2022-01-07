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
    'depends' : ['sale','mail','report_xml'],
    'data': [
    #security -- data -- views --reports
    'data/increment.xml',
    'security/ir.model.access.csv',
    'views/main_prod_app.xml',
    'views/stage_options_views.xml',
    'views/add_files_sales.xml',
    'report/production_report.xml', 
    'report/prod_report.xml',
    'report/english_options.xml',
    'report/english_report.xml',
    'report/norw_invoice_report.xml',
    'report/norwegian_reports.xml',
    'report/invoices_report.xml',
    'report/sale_report.xml', 
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

