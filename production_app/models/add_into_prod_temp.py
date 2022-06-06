from odoo import fields, models, api ,_

class add_into_product_temp(models.Model):
	"""real name of the model"""
	_inherit ="product.template"
	_description="Products Template Edits"
	model = fields.Selection(
		string='Model',
		default = 'other',
		selection=[
		('lean', 'Lean'),
		('zeta', 'Zeta'),
		('pivot', 'Pivot'),
		('nexus', 'Nexus'),
		('meet', 'Meet'),
		('salina', 'Salina'),
		('santana', 'Santana'),
		('bankett', 'Bankett'),
		('other', 'Other')])
