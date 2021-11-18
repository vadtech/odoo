from odoo import fields, models, api , _
from odoo.exceptions import UserError, ValidationError


class patient_appoint(models.Model):
	"""real name of the model"""
	_name = "appointment.model"
	_inherit =["mail.thread","mail.activity.mixin"]
	_description = "For bookings of appointerments"
	_rec_name="patient_id"

	patient_id=fields.Many2one('main_hosp.model',string="Patient")


	Doc=fields.Many2one('save_doctor.model',string="Doctor")
	descrip=fields.Text(string="Description")
	age= fields.Integer(related='patient_id.age',tracking=True, string='Age')
	refer=fields.Char(string="Reference",tracking=True,readonly=True,required=True,copy=False,
							default=lambda self: _('New'))
	state=fields.Selection(
        string='Status',
        default='draft',
        selection=[
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('done','Done'),
        ('cancel','Cancelled')])

	gender=fields.Selection(
        string='Gender',
        required=True,
        default='male',
        selection=[
        ('male','Male'),
        ('female','Female'),
        ('other','other')])

	date_apppoint=fields.Date(string="Date")
	prescrip=fields.Text(string="Prescription")
	pescrption_ids=fields.One2many('appointment_pescrp.model','appointment_id',string="Appointment Pescrptions")

	def action_url(self):
		return {
		'type': 'ir.actions.act_url',
		'target':'new',
		'url': 'file:///home/stan/Downloads/Patient%20Card(4).pdf',
		}


	def action_confirm(self): 
		#search function with and 
		patients_join = self.env['main_hosp.model'].search([('state','=','confirm'),('gender','=','male')])
		print("PATIES FORM US ",patients_join)
		#search function with or 
		patients_joi = self.env['main_hosp.model'].search(['|',('state','=','confirm'),('gender','=','male')])
		print("PATIES FORM US ",patients_joi)
		#search count
		patients_jo = self.env['main_hosp.model'].search_count(['|',('state','=','confirm'),('gender','=','male')])
		print("PATIES FORM US ",patients_jo)

		#reference model
		patient_jo = self.env.ref['hospital.hospital_patince_seq'].search_count(['|',('state','=','confirm'),('gender','=','male')])
		print("PATIES FORM US ",patients_jo)
		self.state='confirm'
		hospital_patince_seq

	def action_done(self):
		self.state='done'

	def action_draft(self):
		self.state='draft'

	def action_cancelled(self):
		self.state='cancel'

	@api.onchange('patient_id')
	def onchange_patient_id(self):
		if self.patient_id:
			if self.patient_id.gender:
				self.gender=self.patient_id.gender
			else:
				self.gender=''
			if self.patient_id.note:
				self.descrip=self.patient_id.note

			else:
				self.descrip=''
	#this methodes ovride whrn you create new fields  in interfwce
	@api.model
	def create(self,vals):
		if not vals.get('descrip'):
			vals['descrip']='New Appointment needed to be attended to'
		if vals.get('refer', _('New')) == _('New'):
			vals['refer']=self.env['ir.sequence'].next_by_code('appointment.seq') or _('New')
		res= super(patient_appoint,self).create(vals)
		return res

	#ovrises delete funtion	
	def unlink(self):
	 	if self.state=='done':
	 		raise ValidationError("You cannot Delete %s as it is in Done State" %self.refer)
	 		return super(patient_appoint, self).unlink()

class appointment_pescrp(models.Model):
	"""real name of the model"""
	_name = "appointment_pescrp.model"
	_description = "For Appointerments Pescriptions"

	Name=fields.Char(string="Medicine Name")
	Qty=fields.Integer(string="Quantity")
	appointment_id=fields.Many2one('appointment.model',string="appointment_id")
