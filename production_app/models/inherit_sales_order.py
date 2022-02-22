from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="sale.order.line"
	_description="Moddification of order sales table"

	disAmount=fields.Integer( string='Line Discount Amount', compute="_cal_disamount")
	delivered_Qty = fields.Integer(string="Delivered Quantity.")
	prod_ist=fields.Text(string='Product Instruction')
	linMarking=fields.Text(string='Line Marking')
	
	linediscPerct=fields.Integer(string='line Discount %' )

	def _cal_disamount(self):
		for rec in self:
			rec.disAmount = rec.linediscPerct/100 * rec.price_unit *  rec.product_uom_qty
			rec.price_subtotal = rec.price_subtotal - rec.disAmount
