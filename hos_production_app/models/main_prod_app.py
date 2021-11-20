from odoo import fields, models

class prod_order_app(models.Model):
	"""real name of the model"""
	_name = "prod_order.model"
	_description = "For Production application"

	name=fields.Char(string="Name")
	main_sales_id=fields.Many2one('sale.order',string="Production_order")
	sales_order_line_ids=fields.Many2one('sale.order.line',string="sale_order_lines")

	order=fields.Datetime(related='main_sales_id.date_order' ,string="Date Order")
	customer_ref= fields.Char(related='main_sales_id.partner_id.name' ,string='Customer')
	deli_address=fields.Char(related='main_sales_id.delivery_add',string="Delivery Address")
	inv_address=fields.Char(related='main_sales_id.invoice_add',string="Invoicer Address")
	
	delivered_all=fields.Boolean(string="Delivered All Units",default="True")
	total_vol=fields.Float(string="Total Volume",default="0.00")
	total_wei=fields.Float(string="Total Weight",default="0.00")
	total_ite=fields.Char(string="Total iteams")

	state=fields.Selection(
        string='Status',
        default='new',
        selection=[
        ('new','New'),
        ('prod','In Production'),
        ('done','Done'),
        ('cancel','Cancel'),
        ('delivered','Delivered')])


	def action_new(self):
		self.state='new'

	def action_prod(self):
		self.state='prod'

	def action_done(self):
		self.state='done'

	def action_cancelled(self):
		self.state='cancel'


	def action_delivered(self):
		self.state='delivered'