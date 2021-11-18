# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospitial Managament System',
    'version' : '14.0.1',
    'summary': 'Invoices & Payments',
    'sequence': -100,
    'description': """this is good for Hospitial to manage its flow """,
    'category': 'Accounting/Accounting',
    'website': 'https://cyber.sys/hospitial',
    'depends' : ['sale','mail'],
    'data': [
    #security -- data -- views --reports
    'security/ir.model.access.csv',
    'data/data.xml',
    'wizard/search_appoint_views.xml',
    'wizard/create_appoint_views.xml',
    'views/hosptial_views.xml',
    'views/hosptial_sale.xml',
    'views/save_doctor_views.xml',
    'views/kids_view.xml',
    'views/patient_gender.xml',
    'views/appoint_views.xml',
    'report/patient_reports.xml',
    'report/patient_report_views.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

