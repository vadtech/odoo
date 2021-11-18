from odoo import fields, models, api , _

class search_appoint(models.TransientModel):
	"""real name of the model"""
	_name = "search.appoint.wizard"
	_description = "It easily searches appointments through a wiz"

	patient_id=fields.Many2one('main_hosp.model',string="Patient")

	def search_view_appoint(self):
		action = self.env.ref('hospital.appointment_action').read()[0]
		#for xml_id for reading actions another method
		action['domain']=[('patient_id','=',self.patient_id.id)]
		return action
