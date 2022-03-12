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
	
	
	@api.model
	def check_u_currency(self):
		for record in self: 
			if record.partner_id.payment_fact == 'pay_3':
				new_sign = 'dkk'
			elif record.partner_id.payment_fact == 'pay_2':
				new_sign = 'sek'
			else:
				new_sign = 'nok'
		return new_sign
	
	def lest_fix_line_disc(self):
		current_rec = self.env['sale.order'].search([])
		for rec in current_rec:
			created_all = self.env["account.move"].search([('sales_char', '=', rec.name)])
			created_no = self.env["account.move"].search_count([('sales_char', '=', rec.name)])
			if created_no == 1:
				copy_rec = self.env["sale.order"].search([('name', '=', rec.name)])
				for line in copy_rec.order_line:
					for cp_line in created_all.invoice_line_ids:
						if line.product_id==cp_line.product_id:
							cp_line.acc_disAmount= line.disAmount
							cp_line.linediscPerct =line.linediscPerct
							
			elif created_no > 1:
				for single_rec in created_all:
					copy_rec = self.env["sale.order"].search([('name', '=', rec.name)])
					for line in copy_rec.order_line:
						for cp_line in single_rec.invoice_line_ids:
							if line.product_id==cp_line.product_id:
								cp_line.acc_disAmount= line.disAmount
								cp_line.linediscPerct =line.linediscPerct
						
	def amount_all(self):
		for single_rec in self:   
			subtot = amount_untaxed = amount_tax = disc = 0.0
			for rec in single_rec.order_line:
				dicAmnt = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
				disc = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
				subtot = rec.price_unit * rec.product_uom_qty - dicAmnt - disc
				rec.disAmount =	dicAmnt
				rec.price_subtotal = subtot
				amount_untaxed += subtot
				amount_tax +=  rec.tax_id.amount / 100 * subtot
			single_rec.amount_untaxed = amount_untaxed
			single_rec.amount_tax = amount_tax
			single_rec.amount_total = amount_untaxed + amount_tax

	def action_confirm(self):
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
		return super().action_confirm()
	
	
	def custom_action_draft(self):
		for record in self:
			record.state='draft'

	def custom_action_confirm(self):
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
