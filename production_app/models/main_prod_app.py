from odoo import fields, models

class prod_order_app(models.Model):
	"""real name of the model"""
	_name = "prod_order.model"
	_description = "For Production application"
	_inherit =["mail.thread","mail.activity.mixin"]
	_rec_name="customer_ref"
	_order="id,state"


	customer_ref=fields.Many2one('sale.order.line',string="sale_order_lines",tracking=True)
	main_sales_id=fields.Many2one('sale.order',string="Production_order",tracking=True)
	orderLines_ids=fields.One2many(related='main_sales_id.order_line', string="")


	order=fields.Datetime(related='main_sales_id.date_order' ,string="Order Date")
	customer_ref= fields.Char(related='main_sales_id.partner_id.name')
	deli_address=fields.Many2one(related='main_sales_id.partner_invoice_id' ,string="Delivery Address")
	delivery_date=fields.Datetime(string="Delivery Date",tracking=True)
	delivery_week=fields.Integer(string="Delivered Week",tracking=True)
	delivered_date=fields.Date(string="Delivered Date",tracking=True)

	all_del = fields.Boolean(string="All iteams as Delivered?", default=False)
	
	total_vol=fields.Float(string="Total Volume",default="0.00")
	total_wei=fields.Float(string="Total Weight",default="0.00")
	total_ite=fields.Char(string="Total iteams")

	state=fields.Selection(
        string='Status',
        tracking=True,
        default='new',
        selection=[
        ('new','New'),
        ('prod','In Production'),
        ('done','Done'),
        ('cancel','Cancel'),
        ('delivered','Delivered')])

	@api.onchange("all_del")
	def _onchange_alldel(self):
		if self.all_del==True:
			self.orderLines_ids.delivered_Qty=self.orderLines_ids.product_uom_qty
			self.state='delivered'
		else:
			pass

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
