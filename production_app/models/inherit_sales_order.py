from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="sale.order.line"
	_description="Moddification of order sales table"

	disAmount=fields.Integer( string='Line Discount Amount', compute="_cal_disamount")
	delivered_Qty = fields.Integer(string="Delivered Quantity.")
	prod_ist=fields.Text(string='Product Instruction')
	linMarking=fields.Text(string='Line Marking')

	def _cal_disamount(self):
		for rec in self:
			total = self.price_subtotal * 100 / self.discount
			rec.disAmount = self.discount/100 * total
