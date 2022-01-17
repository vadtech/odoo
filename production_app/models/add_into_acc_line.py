from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="account.move.line"
	_description="Moddification of aacount move line"

	acc_lineDiscount=fields.Integer( string='Line Discount %')
	acc_disAmount=fields.Integer( string='line Amount' )

	@api.onchange("acc_lineDiscount")
	def _onchange_lineDiscount(self):
		self.acc_disAmount = self.acc_lineDiscount/100 * self.price_subtotal
		temp=self.price_subtotal
		self.price_subtotal=temp-self.acc_disAmount





