from odoo import fields, models, api ,_

class add_into_order_line(models.Model):
	"""real name of the model"""
	_inherit ="account.move.line"
	_description="Moddification of aacount move line"

	acc_disAmount=fields.Integer( string='line Discount Amount', compute="_cal_disamount")
	linediscPerct=fields.Integer( string='line Discount %')

	def _cal_disamount(self):
		list_id=[27665,46,45,44,43]
		if self.move_id.id in list_id:
			for rec in self:
				#calculate line discount amount
				rec.acc_disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.quantity
				#calculate discount amount
				dismount = rec.discount / 100 * rec.price_unit * rec.quantity
				#calculate discount price subtotal
				rec.price_subtotal= dismount
				amount_untaxed = amount_tax = 0.0
				for line in self.move_id.invoice_line_ids:
					amount_untaxed += line.price_subtotal
					amount_tax += line.tax_ids.amount / 100 * line.price_subtotal
				self.move_id.\
					amount_untaxed = amount_untaxed
				self.move_id.amount_tax = amount_tax
				self.move_id.amount_total = amount_untaxed + amount_tax
		else:
			for rec in self:
				rec.acc_disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.quantity
				dismount = rec.discount / 100 * rec.price_unit * rec.quantity
				rec.price_subtotal= dismount
				amount_untaxed = amount_tax = 0.0
				for line in self.move_id.invoice_line_ids:
					amount_untaxed += line.price_subtotal
					amount_tax += line.tax_ids.amount / 100 * line.price_subtotal

				self.move_id.amount_untaxed = amount_untaxed
				self.move_id.amount_tax = amount_tax
				self.move_id.amount_total = amount_untaxed + amount_tax
	

	

 

