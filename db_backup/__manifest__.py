# -*- coding: utf-8 -*-
{
    'name': "db_backup",

    'summary': """
       A app that will backup the database to OneDrive daily 
        """,

    'description': """
        THe app takes db dump from odoo.sh and uploads to OneDrive
    """,

    'author': "heartman.glace.com",
    'website': "http://vad.no/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Technical',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # loading cron vars
    'data': [
        'data/backup_job.xml',
    ],
}
