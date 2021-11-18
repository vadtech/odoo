from odoo import fields, models

class hosptial_sales(models.Model):
	"""real name of the model"""
	_inherit ="sale.order"
	_description = "Model for hosptial sales"

	sale_desciption=fields.Char(string="Sales Description")