from odoo import fields, models, api ,_
from datetime import date
from datetime import timedelta

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
		date_create = datetime.strptime('2022-05-26 0:0:0', '%Y-%m-%d %H:%M:%S')
		for rec in self:
			if rec.state=='sale' or rec.state=='done' and rec.create_date>=date_create:
				rec.disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
				dismount = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
				rec.price_subtotal= (rec.price_unit * rec.product_uom_qty )- rec.disAmount - dismount
				amount_untaxed = amount_tax = 0.0
				for line in self.order_id.order_line:
					amount_untaxed += line.price_subtotal
					amount_tax += line.tax_id.amount/ 100 * line.price_subtotal

				self.order_id.amount_untaxed = amount_untaxed
				self.order_id.amount_tax = amount_tax
				self.order_id.amount_total = amount_untaxed + amount_tax
				
			elif rec.create_date>=date_create:
				rec.disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
				dismount = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
				rec.price_subtotal= (rec.price_unit * rec.product_uom_qty )- rec.disAmount - dismount
				amount_untaxed = amount_tax = 0.0
				for line in self.order_id.order_line:
					amount_untaxed += line.price_subtotal
					amount_tax += line.tax_id.amount/ 100 * line.price_subtotal

				self.order_id.amount_untaxed = amount_untaxed
				self.order_id.amount_tax = amount_tax
				self.order_id.amount_total = amount_untaxed + amount_tax
			else:
				rec.disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
				dismount = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
				rec.price_subtotal= (rec.price_unit * rec.product_uom_qty )- rec.disAmount - dismount
				amount_untaxed = amount_tax = 0.0
				for line in self.order_id.order_line:
					amount_untaxed += line.price_subtotal
					amount_tax += line.tax_id.amount / 100 * line.price_subtotal
				self.order_id.amount_untaxed = amount_untaxed
				self.order_id.amount_tax = amount_tax
				self.order_id.amount_total = amount_untaxed + amount_tax
