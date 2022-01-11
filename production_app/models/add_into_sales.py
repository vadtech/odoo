from odoo import fields, models, api ,_

class add_into_sales(models.Model):
	"""real name of the model"""
	_inherit ="sale.order"
	_description = "Moddification of sales table"
	price_list=fields.Many2one('product.pricelist',string="Price list")
	total_dis=fields.Integer( string='Total Discount')
	total_dis_line=fields.Integer(string='Total line')
	client_order_ref2 = fields.Char(string='Customer Reference 2', copy=False)
	newMarking = fields.Char(string='Marking', copy=False)


	def action_confirm(self):
		created_all = self.env["prod_order.model"].search_count([('main_sales_id', '=', self.id)])
		if created_all == 0:
			self.env["prod_order.model"].create(
				{
					"main_sales_id": self.id,
				}
			)
		else:
			pass
		return super().action_confirm()
