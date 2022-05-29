from odoo import fields, models, api ,_

class production_date(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "production_date.model"
	_description ="For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	production_recs_id = fields.One2many('production_recs.model', 'production_date_ids', string="Week")
	product_family_id = fields.One2many('product_family.model', 'production_to_fam', string="Week")

	delivered_week=fields.Integer(string="Delivery Week Number")
	update_families=fields.Boolean("Update Families", default=True)
	year=fields.Integer(string="Year")
	number_of_rec = fields.Integer(string="Number of New Orders", compute="_number_of_rec", compute_sudo=True,store=True, )
	amount_total = fields.Integer(string="Total Taxed Amount", compute="_amount_total", compute_sudo=True, store=True, )
	amount_untaxed = fields.Integer(string="Total Untaxed Amount", compute="_untaxed_amount", compute_sudo=True,store=True, )
	amount_tax = fields.Integer(string="Total tax", compute="_amount_tax", compute_sudo=True, store=True, )
	
	def create_temp(self):
		prod_date = self.env["production_date.model"].search([('number_of_rec','!=',0)])
		for rec in prod_date:
			rec.write({'product_family_id': [(5, 0, 0)]})
			self.env['product_family.model'].create({
			'production_to_fam': rec.id,
			'family_name': '',
			'Units': 0,
			})
	
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
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)


	customer_name= fields.Char(related='production_lines_ids.customer_ref')
	sales_order_name = fields.Char(related='production_lines_ids.sales_id_char')
	state = fields.Selection(related='production_lines_ids.state')
	delivery_week = fields.Integer(related='production_lines_ids.delivery_week')
	sales_person = fields.Many2one(string="Sales Person", related="production_lines_ids.sales_person")
	amount_untaxed = fields.Monetary(related='production_lines_ids.main_sales_id.amount_untaxed')
	amount_total = fields.Monetary(related='production_lines_ids.main_sales_id.amount_total')
	amount_tax = fields.Monetary(related='production_lines_ids.main_sales_id.amount_tax')

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
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)


	customer_name= fields.Char(related='invoice_lin_ids.invoice_partner_display_name')
	invoice_name = fields.Char(related='invoice_lin_ids.invoice_no_name')
	sales_char = fields.Char(related='invoice_lin_ids.sales_char')
	move_type = fields.Selection(related='invoice_lin_ids.move_type')
	delivery_week = fields.Integer(related='invoice_lin_ids.link_prod_id.delivery_week')
	amount_untaxed = fields.Monetary(related='invoice_lin_ids.amount_untaxed')
	amount_total = fields.Monetary(related='invoice_lin_ids.amount_total')
	amount_tax = fields.Monetary(related='invoice_lin_ids.amount_tax')



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
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)


	customer_name= fields.Char(related='invoice_line_ids.customer_ref')
	sales_order_name = fields.Char(related='invoice_line_ids.sales_id_char')
	state = fields.Selection(related='invoice_line_ids.state')
	delivery_week = fields.Integer(related='invoice_line_ids.delivery_week')
	sales_person = fields.Many2one(string="Sales Person", related="invoice_line_ids.sales_person")
	amount_untaxed = fields.Monetary(related='invoice_line_ids.main_sales_id.amount_untaxed')
	amount_total = fields.Monetary(related='invoice_line_ids.main_sales_id.amount_total')
	amount_tax = fields.Monetary(related='invoice_line_ids.main_sales_id.amount_tax')



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
	
	def reset_every(self):
		production_records = self.env["quot_dashboard.model"].search([])
		for rec in production_records:
			rec.number_of_rec=0
			rec.amount_total=0
			rec.amount_untaxed=0
			rec.amount_tax=0
			rec.write({'quotation_week_ids': [(5, 0, 0)]})

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
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id, readonly=True)
	

	customer_name= fields.Char(related='sales_line_ids.partner_id.name')
	sales_order_name = fields.Char(related='sales_line_ids.name')
	state = fields.Selection(related='sales_line_ids.state')
	delivery_week = fields.Integer(compute="_del_date" , string="Delivery week")
	sales_person = fields.Many2one(string="Sales Person", related="sales_line_ids.user_id")
	amount_untaxed = fields.Monetary(related='sales_line_ids.amount_untaxed')
	amount_total = fields.Monetary(related='sales_line_ids.amount_total')
	amount_tax = fields.Monetary(related='sales_line_ids.amount_tax')



	def _del_date(self):
		for rec in self:
			if rec.sales_line_ids.commitment_date!=False:
				rec.delivery_week=rec.sales_line_ids.commitment_date.strftime("%U")
			elif rec.sales_line_ids.expected_date!=False:
				rec.delivery_week=rec.sales_line_ids.expected_date.strftime("%U")
			else:
				rec.delivery_week =0
				
				
				
				
