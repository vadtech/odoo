from odoo import fields, models, api ,_

class add_into_res(models.Model):
	"""real name of the model"""
	_inherit ="account.move"
	_description="Invoicing Application edits"

	link_prod_id = fields.Many2one('prod_order.model', string="Production ID")
	
	@api.model
	def convert_to_float(self,convert):
		save=float(convert)
		return save

	@api.model
	def convert_to_int(self,convert):
		new_int=int(convert)
		return new_int

	@api.model
	def extract_digits(self,convert):
		change=str(convert)
		res = ''.join(filter(lambda i: i.isdigit(), change))
		return res
