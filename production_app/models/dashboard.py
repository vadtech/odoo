from odoo import fields, models, api ,_

class production_date(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "production_date.model"
	_description ="For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	production_recs_id = fields.One2many('production_recs.model', 'production_date_ids', string="Week")
	delivered_week=fields.Integer(string="Delivery Week Number")
	year=fields.Integer(string="Year")
	number_of_rec = fields.Integer(string="Number of New Orders", compute="_number_of_rec", compute_sudo=True,store=True, )
	amount_total = fields.Integer(string="Total Taxed Amount", compute="_amount_total", compute_sudo=True, store=True, )
	amount_untaxed = fields.Integer(string="Total Untaxed Amount", compute="_untaxed_amount", compute_sudo=True,store=True, )
	amount_tax = fields.Integer(string="Total tax", compute="_amount_tax", compute_sudo=True, store=True, )

	def feed_to_dashboard(self):
		#LOOP ALL PRODUCTION RECORDS
		production_records = self.env["prod_order.model"].search([])
		for record in production_records:
			#CHECK IF IT IS NEW OR IN PROD
			if record.state == "new":
				print("record deteced", record.id)
				production_lines=[]
				production_records = self.env["production_date.model"].search([('delivered_week','=',record.delivery_week)])
				if production_records.exists():
					vali ={
						'production_lines_ids':record.id
					}
					production_lines.append((0, 0, vali))
					production_records.write({
						'production_recs_id':production_lines})
	
	def reset_every(self):
		production_records = self.env["production_date.model"].search([])
		for rec in production_records:
			rec.number_of_rec=0
			rec.amount_total=0
			rec.amount_untaxed=0
			rec.amount_tax=0
			rec.write({'production_recs_id': [(5, 0, 0)]})
								
	@api.depends("production_recs_id")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec = len(rec.production_recs_id)

	@api.depends("production_recs_id")
	def _amount_total(self):
		for recs in self:
			amount_total=0
			for rec in recs.production_recs_id:
				amount_total += rec.production_lines_ids.main_sales_id.amount_total
			recs.amount_total=amount_total

	@api.depends("production_recs_id")
	def _untaxed_amount(self):
		for recs in self:
			amount_untaxed = 0
			for rec in recs.production_recs_id:
				amount_untaxed += rec.production_lines_ids.main_sales_id.amount_untaxed
			recs.amount_untaxed = amount_untaxed

	@api.depends("production_recs_id")
	def _amount_tax(self):
		for recs in self:
			amount_tax = 0
			for rec in recs.production_recs_id:
				amount_tax += rec.production_lines_ids.main_sales_id.amount_tax
			recs.amount_tax = amount_tax


class production_recs(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "production_recs.model"
	_description = "For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	production_date_ids = fields.Many2one('production_date.model', string="Weekly Number")
	production_lines_ids = fields.Many2one('prod_order.model', string="Production order lines")

	customer_name= fields.Char(related='production_lines_ids.customer_ref')
	sales_order_name = fields.Char(related='production_lines_ids.sales_id_char')
	state = fields.Selection(related='production_lines_ids.state')
	delivery_week = fields.Integer(related='production_lines_ids.delivery_week')
	sales_person = fields.Many2one(string="Sales Person", related="production_lines_ids.sales_person")

class invoice_week(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "invoice_week.model"
	_description = "For Tracking invoices in a week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	invoice_week_ids = fields.One2many('invs_week_recs.model', 'inv_weekly_id', string="Week")

	number_of_rec=fields.Integer(string="Number of Sales Created" , compute="_number_of_rec" , compute_sudo=True, store=True,)
	week_number=fields.Integer(string="Delivery Week Number",required=True)
	year=fields.Integer(string="Year")
	amount_total = fields.Integer(string="Total Taxed Amount", compute="_amount_total" )
	amount_untaxed = fields.Integer(string="Total Untaxed Amount", compute="_untaxed_amount", compute_sudo=True,							store=True, )
	amount_tax = fields.Integer(string="Total tax", compute="_amount_tax", compute_sudo=True, store=True, )

	def reset_every(self):
		production_records = self.env["invoice_week.model"].search([])
		for rec in production_records:
			rec.number_of_rec=0
			rec.amount_total=0
			rec.amount_untaxed=0
			rec.amount_tax=0
			rec.write({'invoice_week_ids': [(5, 0, 0)]})

	def feed_to_dashboard(self):
		#LOOP ALL INVOICE RECORDS
		invoice_records = self.env["account.move"].search([])
		for record in invoice_records:
			#CHECK IF IT IS A CREDIT NOTE OR A INVOICE
			if record.move_type == "out_invoice" or record.move_type=="out_refund":
				out_invoiced_lines=[]
				invoiced_records = self.env["invoice_week.model"].search([('week_number','=',record.link_prod_id.delivery_week)])
				#APPEND THE RECORD INTO DASHBOARD
				if invoiced_records.exists():
					vali ={
						'invoice_lin_ids':record.id
					}
					out_invoiced_lines.append((0, 0, vali))
					invoiced_records.write({
						'invoice_week_ids':out_invoiced_lines})

	@api.depends("invoice_week_ids")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec = len(rec.invoice_week_ids)

	@api.depends("invoice_week_ids")
	def _amount_total(self):
		for recs in self:
			amount_total = 0
			for rec in recs.invoice_week_ids:
				#CHECK IF CREDIT NOTE OR NOTE FOR SUBTRACTIONS
				if rec.move_type=="out_invoice":
					amount_total += rec.invoice_lin_ids.amount_total
				elif rec.move_type=="out_refund":
					amount_total -= rec.invoice_lin_ids.amount_total
			recs.amount_total = amount_total

	@api.depends("invoice_week_ids")
	def _untaxed_amount(self):
		for recs in self:
			amount_untaxed = 0
			for rec in recs.invoice_week_ids:
				# CHECK IF CREDIT NOTE OR NOTE FOR SUBTRACTIONS
				if rec.move_type == "out_invoice":
					amount_untaxed += rec.invoice_lin_ids.amount_untaxed
				elif rec.move_type == "out_refund":
					amount_untaxed -= rec.invoice_lin_ids.amount_untaxed
			recs.amount_untaxed = amount_untaxed

	@api.depends("invoice_week_ids")
	def _amount_tax(self):
		for recs in self:
			amount_tax = 0
			for rec in recs.invoice_week_ids:
				# CHECK IF CREDIT NOTE OR NOTE FOR SUBTRACTIONS
				if rec.move_type == "out_invoice":
					amount_tax += rec.invoice_lin_ids.amount_tax
				elif rec.move_type == "out_refund":
					amount_tax -= rec.invoice_lin_ids.amount_tax
			recs.amount_tax = amount_tax

class invs_week_recs(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "invs_week_recs.model"
	_description = "For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	inv_weekly_id = fields.Many2one('invoice_week.model', string="Weekly Number")
	invoice_lin_ids = fields.Many2one('account.move', string="Production ID")

	customer_name= fields.Char(related='invoice_lin_ids.invoice_partner_display_name')
	invoice_name = fields.Char(related='invoice_lin_ids.invoice_no_name')
	move_type = fields.Selection(related='invoice_lin_ids.move_type')
	delivery_week = fields.Integer(related='invoice_lin_ids.link_prod_id.delivery_week')



class to_be_invoice_week(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "invoice_to_be_week.model"
	_description = "For Tracking invoices in a week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	invoice_week_ids = fields.One2many('to_be_week_recs.model', 'inv_weekly_id', string="Week")

	number_of_rec=fields.Integer(string="Number of Sales Created" , compute="_number_of_rec" , compute_sudo=True, store=True,)
	week_number=fields.Integer(string="Delivery Week Number",required=True)
	year=fields.Integer(string="Year")
	amount_total = fields.Integer(string="Total Taxed Amount", compute="_amount_total", compute_sudo=True, store=True, )
	amount_untaxed = fields.Integer(string="Total Untaxed Amount", compute="_untaxed_amount", compute_sudo=True,							store=True, )
	amount_tax = fields.Integer(string="Total tax", compute="_amount_tax", compute_sudo=True, store=True, )

	def reset_every(self):
		production_records = self.env["invoice_to_be_week.model"].search([])
		for rec in production_records:
			rec.number_of_rec=0
			rec.amount_total=0
			rec.amount_untaxed=0
			rec.amount_tax=0
			rec.write({'invoice_week_ids': [(5, 0, 0)]})
			
	def feed_to_dashboard(self):
		#LOOP ALL PRODUCTION RECORDS
		production_records = self.env["prod_order.model"].search([])
		for record in production_records:
			#CHECK IF IT IS NEW OR IN PROD
			if record.state == "new" or record.state == "prod":
				production_lines=[]
				production_records = self.env["invoice_to_be_week.model"].search([('week_number','=',record.delivery_week)])
				if production_records.exists():
					vali ={
						'invoice_line_ids':record.id
					}
					production_lines.append((0, 0, vali))
					production_records.write({
						'invoice_week_ids':production_lines})

	@api.depends("invoice_week_ids")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec = len(rec.invoice_week_ids)

	@api.depends("invoice_week_ids")
	def _amount_total(self):
		for recs in self:
			amount_total = 0
			for rec in recs.invoice_week_ids:
				amount_total += rec.invoice_line_ids.main_sales_id.amount_total
			recs.amount_total = amount_total

	@api.depends("invoice_week_ids")
	def _untaxed_amount(self):
		for recs in self:
			amount_untaxed = 0
			for rec in recs.invoice_week_ids:
				amount_untaxed += rec.invoice_line_ids.main_sales_id.amount_untaxed
			recs.amount_untaxed = amount_untaxed

	@api.depends("invoice_week_ids")
	def _amount_tax(self):
		for recs in self:
			amount_tax = 0
			for rec in recs.invoice_week_ids:
				amount_tax += rec.invoice_line_ids.main_sales_id.amount_tax
			recs.amount_tax = amount_tax

class to_be_week_recs(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "to_be_week_recs.model"
	_description = "For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	inv_weekly_id = fields.Many2one('invoice_to_be_week.model', string="Weekly Number")
	invoice_line_ids = fields.Many2one('prod_order.model', string="Production ID")


	customer_name= fields.Char(related='invoice_line_ids.customer_ref')
	sales_order_name = fields.Char(related='invoice_line_ids.sales_id_char')
	state = fields.Selection(related='invoice_line_ids.state')
	delivery_week = fields.Integer(related='invoice_line_ids.delivery_week')
	sales_person = fields.Many2one(string="Sales Person", related="invoice_line_ids.sales_person")



class quotation_dashboard(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "quot_dashboard.model"
	_description = "For Tracking Quotation creation in a week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	quotation_week_ids = fields.One2many('week_quot_recs.model', 'week_quot_recs', string="Quotation Weekly Records")

	number_of_rec=fields.Integer(string="Number of Quotations Created" , compute="_number_of_rec" , compute_sudo=True, store=True,)
	week_number=fields.Integer(string="Delivery Week Number",required=True)
	year=fields.Integer(string="Year")
	amount_total = fields.Integer(string="Total Taxed Amount", compute="_amount_total", compute_sudo=True, store=True, )
	amount_untaxed = fields.Integer(string="Total Untaxed Amount", compute="_untaxed_amount", compute_sudo=True,							store=True, )
	amount_tax = fields.Integer(string="Total tax", compute="_amount_tax", compute_sudo=True, store=True, )


	def feed_to_dashboard(self):
		#LOOP ALL PRODUCTION RECORDS
		sales_records = self.env["sale.order"].search([])
		for record in sales_records:
			#CHECK IF IT IS draft OR IN sent
			if record.state == "draft" or record.state == "sent":
				sales_lines=[]
				if record.commitment_date != False:
					delivery_week = record.commitment_date.strftime("%U")
				elif record.expected_date != False:
					delivery_week = record.expected_date.strftime("%U")
				else:
					delivery_week = 0
				quot_dash_records = self.env["quot_dashboard.model"].search([('week_number','=',delivery_week)])
				if quot_dash_records.exists():
					vali ={
						'sales_line_ids':record.id
					}
					sales_lines.append((0, 0, vali))
					quot_dash_records.write({
						'quotation_week_ids':sales_lines})

	@api.depends("quotation_week_ids")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec = len(rec.quotation_week_ids)

	@api.depends("quotation_week_ids")
	def _amount_total(self):
		for recs in self:
			amount_total = 0
			for rec in recs.quotation_week_ids:
				amount_total += rec.sales_line_ids.amount_total
			recs.amount_total = amount_total

	@api.depends("quotation_week_ids")
	def _untaxed_amount(self):
		for recs in self:
			amount_untaxed = 0
			for rec in recs.quotation_week_ids:
				amount_untaxed += rec.sales_line_ids.amount_untaxed
			recs.amount_untaxed = amount_untaxed

	@api.depends("quotation_week_ids")
	def _amount_tax(self):
		for recs in self:
			amount_tax = 0
			for rec in recs.quotation_week_ids:
				amount_tax += rec.sales_line_ids.amount_tax
			recs.amount_tax = amount_tax

class week_quot_recs(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "week_quot_recs.model"
	_description = "For Tracking Quotations Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	week_quot_recs = fields.Many2one('quot_dashboard.model', string="Weekly Number")
	sales_line_ids = fields.Many2one('sale.order', string="Production ID")


	customer_name= fields.Char(related='sales_line_ids.partner_id.name')
	sales_order_name = fields.Char(related='sales_line_ids.name')
	state = fields.Selection(related='sales_line_ids.state')
	delivery_week = fields.Integer(compute="_del_date" , string="Delivery week")
	sales_person = fields.Many2one(string="Sales Person", related="sales_line_ids.user_id")


	def _del_date(self):
		for rec in self:
			if rec.sales_line_ids.commitment_date!=False:
				rec.delivery_week=rec.sales_line_ids.commitment_date.strftime("%U")
			elif rec.sales_line_ids.expected_date!=False:
				rec.delivery_week=rec.sales_line_ids.expected_date.strftime("%U")
			else:
				rec.delivery_week =0
