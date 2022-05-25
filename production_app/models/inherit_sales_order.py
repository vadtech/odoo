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
			# calculate discount
			disc_ammount = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
			# calculate temp subtotal
			temp_price_subtotal = (rec.price_unit * rec.product_uom_qty) - disc_ammount
			# calculate line discounts and line discount amount
			rec.disAmount = rec.linediscPerct / 100 * temp_price_subtotal
			#subtract line discount from subtotal
			rec.price_subtotal = temp_price_subtotal - rec.disAmount
			amount_untaxed = amount_tax = 0.0
			for line in self.order_id.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.tax_id.amount / 100 * line.price_subtotal
	
			rec.order_id.amount_untaxed = amount_untaxed
			rec.order_id.amount_tax = amount_tax
			rec.order_id.amount_total = amount_untaxed + amount_tax
