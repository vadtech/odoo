from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="account.move.line"
	_description="Moddification of aacount move line"

	acc_disAmount=fields.Integer( string='line Discount Amount', compute="sale_line_ids.acc_disAmount")
	linediscPerct=fields.Integer( string='line Discount %', compute="sale_line_ids.linediscPerct")



 

