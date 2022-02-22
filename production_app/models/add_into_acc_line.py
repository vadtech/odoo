from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="account.move.line"
	_description="Moddification of aacount move line"

	acc_disAmount=fields.Integer( string='line Discount Amount', compute="_cal_disamount")
	linediscPerct=fields.Integer( string='line Discount %')

	
	def _cal_disamount(self):
		for rec in self:
			rec.acc_disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.quantity
			rec.price_subtotal = rec.price_subtotal - rec.acc_disAmount
			rec.amount_untaxed=rec.amount_untaxed-rec.acc_disAmount
	
	

 

