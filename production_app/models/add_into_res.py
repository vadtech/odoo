from odoo import fields, models, api ,_

class add_into_res(models.Model):
	"""real name of the model"""
	_inherit ="res.partner"
	_description="Res Partner edits"

	delv_terms = fields.Selection(
		string='Delivery Terms',
		default='del_1',
		selection=[
			('del_1', 'incoterms 2020-Ex.works'),
			('del_2', 'incoterms 2020-CPT'),
			('del_3', 'incoterms 2020-CIP'),
			('del_4', 'incoterms 2020-DPU')])
	detailed_terms=fields.Text(string='Detailed Delivery Terms')
	@api.onchange("delv_terms")
	def _onchange_delvterms(self):
		if self.delv_terms == 'del_1':
			self.detailed_terms = ""
		else:
			self.detailed_terms = "Priser i NOK. Fritt levert forhandlers adresse inkl. assuranse. Ordrer under kr. 7 500 netto belastes omkostninger/frakttillegg på netto kr. 750. Ved levering på annen vareadresse kan det kreves et tillegg på inntil 6 %, dog minimum netto kr. 900."
