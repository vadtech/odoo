from odoo import fields, models, api , _

class save_doctors(models.Model):
	"""real name of the model"""
	_name = "save_doctor.model"
	_inherit =["mail.thread","mail.activity.mixin"]
	_description = "For Saving Doctors and their manangment"
	_rec_name="doc_name"
	_order="doc_name"

	doc_name = fields.Char(required=True ,string="Name",default="Doc")
	age= fields.Integer(tracking=True)
	#sqeunce number
	reference_id=fields.Char(string="Reference",tracking=True,readonly=True,required=True,copy=False,default=lambda self: _('New'))
	gender=fields.Selection(string='Gender',required=True,default='male',selection=[('male','Male'),('female','Female'),('other','other')])
	image=fields.Binary(string="Photo")
	doc_appoint_count = fields.Integer(compute="_doc_cal_appoint", string="Appointment Times")
	active=fields.Boolean(string="Active",default="True")
	#usinf f=or looops saves from singleton 
	def _doc_cal_appoint(self):
		for rec in self:
			ap_count=self.env['appointment.model'].search_count([('Doc','=',rec.id)])
			rec.doc_appoint_count=ap_count

	@api.model
	def create(self,vals):
		if vals.get('reference_id', _('New')) == _('New'):
			vals['reference_id']=self.env['ir.sequence'].next_by_code('doctor.seq') or _('New')
		res= super(save_doctors,self).create(vals)
		return res      

	#ovrides copy function
	def copy(self, default=None):
		if default is None:
			default={}
		if not default.get('doc_name'):
			default['doc_name']=_("%s (Copy)",self.doc_name)
		default['age']= 18
		return super(save_doctors, self).copy(default) 

	