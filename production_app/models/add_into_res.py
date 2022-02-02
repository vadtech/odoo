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

	payment_fact = fields.Selection(
		string='Payment Factoring',
		default='pay_1',
		selection=[
			('pay_1', 'Factoring Norway'),
			('pay_2', 'Factoring Sweden'),
			('pay_3', 'Factoring Denmark'),
			('pay_4', 'English without factoring with IBAN/SWIFT'),
			('pay_5', 'Norway without factoring to VIPPS'),
			('pay_6', 'Norway without factoring to bank account'),
		])
	jurid_info=fields.Text(string='Jurisdictional Information' ,default="Fordringer etter nærværende faktura er overdratt DNB Bank ASA, Postboks 1600 Sentrum, 0021 Oslo, tileiendom. Befriende betaling kan kun skje til DNB Bank ASA. Bankkonto 7032.05.16038. Ved betaling vennligst oppgi KIDreferanse eller fakturanummer og leverandør.")
	
	@api.onchange("delv_terms")
	def _onchange_delvterms(self):
		if self.delv_terms == 'del_1':
			self.detailed_terms = ""
		else:
			self.detailed_terms = "Priser i NOK. Fritt levert forhandlers adresse inkl. assuranse. Ordrer under kr. 7 500 netto belastes omkostninger/frakttillegg på netto kr. 750. Ved levering på annen vareadresse kan det kreves et tillegg på inntil 6 %, dog minimum netto kr. 900."

	@api.onchange("payment_fact")
	def _onchange_jurid_info(self):
		if self.payment_fact == 'pay_1':
			self.jurid_info = "Fordringer etter nærværende faktura er overdratt DNB Bank ASA, Postboks 1600 Sentrum, 0021 Oslo, tileiendom. Befriende betaling kan kun skje til DNB Bank ASA. Bankkonto 7032.05.16038. Ved betaling vennligst oppgi KIDreferanse eller fakturanummer og leverandør."
		if self.payment_fact == 'pay_2':
			self.jurid_info = "Vår fordran enligt denne faktura har överlåtits til DNB Bank ASA, postboks 1600 Sentrum, N-0021 Oslo. Betalning med befriande verkan kan endast ske direkt til DNB Bank ASABankgiro i SEK 5397-0612 i DNB Bank ASA , SE-105 88 Stockholm med angivande av OCR-nummer eller leverantör och fakturanummer."
		if self.payment_fact == 'pay_3':
			self.jurid_info = "Fordringer i henhold til nærværende faktura er overdraget DNB Bank ASA, postboks 1600 Sentrum,N-0021 Oslo, til eje. Betaling med frigørende virkning kan kun ske til DNB Bank ASA.Bankkonto i DKK 5290.90.10018002 i DNB filial Danmark, Postboks 879, DK-2100 København Ø. Ved betaling bedes leverandør- og fakturanummer venligst oplyst."
		if self.payment_fact == 'pay_4':
			self.jurid_info = "IBAN/Account No: NO4315030567142 Bank: DNB Bank ASA, NO-0021 Oslo, Norway. BIC/SWIFT address: DNBANOKKXXX"
		if self.payment_fact == 'pay_5' or self.payment_fact == 'pay_6':
			self.jurid_info = "Vårt bankkontonummer: 1503.05.67142 Merk innbetalingene med fakturanummer. VAD AS, VAD-bygget, 6250Stordal Org.nr. 982812046 Selger har salgspant i de leverte varer inntil kjøpesummen med tillegg av evt. renter ogomkostninger er betalt i sin helhet. Jmfr Pantelovens § 3-14"

