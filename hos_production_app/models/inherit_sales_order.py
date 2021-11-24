from odoo import fields, models

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="sale.order.line"
	_description="Moddification of order sales table"

	line_marking=fields.Text(string='Line Making')
	prod_ist=fields.Text(string='Product Instruction')


