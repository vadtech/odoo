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

	def royalties_logs_appoint(self):
		date_from="01/"+str(self.date_month)+"/"+str(self.year)
		Begindate = datetime.strptime(date_from, "%d/%m/%Y")
		Enddate = Begindate + timedelta(days=30)
		search_result=self.env['account.move'].search(["&",('create_date','>=',Begindate),('create_date','<=',Enddate)])
		lean=[]
		zeta=[]
		pivot=[]
		nexus=[]
		meet=[]
		salina=[]
		santana=[]
		bankett=[]
		other=[]
		for rec in search_result:
			for lines in rec.invoice_line_ids:
				if lines.product_id.model=='lean':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					lean.append(product)
				elif lines.product_id.model=='zeta':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					zeta.append(product)
				elif lines.product_id.model=='pivot':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					pivot.append(product)
				elif lines.product_id.model=='nexus':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					nexus.append(product)
				elif lines.product_id.model=='meet':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					meet.append(product)
				elif lines.product_id.model=='salina':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					salina.append(product)
				elif lines.product_id.model=='santana':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					santana.append(product)
				elif lines.product_id.model=='bankett':
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					bankett.append(product)
				else:
					product = {
						'prod_name': lines.product_id.name,
						'units': lines.quantity,
						'amount': lines.price_subtotal,
					}
					other.append(product)

		zeta_tot_units = 0
		zeta_tot_amt = 0
		santana_tot_units = 0
		santana_tot_amt = 0
		pivot_tot_units = 0
		pivot_tot_amt = 0
		nexus_tot_units = 0
		nexus_tot_amt = 0
		lean_tot_units = 0
		lean_tot_amt = 0
		meet_tot_units = 0
		meet_tot_amt = 0
		salina_tot_units = 0
		salina_tot_amt = 0
		other_tot_units = 0
		other_tot_amt = 0
		bankett_tot_units = 0
		bankett_tot_amt = 0

		for rec in range(len(lean)):
			for sub_rec in range(rec + 1, len(lean)):
				if lean[rec] != {} and lean[sub_rec] != {}:
					if lean[rec]['prod_name'] == lean[sub_rec]['prod_name']:
						lean[rec]['units'] += lean[sub_rec]['units']
						lean[rec]['amount'] += lean[sub_rec]['amount']
						lean[sub_rec].clear()
			if lean[rec] != {}:
				lean_tot_units += lean[rec]['units']
				lean_tot_amt += lean[rec]['amount']

		for rec in range(len(zeta)):
			for sub_rec in range(rec + 1, len(zeta)):
				if zeta[rec] != {} and zeta[sub_rec] != {}:
					if zeta[rec]['prod_name'] == zeta[sub_rec]['prod_name']:
						zeta[rec]['units'] += zeta[sub_rec]['units']
						zeta[rec]['amount'] += zeta[sub_rec]['amount']
						zeta[sub_rec].clear()
			if zeta[rec] != {}:
				zeta_tot_units += zeta[rec]['units']
				zeta_tot_amt += zeta[rec]['amount']


		for rec in range(len(pivot)):
			for sub_rec in range(rec + 1, len(pivot)):
				if pivot[rec] != {} and pivot[sub_rec] != {}:
					if pivot[rec]['prod_name'] == pivot[sub_rec]['prod_name']:
						pivot[rec]['units'] += pivot[sub_rec]['units']
						pivot[rec]['amount'] += pivot[sub_rec]['amount']
						pivot[sub_rec].clear()
			if pivot[rec] != {}:
				pivot_tot_units += pivot[rec]['units']
				pivot_tot_amt += pivot[rec]['amount']

		for rec in range(len(nexus)):
			for sub_rec in range(rec + 1, len(nexus)):
				if nexus[rec] != {} and nexus[sub_rec] != {}:
					if nexus[rec]['prod_name'] == nexus[sub_rec]['prod_name']:
						nexus[rec]['units'] += nexus[sub_rec]['units']
						nexus[rec]['amount'] += nexus[sub_rec]['amount']
						nexus[sub_rec].clear()
			if nexus[rec] != {}:
				nexus_tot_units += nexus[rec]['units']
				nexus_tot_amt += nexus[rec]['amount']

		for rec in range(len(meet)):
			for sub_rec in range(rec + 1, len(meet)):
				if meet[rec] != {} and meet[sub_rec] != {}:
					if meet[rec]['prod_name'] == meet[sub_rec]['prod_name']:
						meet[rec]['units'] += meet[sub_rec]['units']
						meet[rec]['amount'] += meet[sub_rec]['amount']
						meet[sub_rec].clear()
			if meet[rec] != {}:
				meet_tot_units += meet[rec]['units']
				meet_tot_amt += meet[rec]['amount']

		for rec in range(len(salina)):
			for sub_rec in range(rec + 1, len(salina)):
				if salina[rec] != {} and salina[sub_rec] != {}:
					if salina[rec]['prod_name'] == salina[sub_rec]['prod_name']:
						salina[rec]['units'] += salina[sub_rec]['units']
						salina[rec]['amount'] += salina[sub_rec]['amount']
						salina[sub_rec].clear()
			if salina[rec] != {}:
				salina_tot_units += salina[rec]['units']
				salina_tot_amt += salina[rec]['amount']

		for rec in range(len(other)):
			for sub_rec in range(rec + 1, len(other)):
				if other[rec] != {} and other[sub_rec] != {}:
					if other[rec]['prod_name'] == other[sub_rec]['prod_name']:
						other[rec]['units'] += other[sub_rec]['units']
						other[rec]['amount'] += other[sub_rec]['amount']
						other[sub_rec].clear()
			if other[rec] != {}:
				other_tot_units +=other[rec]['units']
				other_tot_amt += other[rec]['amount']

		for rec in range(len(santana)):
			for sub_rec in range(rec + 1, len(santana)):
				if santana[rec] != {} and santana[sub_rec] != {}:
					if santana[rec]['prod_name'] == santana[sub_rec]['prod_name']:
						santana[rec]['units'] += santana[sub_rec]['units']
						santana[rec]['amount'] += santana[sub_rec]['amount']
						santana[sub_rec].clear()
			if santana[rec] != {}:
				santana_tot_units += santana[rec]['units']
				santana_tot_amt += santana[rec]['amount']

		for rec in range(len(bankett)):
			for sub_rec in range(rec + 1, len(bankett)):
				if bankett[rec] != {} and bankett[sub_rec] != {}:
					if bankett[rec]['prod_name'] == bankett[sub_rec]['prod_name']:
						bankett[rec]['units'] += bankett[sub_rec]['units']
						bankett[rec]['amount'] += bankett[sub_rec]['amount']
						bankett[sub_rec].clear()
			if bankett[rec] != {}:
				bankett_tot_units += bankett[rec]['units']
				bankett_tot_amt += bankett[rec]['amount']

		data = {
			'lean_tot_units': lean_tot_units,
			'lean_tot_amt': lean_tot_amt,
			'zeta_tot_units': zeta_tot_units,
			'zeta_tot_amt': zeta_tot_amt,
			'pivot_tot_units': pivot_tot_units,
			'pivot_tot_amt': pivot_tot_amt,
			'nexus_tot_units': nexus_tot_units,
			'nexus_tot_amt': nexus_tot_amt,
			'salina_tot_units':salina_tot_units,
			'salina_tot_amt':salina_tot_amt,
			'santana_tot_units':salina_tot_units,
			'santana_tot_amt':salina_tot_amt,
			'meet_tot_units':meet_tot_units,
			'meet_tot_amt':meet_tot_amt,
			'bankett_tot_units':bankett_tot_units,
			'bankett_tot_amt':bankett_tot_amt,
			'other_tot_units':other_tot_units,
			'other_tot_amt':other_tot_amt,
			'month': self.date_month,
			'year':self.year,
			'other': [i for i in other if i],
			'lean': [i for i in lean if i],
			'zeta': [i for i in zeta if i],
			'pivot': [i for i in pivot if i],
			'nexus': [i for i in nexus if i],
			'meet': [i for i in meet if i],
			'salina': [i for i in salina if i],
			'santana': [i for i in santana if i],
			'bankett': [i for i in bankett if i],
		}
		return self.env.ref('hos_production_app.royalties_option').report_action(self, data=data)
	
