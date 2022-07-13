# -*- coding: utf-8 -*-
# from odoo import http


# class DbBackup(http.Controller):
#     @http.route('/db_backup/db_backup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/db_backup/db_backup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('db_backup.listing', {
#             'root': '/db_backup/db_backup',
#             'objects': http.request.env['db_backup.db_backup'].search([]),
#         })

#     @http.route('/db_backup/db_backup/objects/<model("db_backup.db_backup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('db_backup.object', {
#             'object': obj
#         })
