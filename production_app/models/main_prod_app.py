from odoo import fields, models , api
import datetime
from datetime import date
from datetime import timedelta

class prod_order_app(models.Model):
	"""real name of the model"""
	_name = "prod_order.model"
	_description = "For Production application"
	_inherit =["mail.thread","mail.activity.mixin"]
	_rec_name="customer_ref"
	_order="id desc"

	customer_ref=fields.Many2one('sale.order.line',string="sale_order_lines",tracking=True)
	main_sales_id=fields.Many2one('sale.order',string="Production_order",tracking=True,index=True,required=True)
	orderLines_ids=fields.One2many(related='main_sales_id.order_line', string="")
	sales_id_char=fields.Char(string="Sales Order Number", related="main_sales_id.name",required=True)
	pro_order_ids = fields.One2many('pro_order.model', 'prod_ids', string="Product Order")

	order=fields.Datetime(related='main_sales_id.date_order' ,string="Order Date")
	customer_ref= fields.Char(related='main_sales_id.partner_id.name')
	deli_address=fields.Many2one(related='main_sales_id.partner_shipping_id' ,string="Delivery Address")
	street=fields.Char(related='main_sales_id.partner_shipping_id.street')
	city=fields.Char(related='main_sales_id.partner_shipping_id.city')
	count_zw=fields.Char(related='main_sales_id.partner_shipping_id.country_id.name')
	sales_person=fields.Many2one(string="Sales Person", related="main_sales_id.user_id")

	
	delivery_date=fields.Datetime(string="Delivery Date")
	delivery_week=fields.Integer(compute="_del_date" ,string="Delivery Week")

	all_del = fields.Boolean(string="All iteams as Delivered?", default=False)
	total_vol=fields.Float(string="Total Volume(dm3)",default="0.00")
	total_wei=fields.Float(string="Total Weight(kg)",default="0.00")
	total_ite=fields.Char(string="Total Iteams")

	state=fields.Selection(
        string='Status',
        tracking=True,
        default='new',
        selection=[
        ('new','New'),
        ('prod','In Production'),
        ('cancel','Cancel'),
        ('delivered','Delivered')])
	
	
	""" FAKE FUNCTIONS FOR FIXING BUGS """		
	def fix_sales_char(self):
		for x in range(25000, 30000):
			record_to_copy = self.env["account.move"].search([('id', '=', x)])
			if record_to_copy.exists():
				vali = {
					'fake_sales_id': record_to_copy.sales_char,
				}
				record_to_copy.write(vali)
				
	def fix_invocie_no(self):
		for x in range(25000, 32000):
			record_to_copy = self.env["account.move"].search([('id', '=', x)])
			if record_to_copy.exists():
				vali = {
					'invoice_no_name': record_to_copy.id,
				}
				record_to_copy.write(vali)
				
	def test_me_stan(self):
		# for x in range(100):
		# 	record_to_copy = self.env["account.move"].search([('id', '=', x)])
		# 	if record_to_copy.exists():
		# 		vali = {
		# 			'new_invoice_no': record_to_copy.id,
		# 		}
		# 		record_to_copy.write(vali)
		
		for x in range(7555):
			record_to_copy = self.env["product.template"].search([('id', '=', x)])
			if record_to_copy.exists():
				check1 ="lean" in str(record_to_copy.name).lower().replace(',', '')
				check2 ="zeta" in str(record_to_copy.name).lower().replace(',', '')
				check3 ="pivot" in str(record_to_copy.name).lower().replace(',', '')
				check4 ="nexus" in str(record_to_copy.name).lower().replace(',', '')
				check5 ="meet" in str(record_to_copy.name).lower().replace(',', '')
				check6 ="salina" in str(record_to_copy.name).lower().replace(',', '')
				check7 ="santana" in str(record_to_copy.name).lower().replace(',', '')
				check8 ="bankett" in str(record_to_copy.name).lower().replace(',', '')
				check9 ="other" in str(record_to_copy.name).lower().replace(',', '')
				if check1 == True:
					record_to_copy.model="lean"
				elif check2 == True:
					record_to_copy.model = "zeta"
				elif check3 == True:
					record_to_copy.model = "pivot"
				elif check4 == True:
					record_to_copy.model = "nexus"
				elif check5 == True:
					record_to_copy.model = "meet"
				elif check6 == True:
					record_to_copy.model = "salina"
				elif check7 == True:
					record_to_copy.model = "santana"
				elif check8 == True:
					record_to_copy.model = "bankett"
				else:
					record_to_copy.model = "other"
			else:
				pass
			
	""" FAKE FUNCTIONS FOR FIXING BUGS """			
					
	def _del_week(self):
		for rec in self:
			if rec.delivery_date==False:
				pass
			else:
				rec.delivery_week = rec.delivery_date.strftime("%w")

	def _del_date(self):
		for rec in self:
			if rec.main_sales_id.commitment_date!=False:
				rec.delivery_date=rec.main_sales_id.commitment_date
				rec.delivery_week = rec.delivery_date.strftime("%U")
			elif rec.main_sales_id.expected_date!=False:
				rec.delivery_date = rec.main_sales_id.expected_date
				rec.delivery_week = rec.delivery_date.strftime("%U")
			else:
				pass
		
	@api.onchange("all_del")
	def _onchange_alldel(self):
		if self.all_del == True and self.state == 'prod':
			for rec in self.pro_order_ids:
				rec.del_qunt = rec.qunt
			self.state = 'delivered'
		else:
			if self.state == 'delivered':
				for rec in self.pro_order_ids:
					rec.del_qunt = 0
				self.state = 'prod'
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
		for record in self:
			created_all = self.env["account.move"].search_count([('link_prod_id', '=', record.id)])
			if created_all == 0:
				invoice_lines = []
				for line in record.orderLines_ids:
					vals = {
						'name': line.name,
						'discount':line.discount,
						'price_unit': line.price_unit,
						'quantity': line.product_uom_qty,
						'product_id': line.product_id.id,
						'product_uom_id': line.product_uom.id,
						'acc_disAmount': line.disAmount,
						'linediscPerct':line.linediscPerct,
						'tax_ids': [(6, 0, line.tax_id.ids)],
						'sale_line_ids': [(6, 0, [line.id])],
					}
					invoice_lines.append((0, 0, vals))
				self.env['account.move'].create({
					'link_prod_id':record.id,
					'invoice_no_name' : self.env['ir.sequence'].next_by_code('invoice.seq'),
					'inv_state':'not_invc',
					'ref': record.main_sales_id.client_order_ref,
					'state':'draft',
					'move_type': 'out_invoice',
					'invoice_origin': record.main_sales_id.name,
					'invoice_user_id': record.main_sales_id.user_id.id,
					'partner_id': record.main_sales_id.partner_invoice_id.id,
					'currency_id': record.main_sales_id.pricelist_id.currency_id.id,
					'invoice_line_ids': invoice_lines
				})
				record_to_update = self.env["account.move"].search([('link_prod_id', '=',record.id )])
				if record_to_update.exists():
					vali = {
						'state': 'posted',
						'invoice_date':date.today(),
						'invoice_date_due':date.today() + timedelta(days=30),
					}
					record_to_update.write(vali)
					self.env['logs.model'].create({
						'acc_move_id': record_to_update.id,
						'log_state': 'create',
						'inv_date': record_to_update.invoice_date,
						'due_date': record_to_update.invoice_date_due,
						'customer_no': record_to_update.customer_name.name,
						'untaxed_amt': record_to_update.amount_untaxed,
						'mva': record_to_update.amount_tax,
						'total': record_to_update.amount_total,
					})

