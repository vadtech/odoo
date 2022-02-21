from odoo import fields, models, api , _
from datetime import datetime
from datetime import timedelta


class report_logs(models.TransientModel):
	"""real name of the model"""
	_name = "log_wiz.model"
	_description = "report logs"

	date_form = fields.Date(required=True ,string="Date From")
	date_to = fields.Date(required=True ,string="Date To")

	def report_logs_appoint(self):
		search_result=self.env['logs.model'].search_read(["&",('create_date','>=',self.date_form),('create_date','<=',self.date_to)])
		data={
			'form':self.read()[0],
			'search_result':search_result,
		}
		return self.env.ref('production_app.log_report_option').report_action(self,data=data)
	
	
class send_print_eidts(models.TransientModel):
	_inherit = 'account.invoice.send'
	_description = 'edit account send'

	def send_and_print_action(self):
		for record in self:
			record.invoice_ids.inv_state='invc'
		return super().send_and_print_action()	
	



class report_royalties(models.TransientModel):
	"""real name of the model"""
	_name = "royalties.model"
	_description = "royalties Model"

	date_month = fields.Selection(
		string='Select Month',
		selection=[
			('01', 'January'),
			('02', 'February'),
			('03', 'March'),
			('04', 'April'),
			('05', 'May'),
			('06', 'June'),
			('07', 'July'),
			('08', 'August'),
			('09', 'September'),
			('10', 'October'),
			('11', 'November'),
			('12', 'December')])

	year = fields.Selection(
		string='Select Year',
		selection=[
			('2020', '2020'),
			('2021', '2021'),
			('2022', '2022'),
			('2023', '2023')])

	model = fields.Selection(
		string='Model',
		default='other',
		selection=[
		('lean', 'Lean'),
		('zeta', 'Zeta'),
		('pivot', 'Pivot'),
		('nexus', 'Nexus'),
		('meet', 'Meet'),
		('salina', 'Salina'),
		('santana', 'Santana'),
		('bankett', 'Bankett'),
		('other', 'Other')])

	def royalties_lean_report(self):
		date_from = "01/" + str(self.date_month) + "/" + str(self.year)
		Begindate = datetime.strptime(date_from, "%d/%m/%Y")
		Enddate = Begindate + timedelta(days=30)
		search_result = self.env['account.move'].search(["&", ('create_date', '>=', Begindate), ('create_date', '<=', Enddate)])
		model_need = []
		print(self.model)
		for rec in search_result:
			for lines in rec.invoice_line_ids:
				if lines.product_id.model == self.model:
					product = {
					'prod_name': lines.product_id.name,
					'units': lines.quantity,
					'amount': lines.price_subtotal,
					}
					model_need.append(product)

		lean_tot_units = 0
		lean_tot_amt = 0

		for rec in range(len(model_need)):
			for sub_rec in range(rec + 1, len(model_need)):
				if model_need[rec] != {} and model_need[sub_rec] != {}:
					if model_need[rec]['prod_name'] == model_need[sub_rec]['prod_name']:
						model_need[rec]['units'] += model_need[sub_rec]['units']
						model_need[rec]['amount'] += model_need[sub_rec]['amount']
						model_need[sub_rec].clear()

		if model_need[rec] != {}:
			lean_tot_units += model_need[rec]['units']
			lean_tot_amt += model_need[rec]['amount']

		data = {
			'model':self.model,
			'month': self.date_month,
			'year': self.year,
			'lean_tot_units': lean_tot_units,
			'lean_tot_amt': lean_tot_amt,
			'model_need': [i for i in model_need if i],
		}
		return self.env.ref('production_app.royalties_option').report_action(self, data=data)



