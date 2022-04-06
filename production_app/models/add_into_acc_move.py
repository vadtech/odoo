from odoo import fields, models, api ,_

class add_into_acc(models.Model):
	"""real name of the model"""
	_inherit ="account.move"
	_rec_name = "invoice_no_name"
	_description="Invoicing Application edits"

	link_prod_id = fields.Many2one('prod_order.model', string="Production ID")
	payment_ref = fields.Char(compute="_pay_ref", string="Payment Reference")

	banch_no=fields.Integer(string="Banch No")
	reference = fields.Char(string="Referece", readonly=True, required=True, copy=False, default=lambda self: _('New'))
	sales_char=fields.Char(string="Sales Order Number", related="link_prod_id.main_sales_id.name")
	invoice_no_name=fields.Char(string="Inovice Number")
	customer_name=fields.Many2one(string="Customer", related="link_prod_id.main_sales_id.partner_id")
	fake_sales_char = fields.Char(string="Sales Order Number")

	fake_sales_id = fields.Char(string="fake_sales_id")

	inv_state = fields.Selection(
		string='Invoice Status',
		tracking=True,
		default='not_invc',
		selection=[
			('invc', 'Invoiced'),
			('not_invc', 'Not Invoiced')])

	"""ALL FUNCTTION S FOR QUICK FIX """
	def fix_sales_char(self):
		for rec in self:
			rec.fake_sales_char = rec.sales_char

	def fix_updating_fields(self):
		current_rec = self.env['account.move'].search([])
		for single_rec in current_rec:
			amount_untaxed = amount_tax = dismount = 0.0
			for rec in single_rec.invoice_line_ids:
				rec.acc_disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.quantity
				dismount = rec.discount / 100 * rec.price_unit * rec.quantity
				rec.price_subtotal = rec.price_unit * rec.quantity - rec.acc_disAmount - dismount
				amount_untaxed += rec.price_subtotal
				amount_tax += rec.tax_ids.amount / 100 * rec.price_subtotal
			single_rec.amount_untaxed = amount_untaxed
			single_rec.amount_tax = amount_tax
			single_rec.amount_total = amount_untaxed + amount_tax

	def fix_log_reports(self):
		for rec in self:
			self.env['logs.model'].create({
				'acc_move_id': str(rec.invoice_no_name),
				'log_state': 'create',
				'inv_date': rec.invoice_date,
				'due_date': rec.invoice_date_due,
				'customer_no': rec.customer_name.name,
				'untaxed_amt': rec.amount_untaxed,
				'mva': rec.amount_tax,
				'total': rec.amount_total,
				'dte_create':rec.create_date,
			})

	def quick_fix_id(self):
		#initial lise first id
		correct_id=27665
		#loop through selected ids
		for rec in self:
			# change its id
			rec.invoice_no_name = correct_id + 1
			# save now correct id
			correct_id = int(rec.invoice_no_name)

	def quick_fix_inv(self):
		"""Get All Records Selected"""
		for rec in self:
			# change the invoice line state
			rec.inv_state="invc"

	def _pay_ref(self):
		for rec in self:
			bn = 8 - len(str(rec.invoice_no_name))
			y = '0' * bn
			x = self.luhn_checksum(rec.invoice_no_name)
			ne_p = '609891' + str(y) + str(rec.invoice_no_name) + str(x)
			rec.payment_ref=ne_p

	def luhn_checksum(self,card_number):
		def digits_of(n):
			return [int(d) for d in str(n)]

		digits = digits_of(card_number)
		odd_digits = digits[-1::-2]
		even_digits = digits[-2::-2]
		checksum = 0
		checksum += sum(odd_digits)
		for d in even_digits:
			checksum += sum(digits_of(d * 2))
		return checksum % 10

	@api.model
	def check_currency(self,convert):
		for record in self:
			formatted_float = "{:.2f}".format(convert)
			new_money="kr %s" %formatted_float
			return new_money

	@api.model
	def check_taxC(self,convert=[]):
		for record in self:
			for x in convert:
				res = ''.join(filter(lambda i: i.isdigit(), x))
				formatted_float = "{:.2f}".format(res)
				new_money="kr %s" %formatted_float
		return new_money

	@api.model
	def check_u_currency(self):
		for record in self:
			if record.link_prod_id.main_sales_id.partner_id.payment_fact == 'pay_3':
				new_sign = 'dkk'
			elif record.link_prod_id.main_sales_id.partner_id.payment_fact == 'pay_2':
				new_sign = 'sek'
			else:
				new_sign = 'nok'
		return new_sign


