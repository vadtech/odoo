from odoo import fields, models, api ,_

class production_date(models.Model):
	"""THIS IS TO LOG INVOICE'S DASHBOARD"""
	_name = "production_date.model"
	_description ="For Tracking Sales Records in Production in A week"
	_rec_name="id"
	_order="id desc"

	# LINKS TO OTHER MODELS
	production_recs_id = fields.One2many('production_recs.model', 'production_date_ids', string="Week")
	delivered_week=fields.Integer(string="Delivered Week Number")
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
			if record.state == "new" or record.state=="prod":
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

	street = fields.Char(related='production_lines_ids.street')
	city = fields.Char(related='production_lines_ids.city')
	count_zw = fields.Char(related='production_lines_ids.count_zw')
	sales_person = fields.Many2one(string="Sales Person", related="production_lines_ids.sales_person")
