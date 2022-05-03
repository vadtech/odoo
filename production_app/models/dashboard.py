from odoo import fields, models, api ,_

class dashboard_week(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "weekly_no.model"
	_description = "For Tracking Dashboard Sales"
	_inherit =["mail.thread","mail.activity.mixin"]
	_rec_name="id"
	_order="id desc"

	#LINKS TO OTHER MODELS
	weekly_records_ids = fields.One2many('weekly_sales_records.model', 'weekly_no_id', string="Week")
	week_number=fields.Integer(string="Week Number",required=True)
	year=fields.Integer(string="Year")
	number_of_rec=fields.Integer(string="Number of Sales Created" , compute="_number_of_rec" , compute_sudo=True, store=True,)
	amount_total=fields.Integer(string="Total Taxed Amount" , compute="_amount_total" , compute_sudo=True, store=True,)
	amount_untaxed=fields.Integer(string="Total Untaxed Amount" , compute="_untaxed_amount" , compute_sudo=True, store=True,)
	amount_tax=fields.Integer(string="Total tax" , compute="_amount_tax" , compute_sudo=True, store=True,)

	@api.depends("weekly_records_ids")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec=len(rec.weekly_records_ids)

	@api.depends("weekly_records_ids")
	def _amount_total(self):
		for recs in self:
			amount_total=0
			for rec in recs.weekly_records_ids:
				amount_total += rec.sales_order_ids.amount_total
			recs.amount_total=amount_total

	@api.depends("weekly_records_ids")
	def _untaxed_amount(self):
		for recs in self:
			amount_untaxed=0
			for rec in recs.weekly_records_ids:
				amount_untaxed += rec.sales_order_ids.amount_untaxed
			recs.amount_untaxed=amount_untaxed

	@api.depends("weekly_records_ids")
	def _amount_tax(self):
		for recs in self:
			amount_tax = 0
			for rec in recs.weekly_records_ids:
				amount_tax += rec.sales_order_ids.amount_tax
			recs.amount_tax = amount_tax

class week_records(models.Model):
	"""THIS IS TO MAKE ALL MODELS FOR DASHBOARD"""
	_name = "weekly_sales_records.model"
	_description = "For Tracking Dashboard Sales Records"
	_inherit =["mail.thread","mail.activity.mixin"]
	_rec_name="id"
	_order="id desc"

	#LINKS TO OTHER MODELS
	weekly_no_id = fields.Many2one('weekly_no.model', string="Weekly Number")
	sales_order_ids = fields.Many2one('sale.order', string="Sales Order ID")

	sales_number = fields.Char(related='sales_order_ids.name')
	create_dte = fields.Datetime(related='sales_order_ids.create_date')
	state = fields.Selection(related='sales_order_ids.state')
