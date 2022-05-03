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
	year=fields.Integer(string="Week Number")
	number_of_rec=fields.Integer(string="Sales Created" , compute="_number_of_rec" , compute_sudo=True, store=True,)
	number_of_rec2=fields.Integer(string="Sales Created")

	@api.depends("weekly_records_ids")
	def _number_of_rec(self):
		for rec in self:
			rec.number_of_rec=len(rec.weekly_records_ids)




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
