from odoo import fields, models, api , _
from odoo.exceptions import  ValidationError

class main_hosptial(models.Model):
	"""real name of the model"""
	_name = "main_hosp.model"
	_inherit =["mail.thread","mail.activity.mixin"]
	_description = "Main Model for hosptial manangment"
	_order="id,age"


	name = fields.Char(required=True ,string="Name")
	age= fields.Integer(tracking=True)
	#sqeunce number
	reference=fields.Char(string="Reference",tracking=True,readonly=True,required=True,copy=False,
							default=lambda self: _('New'))
	gender=fields.Selection(
        string='Gender',
        required=True,
        default='male',
        selection=[
        ('male','Male'),
        ('female','Female'),
        ('other','other')])
	state=fields.Selection(
        string='Status',
        default='draft',
        selection=[
        ('draft','Draft'),
        ('confirm','Confirmed'),
        ('done','Done'),
        ('cancel','Cancelled')])

	responsible_id=fields.Many2one('res.partner',string="Responsible")
	appointement_ids=fields.One2many('appointment.model','patient_id',string="appointment")

	
	note=fields.Text(string="Description")
	appoint_count = fields.Integer(compute="_cal_appoint", string="Appointment Times")
	image=fields.Binary(string="Patient Image")
	#usinf for looops saves from singleton 
	def _cal_appoint(self):
		for rec in self:
			ap_count=self.env['appointment.model'].search_count([('patient_id','=',rec.id)])
			rec.appoint_count=ap_count

	def action_confirm(self):
		self.state='confirm'

	def action_done(self):
		self.state='done'

	def action_draft(self):
		self.state='draft'

	def action_cancelled(self):
		self.state='cancel'

	#this methodes ovride whrn you create new fields  in interfwce

	@api.model
	def create(self,vals):
		if not vals.get('note'):
			vals['note']='New Patient'
		if vals.get('reference', _('New')) == _('New'):
			vals['reference']=self.env['ir.sequence'].next_by_code('hosp_patience.seq') or _('New')
		res= super(main_hosptial,self).create(vals)
		return res

	@api.model
	def default_get(self, fields):
		vals = super(main_hosptial, self).default_get(fields)
		#if not res.get('gender'):
		#	vals['gender']='other'	
		return vals
		
	#check for condtions and constraints on specific field
	@api.constrains('name')
	def _validate_name_exist(self):
		for rec in self:
			patients=self.env['main_hosp.model'].search([('name','=',rec.name),('id','=',rec.id)])
			if patients:
				raise ValidationError(_("Name %s Already Exisit"% rec.name))

	#check for condtions and constraints on specific field
	@api.constrains('age')
	def _validate_age(self):
		for rec in self:
			if rec.age==0:
				raise ValidationError(_("Age cannot be Zero"))

	#for having more deatils in many2 one fields dropdown
	def name_get(self):
		result=[]
		for rec in self:
			name = rec.reference + ' ' + rec.name
			result.append((rec.id, name))
		return result

	#open oppoinrmtnes from smart buttons
	def action_open_appointments(self):
		
		return{
			'type':'ir.actions.act_window',
			'name':'Appointments',
			'res_model':'appointment.model',
			'domain':[('patient_id','=',self.id)],
			'context':[('default_patient_id','=',self.id)],
			'view_mode':'tree,form',
			'target':'current',
		}