# 	def write(self, val):
# 		self.env['logs.model'].create({
# 			'acc_move_id': self.id,
# 			'log_state': 'update',
# 			'inv_date': self.invoice_date,
# 			'due_date': self.invoice_date_due,
# 			'customer_no': self.partner_id.name,
# 			'untaxed_amt': self.amount_untaxed,
# 			'mva': self.amount_tax,
# 			'total': self.amount_total,
# 		})
# 		res = super(add_into_acc, self).write(val)
# 		return res

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
		invoice_lines=[]
		x=0
		for rec in self:
			vals = {
				'acc_mv_ids': rec.id
			}
			invoice_lines.append((0, 0, vals))
			X=+1
		self.env['inv_pdfs.model'].create({
			'banch_no': reference,
			'no_invoives': x,
			'isPrinted': True,
			'bunch_inv_ids': invoice_lines
		})
		return reference

	def cal_tot_untaxed_amt(self,date_form,date_to):
		total=0
		search_result = self.env['logs.model'].search_read(["&", ('dte_create', '>=',date_form), ('dte_create', '<=',date_to)])
		for rec in search_result:
			total+=rec['untaxed_amt']
		return total

	def cal_tot_mva(self, date_form, date_to):
		mva_total=0
		search_result = self.env['logs.model'].search_read(["&", ('dte_create', '>=', date_form), ('dte_create', '<=', date_to)])
		for rec in search_result:
			mva_total += rec['mva']
		return mva_total

	def cal_log_total(self, date_form, date_to):
		mv_totals=0
		search_result = self.env['logs.model'].search_read(["&", ('dte_create', '>=', date_form), ('dte_create', '<=', date_to)])
		for rec in search_result:
			mv_totals += rec['total']
		return mv_totals


