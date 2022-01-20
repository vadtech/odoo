from odoo import fields, models, api , _

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
		return self.env.ref('hos_production_app.log_report_option').report_action(self,data=data)