class log_invoice_app(models.Model):
	"""real name of the model"""
	_name = "logs.model"
	_description = "For Logging Account Movement"

	acc_move_id= fields.Integer(string="Account Move")
	inv_date = fields.Date(string="Invoice Date")
	due_date = fields.Date(string="Due Date")
	customer_no = fields.Text(string="Customer NO")
	untaxed_amt = fields.Integer(string="Untaxed Amt")
	mva = fields.Integer(string="mva")
	total = fields.Integer(string="total")

	log_state = fields.Selection(
		string='log_state',
		selection=[
			('create', 'Create'),
			('delete', 'Delete'),
			('update', 'Update')])

		
class pro_ord(models.Model):
	"""real name of the model"""
	_name = "pro_order.model"
	_description = "For Logging Account Movement"

	name_id= fields.Integer()
	prod_ids = fields.Many2one('prod_order.model', string=" Main Production")

	line_mark = fields.Text(string="Line Marking")
	product_order = fields.Text(string="Art No and Description")
	product_ints = fields.Text(string="Product Instruction")
	qunt = fields.Integer(string="Quantity")
	del_qunt = fields.Integer(string="Delivered Quantity")
	
	@api.model
	def count_records(self):
		refi = 0
		for record in self:
			refi = refi + 1
		return refi
