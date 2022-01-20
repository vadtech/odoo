from odoo import fields, models , api
import datetime
from datetime import date
from datetime import timedelta


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