class branch_pdf_ids(models.Model):
	"""Data of bunched invoices"""
	_name = "inv_pdfs.model"
	_rec_name = "banch_no"
	_inherit = ["mail.thread", "mail.activity.mixin"]
	_description = "For keeping all branched pdfs with their Branch no"

	link_acc_id = fields.Many2one('account.move', string="Inovince ID")
	isPrinted = fields.Boolean(string="IS Printed", default=False)
	brch_no=fields.Integer(string="branch No")
	sale_order = fields.Char(related='link_acc_id.sales_char')
	custmer = fields.Char(related='link_acc_id.invoice_partner_display_name')
	inv_no= fields.Char(related='link_acc_id.invoice_no_name')

	bunch_inv_ids=fields.One2many('bunchinvoices.model', 'bunch_inv_id', string="Bunch Invoices Pfd's")

	banch_no=fields.Integer(string="Bunch Number")
	date_generated=fields.Datetime(related='create_date',string="Date Xml Generated")
	no_invoives=fields.Integer(string="Number of Invoices")
	iPrinted = fields.Boolean(string="IS Printed", default=False)

	#QUICK FIX BUNCHED INVOIVES
	def refill_records(self):
		# detect records with same banch_no
		for x in range(1,204):
			invoice_lines=[]
			record_to_copy = self.env["inv_pdfs.model"].search([('banch_no', '=', x)])
			count= self.env["inv_pdfs.model"].search_count([('banch_no', '=', x)])

			if record_to_copy.exists():
				for rec in record_to_copy:
					vals={
						'acc_mv_ids' : rec.link_acc_id.id
					}
					invoice_lines.append((0,0,vals))
				self.env['inv_pdfs.model'].create({
					'banch_no':x,
					'no_invoives':count,
					'isPrinted':True,
					'bunch_inv_ids':invoice_lines
				})


	@api.model
	def update_banch(self):
		x=0
		return x

	@api.model
	def change_to_printed(self):
		for rec in self:
			rec.isPrinted = True

	@api.model
	def cal_records(self, cur):
		refi=0
		for record in self.bunch_inv_ids:
			#if record is in nok
			if cur==2 and record.payment_fact== 'pay_1':
				refi = refi+1
			#if record is in sek
			elif cur==3 and record.payment_fact== 'pay_2':
				refi = refi+1
			#if record is in dkk
			elif cur == 4 and record.payment_fact== 'pay_3':
				refi = refi + 1
		return refi

	@api.model
	def cal_total(self,cur):
		total_amt =0
		for record in self.bunch_inv_ids:
			print()
			#if record is in nok
			if cur==2 and record.payment_fact== 'pay_1':
				total_amt += record.acc_mv_ids.amount_total_signed
			# if record is in sek
			elif cur == 3 and record.payment_fact == 'pay_2':
				total_amt += record.acc_mv_ids.amount_total_signed
			# if record is in sek
			elif cur == 4 and record.payment_fact== 'pay_3':
				total_amt += record.acc_mv_ids.amount_total_signed
			round(total_amt, 2)
		return total_amt

	@api.model
	def cal_no_tax(self,cur):
		total_not =0
		for record in self.bunch_inv_ids:
			if cur==2 and record.payment_fact== 'pay_1':
				total_not += record.acc_mv_ids.amount_untaxed
			if cur==3 and record.payment_fact== 'pay_2':
				total_not += record.acc_mv_ids.amount_untaxed
			if cur==4 and record.payment_fact== 'pay_3':
				total_not += record.acc_mv_ids.amount_untaxed
			round(total_not, 2)
		return total_not

	@api.model
	def cal_in_tax(self,cur):
		total_tax =0
		for record in self.bunch_inv_ids:
			if cur==2 and record.payment_fact== 'pay_1':
				total_tax += record.acc_mv_ids.amount_tax
			if cur==3 and record.payment_fact== 'pay_2':
				total_tax += record.acc_mv_ids.amount_tax
			if cur==4 and record.payment_fact== 'pay_3':
				total_tax += record.acc_mv_ids.amount_tax
		return total_tax

	@api.model
	def change_state(self):
		for record in self:
			record.isPrinted=True

class branch_pdf_ids2(models.Model):
	"""Database for bunched inovies ids"""
	_name = "bunchinvoices.model"
	_description = "For keeping all bunched pdfs their ids"

	bunch_inv_id = fields.Many2one('inv_pdfs.model', string="Bunch Invoices id's")
	acc_mv_ids = fields.Many2one('account.move', string="Inovine ID")
	inv_no= fields.Char(related='acc_mv_ids.invoice_no_name')
	inv_id= fields.Integer(related='acc_mv_ids.id')
	sale_order = fields.Char(related='acc_mv_ids.sales_char')
	date_due = fields.Date(related='acc_mv_ids.invoice_date_due')
	inv_date = fields.Date(related='acc_mv_ids.invoice_date')
	custmer = fields.Char(related='acc_mv_ids.invoice_partner_display_name')
	payment_fact= fields.Selection(related='acc_mv_ids.customer_name.payment_fact')
	customer_nme= fields.Char(related='acc_mv_ids.customer_name.name')

	# amt_un_tax= fields.Monetary(related='acc_mv_ids.amount_untaxed')#
	# amt_tax= fields.Integer(related='acc_mv_ids.amount_tax')
	# amt_res= fields.Integer(related='acc_mv_ids.amount_residual')
