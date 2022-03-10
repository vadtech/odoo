from odoo import fields, models, api, _


class add_into_acc(models.Model):
    """real name of the model"""
    _inherit = "account.move"
    _description = "Invoicing Application edits"

    link_prod_id = fields.Many2one('prod_order.model', string="Production ID")
    payment_ref = fields.Char(compute="_pay_ref", string="Payment Reference")

    banch_no = fields.Integer(string="Banch No")
    reference = fields.Char(string="Referece", readonly=True, required=True, copy=False, default=lambda self: _('New'))
    sales_char = fields.Char(string="Sales Order Number", related="link_prod_id.main_sales_id.name")
    invoice_no_name = fields.Char(string="Inovice Number")
    customer_name = fields.Many2one(string="Customer", related="link_prod_id.main_sales_id.partner_id")
    inv_state = fields.Selection(
        string='Invoice Status',
        tracking=True,
        default='not_invc',
        selection=[
            ('invc', 'Invoiced'),
            ('not_invc', 'Not Invoiced')])
    
    """fake fields"""
	fake_sales_id=fields.Char(string="Sales Order Number")
    
	""" fake functions to fix Staff """
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

			
    def _pay_ref(self):
        for rec in self:
            bn = 8 - len(str(rec.invoice_no_name))
            y = '0' * bn
            x = self.luhn_checksum(rec.invoice_no_name)
            ne_p = '609891' + str(y) + str(rec.invoice_no_name) + str(x)
            rec.payment_ref = ne_p

    def luhn_checksum(self, card_number):
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
    def check_currency(self, convert):
        for record in self:
            formatted_float = "{:.2f}".format(convert)
            new_money = "kr %s" % formatted_float
            return new_money

    @api.model
    def check_taxC(self, convert=[]):
        for record in self:
            for x in convert:
                res = ''.join(filter(lambda i: i.isdigit(), x))
                formatted_float = "{:.2f}".format(res)
                new_money = "kr %s" % formatted_float
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
        vali = {}
        for record in self:
            record_to_update = self.env["account.move"].search([('id', '=', record.id)])
            if record_to_update.exists():
                vali = {
                    'inv_state': 'invc', }
            record_to_update.write(vali)

    @api.model
    def convert_to_float(self, convert):
        save = float(convert)
        return save

    @api.model
    def convert_to_int(self, convert):
        new_int = int(convert)
        return new_int

    @api.model
    def extract_digits(self, convert):
        change = str(convert)
        res = ''.join(filter(lambda i: i.isdigit(), change))
        return res

    @api.model
    def count_banch(self):
        for record in self:
            reference = self.env['ir.sequence'].next_by_code('banch_no.seq') or _('New')
            break
        for rec in self:
            self.env['inv_pdfs.model'].create({
                'link_acc_id': rec.invoice_no_name,
                'isPrinted': False,
                'brch_no': reference
            })
        return reference

    def cal_tot_untaxed_amt(self, date_form, date_to):
        total = 0
        search_result = self.env['logs.model'].search_read(
            ["&", ('create_date', '>=', date_form), ('create_date', '<=', date_to)])
        for rec in search_result:
            total += rec['untaxed_amt']
        return total

    def cal_tot_mva(self, date_form, date_to):
        mva_total = 0
        search_result = self.env['logs.model'].search_read(
            ["&", ('create_date', '>=', date_form), ('create_date', '<=', date_to)])
        for rec in search_result:
            mva_total += rec['mva']
        return mva_total

    def cal_log_total(self, date_form, date_to):
        mv_totals = 0
        search_result = self.env['logs.model'].search_read(
            ["&", ('create_date', '>=', date_form), ('create_date', '<=', date_to)])
        for rec in search_result:
            mv_totals += rec['total']
        return mv_totals


class branch_pdf_ids(models.Model):
    """real name of the model"""
    _name = "inv_pdfs.model"
    _description = "For keeping all branched pdfs with their Branch no"

    link_acc_id = fields.Many2one('account.move', string="Inovince ID")
    isPrinted = fields.Boolean(string="IS Printed", default=False)
    brch_no = fields.Integer(string="branch No")
    sale_order = fields.Char(related='link_acc_id.sales_char')
    custmer = fields.Char(related='link_acc_id.invoice_partner_display_name')
    inv_no = fields.Char(related='link_acc_id.invoice_no_name')

    def print_pdf_aut(self):
        records_to_print = self.env["inv_pdfs.model"].search_read([('isPrinted', '=', False)])
        data = {
            'records_to_print': records_to_print
        }
        return self.env.ref('hos_production_app.Bunch_edited_xml').report_action(self, data=data)

    # addd this line please

    @api.model
    def update_banch(self):
        for record in self:
            reference = record.brch_no
            break
        return reference

    @api.model
    def count_records(self):
        refi = 0
        for record in self:
            refi = refi + 1
        return refi

    @api.model
    def cal_total(self):
        total_amt = 0
        for record in self:
            total_amt += record.link_acc_id.amount_total_signed
        return total_amt

    @api.model
    def cal_no_tax(self):
        total_not = 0
        for record in self:
            total_not += record.link_acc_id.amount_untaxed
        return total_not

    @api.model
    def cal_in_tax(self):
        total_tax = 0
        for record in self:
            total_tax += record.link_acc_id.amount_tax
        return total_tax

    @api.model
    def change_state(self):
        for record in self:
            record.isPrinted = True



