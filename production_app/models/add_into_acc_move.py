from odoo import fields, models, api ,_

class add_into_res(models.Model):
	"""real name of the model"""
	_inherit ="account.move"
	_description="Invoicing Application edits"

	link_prod_id = fields.Many2one('prod_order.model', string="Production ID")
	banch_no=fields.Integer(string="Banch No")
	sales_char=fields.Char(string="Sales Order Number", related="link_prod_id.main_sales_id.name")
	
	inv_state = fields.Selection(
		string='Invoice Status',
		tracking=True,
		default='not_invc',
		selection=[
			('invc', 'Invoiced'),
			('not_invc', 'Not Invoiced')])
	
	def write(self, val):
		self.env['logs.model'].create({
			'acc_move_id': self.id,
			'log_state': 'update',
			'inv_date': self.invoice_date,
			'due_date': self.invoice_date_due,
			'customer_no': self.partner_id.name,
			'untaxed_amt': self.amount_untaxed,
			'mva': self.amount_tax,
			'total': self.amount_total,
		})
		res = super(add_into_acc, self).write(val)
		return res
	
	def auto_mate(self):
		vali={}
		for record in self:
			record_to_update = self.env["account.move"].search([('id', '=', record.id)])
			if record_to_update.exists():
				vali = {
					'inv_state': 'invc',}
			record_to_update.write(vali)
	
	@api.model
	def convert_to_float(self,convert):
		save=float(convert)
		return save

	@api.model
	def convert_to_int(self,convert):
		new_int=int(convert)
		return new_int

	@api.model
	def extract_digits(self,convert):
		change=str(convert)
		res = ''.join(filter(lambda i: i.isdigit(), change))
		return res
	
	@api.model
	def count_banch(self):
		for record in self:
			reference= self.env['ir.sequence'].next_by_code('banch_no.seq') or _('New')
			break
		return reference

	
	