class product_family(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "product_family.model"
	_description = "For Tracking Quotations Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	production_to_fam = fields.Many2one('production_date.model', string="Production ids")

	family_name = fields.Char(string="Family Name")
	compute_me= fields.Char(string="", compute="_feed_families")
	Units = fields.Integer(string="Total units")
	Amount = fields.Integer(string="Amount")

	def _feed_families(self):
		for rec in self:
			rec.compute_me=""
			self.update_families(self.production_to_fam)

	def update_families(self,production_to_fa):
		#THIS IS TO UPDATE FAMILIES WITHIN DEFFIRENT MODELS
		if production_to_fa.update_families==True:
			print("prod is true")
			"""THIS IS FOR CREATION OF FAMILIES IN ORDERSTOCK DASHBAORD"""
			lean = []
			zeta = []
			pivot = []
			nexus = []
			meet = []
			salina = []
			santana = []
			bankett = []
			other = []
			#CHECK FOR ALL RECORDS AVAILABLE AND GET THEIR FAMILY NAME
			for rec in production_to_fa.production_recs_id.production_lines_ids.orderLines_ids:
				#GROUPING RECORDS INTO THEIR FAMILIES
				if rec.product_id.model=='lean':
					product = {
						'prod_name': rec.product_id.name,
						'model': rec.product_id.model,
						'units': rec.product_uom_qty,
						'amount': rec.price_subtotal,
					}
					print("something with lean")
					lean.append(product)
				elif rec.product_id.model=='zeta':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					zeta.append(product)
				elif rec.product_id.model=='pivot':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					print("something with pivot")
					pivot.append(product)
				elif rec.product_id.model=='nexus':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					nexus.append(product)
				elif rec.product_id.model=='meet':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					meet.append(product)
				elif rec.product_id.model=='salina':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					salina.append(product)
				elif rec.product_id.model=='santana':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					santana.append(product)
				elif rec.product_id.model=='bankett':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					bankett.append(product)
				elif rec.product_id.model=='other':
					product = {
						'prod_name': rec.product_id.name,
						'units': rec.product_uom_qty,
						'model': rec.product_id.model,
						'amount': rec.price_subtotal,
					}
					other.append(product)
			#PASS TO ANOTHER FUNCTION FOR CREATION
			self.create_fam(other)
			self.create_fam(zeta)
			self.create_fam(pivot)
			self.create_fam(nexus)
			self.create_fam(meet)
			self.create_fam(salina)
			self.create_fam(santana)
			self.create_fam(bankett)
			self.create_fam(lean)
		else:
			pass
		self.production_to_fam.update_families=False



	def create_fam(self,familie):
		# LEST REMOVE DUPLICATES WITHIN FAMILIES
		fam_tot_unt = 0
		fam_tot_amt = 0
		fam_model = ''
		for x in range(len(familie)):
			fam_tot_unt += int(familie[x]['units'])
			fam_tot_amt += int(familie[x]['amount'])
			fam_model = familie[x]['model']
		# LEST CREATE A NEW RECORD
		if fam_tot_unt != 0 and fam_tot_amt != 0:
			# LEST CREATE THE RECORD
			self.env['product_family.model'].create({
				'production_to_fam': self.production_to_fam.id,
				'family_name': fam_model,
				'Amount': fam_tot_amt,
				'Units': fam_tot_unt,
			})
