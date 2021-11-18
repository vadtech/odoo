from odoo import fields, models, api , _

class create_appoint(models.TransientModel):
	"""real name of the model"""
	_name = "create.appoint.wizard"
	_description = "It easily creates appointments through a wiz"

	Date = fields.Date(required=True ,string="Date Appointment")
	patient_id=fields.Many2one('main_hosp.model',string="Patient")


	@api.model
	def default_get(self,fields):
		res=super(create_appoint, self).default_get(fields)
		res['patient_id']=self._context.get('active_id')
		return res

	def action_create_appoint(self):
		vals={
			'patient_id':self.patient_id.id,
			'date_apppoint':self.Date
		}
		patience_rec=self.env['appointment.model'].create(vals)
		return {
            'name': {'Appointment'},
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'appointment.model',
            'res_id': patience_rec.id,
            'target':'new',
        }

	def action_view_appoint(self):
		action = self.env.ref('hospital.appointment_action').read()[0]
		#for xml_id for reading actions another method
		action['domain']=[('patient_id','=',self.patient_id.id)]
		return action
