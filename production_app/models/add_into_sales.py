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
		self.state="done"
		for record in self:
			created_all = self.env["prod_order.model"].search_count([('main_sales_id', '=', record.id)])
			temp_ids=[]
			if created_all == 0:
				for line in record.order_line:
					vals = {
						'name_id': int(line.id),
						'line_mark': line.linMarking,
						'product_order': line.name,
						'product_ints': line.prod_ist,
						'qunt': line.product_uom_qty,
					}
					temp_ids.append((0, 0, vals))
				self.env["prod_order.model"].create(
					{
						"main_sales_id": record.id,
						"pro_order_ids": temp_ids,
					}
				)
			else:
				pass
		return super().action_confirm()
	
	
	def custom_action_draft(self):
		for record in self:
			record.state='draft'

	def custom_action_confirm(self):
		self.state=""
		for record in self:
			created_all = self.env["prod_order.model"].search_count([('main_sales_id', '=', record.id)])
			temp_ids=[]
			if created_all == 0:
				for line in record.order_line:
					vals = {
						'name_id': int(line.id),
						'line_mark': line.linMarking,
						'product_order': line.name,
						'product_ints': line.prod_ist,
						'qunt': line.product_uom_qty,
					}
					temp_ids.append((0, 0, vals))
				self.env["prod_order.model"].create(
					{
						"main_sales_id": record.id,
						"pro_order_ids": temp_ids,
					}
				)
			else:
				pass
