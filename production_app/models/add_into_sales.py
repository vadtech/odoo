from odoo import fields, models, api
import datetime
from datetime import date
from datetime import timedelta


class add_into_sales(models.Model):
    """real name of the model"""
    _inherit = "sale.order"
    _description = "Moddification of sales table"
    price_list = fields.Many2one('product.pricelist', string="Price list")
    total_dis = fields.Integer(string='Total Discount')
    total_dis_line = fields.Integer(string='Total line')
    client_order_ref2 = fields.Char(string='Customer Reference 2')
    client_order_ref = fields.Char(string='Customer Reference',copy=True)
    newMarking = fields.Char(string='Marking')
    previous_sales_name = fields.Char(string='Marking')
    update_dashbaord = fields.Boolean(string='Update Dashboard', default=False, compute="_update_dashboard")


    @api.model
    def check_u_currency(self):
        for record in self:
            if record.partner_id.payment_fact == 'pay_3':
                new_sign = 'dkk'
            elif record.partner_id.payment_fact == 'pay_2':
                new_sign = 'sek'
            else:
                new_sign = 'nok'
        return new_sign
    
    def _update_dashboard(self):
        for rec in self:
            if rec.update_dashbaord==False:
                rec.env['quot_dashboard.model'].reset_every()
                rec.env['quot_dashboard.model'].feed_to_dashboard()
                rec.update_dashbaord=True
            else:
                rec.update_dashbaord = True

    def copy(self, default=None):
        default = {}
        default['previous_sales_name'] = self.name
        return super(add_into_sales, self).copy(default)

    def create_to_invoice(self):
        """THIS IS TO PUSH SALES RECORDS INTO CREDIT NOTE AND ITS INVOICES"""
        for record in self:
            invoice_lines = []
            inv_lines = []
            temp_ids = []
            # CREATE A RECORD IN PRODUCTION APP
            for line in record.order_line:
                vals = {
                    'name_id': int(line.id),
                    'line_mark': line.linMarking,
                    'product_order': line.name,
                    'product_ints': line.prod_ist,
                    'qunt': line.product_uom_qty,
                }
                temp_ids.append((0, 0, vals))
            self.env["prod_order.model"].create(
                {
                    "main_sales_id": record.id,
                    'state': 'delivered',
                    "pro_order_ids": temp_ids,
                }
            )
            # CREATE INVOICE APPLICATION TAKING FROM PRODUCTION APP
            create_in_inv = self.env["prod_order.model"].search([('main_sales_id', '=', record.id)])
            # LOOP THROUGH ORDER LINES
            for lin in create_in_inv.orderLines_ids:
                vals = {
                    'name': lin.name,
                    'discount': lin.discount,
                    'price_unit': lin.price_unit,
                    'quantity': lin.product_uom_qty,
                    'product_id': lin.product_id.id,
                    'product_uom_id': lin.product_uom.id,
                    'acc_disAmount': lin.disAmount,
                    'linediscPerct': lin.linediscPerct,
                    'tax_ids': [(6, 0, lin.tax_id.ids)],
                    'sale_line_ids': [(6, 0, [lin.id])],
                }
                inv_lines.append((0, 0, vals))
            # CREATE INVOICE IN ACCOUNT_MOVE
            self.env['account.move'].create({
                'link_prod_id': create_in_inv.id,
                'invoice_no_name': self.env['ir.sequence'].next_by_code('invoice.seq'),
                'inv_state': 'not_invc',
                'ref': create_in_inv.main_sales_id.client_order_ref,
                'state': 'draft',
                'move_type': 'out_invoice',
                'invoice_origin': create_in_inv.main_sales_id.name,
                'invoice_user_id': create_in_inv.main_sales_id.user_id.id,
                'partner_id': create_in_inv.main_sales_id.partner_invoice_id.id,
                'currency_id': create_in_inv.main_sales_id.pricelist_id.currency_id.id,
                'invoice_line_ids': inv_lines,

            })

            record_to_update = self.env["account.move"].search([('link_prod_id', '=', create_in_inv.id)])
            # UPDATE AND CREATE FOR ACCOUNT MOVE
            if record_to_update.exists():
                vali = {
                    'state': 'posted',
                    'invoice_date': date.today(),
                    'invoice_date_due': date.today() + timedelta(days=30),
                }
                record_to_update.write(vali)
                # check if a record is in sek currency
                if record_to_update.customer_name.payment_fact == 'pay_3':
                    cur = 'DKK'
                    rate_dkk = self.env['res.currency'].search([('name', '=', 'DKK')], limit=1).rate
                    amt_un_tax = record_to_update.amount_untaxed * rate_dkk
                    amt_tax = record_to_update.amount_tax * rate_dkk
                    amt_total = record_to_update.amount_total * rate_dkk
                elif record_to_update.customer_name.payment_fact == 'pay_2':
                    cur = 'SEK'
                    rate_sek = self.env['res.currency'].search([('name', '=', 'SEK')], limit=1).rate
                    amt_un_tax = record_to_update.amount_untaxed * rate_sek
                    amt_tax = record_to_update.amount_tax * rate_sek
                    amt_total = record_to_update.amount_total * rate_sek
                else:
                    cur = 'NOK'
                    amt_un_tax = record_to_update.amount_untaxed
                    amt_tax = record_to_update.amount_tax
                    amt_total = record_to_update.amount_total
                self.env['logs.model'].create({
                    'acc_move_id': record_to_update.invoice_no_name,
                    'inv_date': record_to_update.invoice_date,
                    'due_date': record_to_update.invoice_date_due,
                    'customer_no': record_to_update.customer_name.name,
                    'untaxed_amt': amt_un_tax,
                    'mva': amt_tax,
                    'total': amt_total,
                    'dte_create': record_to_update.invoice_date,
                    'curncy': cur,
                })

            # CREATE IN CREDIT NOTE IN INVOICE APPLICATION
            inv_lines = []
            create_in_inv = self.env["prod_order.model"].search([('main_sales_id', '=', record.id)])
            for lin in create_in_inv.orderLines_ids:
                vals = {
                    'name': lin.name,
                    'discount': lin.discount,
                    'price_unit': lin.price_unit,
                    'quantity': lin.product_uom_qty,
                    'product_id': lin.product_id.id,
                    'product_uom_id': lin.product_uom.id,
                    'acc_disAmount': lin.disAmount,
                    'linediscPerct': lin.linediscPerct,
                    'tax_ids': [(6, 0, lin.tax_id.ids)],
                    'sale_line_ids': [(6, 0, [lin.id])],
                }
                inv_lines.append((0, 0, vals))
            self.env['account.move'].create({
                'link_prod_id': create_in_inv.id,
                'invoice_no_name': self.env['ir.sequence'].next_by_code('invoice.seq'),
                'inv_state': 'not_invc',
                'ref': create_in_inv.main_sales_id.client_order_ref,
                'state': 'draft',
                'move_type': 'out_refund',
                'invoice_origin': create_in_inv.main_sales_id.name,
                'invoice_user_id': create_in_inv.main_sales_id.user_id.id,
                'partner_id': create_in_inv.main_sales_id.partner_invoice_id.id,
                'currency_id': create_in_inv.main_sales_id.pricelist_id.currency_id.id,
                'invoice_line_ids': inv_lines,

            })
            record_to_update = self.env["account.move"].search(
                ['&', ('link_prod_id', '=', create_in_inv.id), ('move_type', '!=', 'out_invoice')])
            if record_to_update.exists():
                vali = {
                    'state': 'posted',
                    'invoice_date': date.today(),
                    'invoice_date_due': date.today() + timedelta(days=30),
                }
                record_to_update.write(vali)
                # check if a record is in sek currency
                if record_to_update.customer_name.payment_fact == 'pay_3':
                    cur = 'DKK'
                    rate_dkk = self.env['res.currency'].search([('name', '=', 'DKK')], limit=1).rate
                    amt_un_tax = record_to_update.amount_untaxed * rate_dkk
                    amt_tax = record_to_update.amount_tax * rate_dkk
                    amt_total = record_to_update.amount_total * rate_dkk
                elif record_to_update.customer_name.payment_fact == 'pay_2':
                    cur = 'SEK'
                    rate_sek = self.env['res.currency'].search([('name', '=', 'SEK')], limit=1).rate
                    amt_un_tax = record_to_update.amount_untaxed * rate_sek
                    amt_tax = record_to_update.amount_tax * rate_sek
                    amt_total = record_to_update.amount_total * rate_sek
                else:
                    cur = 'NOK'
                    amt_un_tax = record_to_update.amount_untaxed
                    amt_tax = record_to_update.amount_tax
                    amt_total = record_to_update.amount_total
                self.env['logs.model'].create({
                    'acc_move_id': record_to_update.invoice_no_name,
                    'inv_date': record_to_update.invoice_date,
                    'due_date': record_to_update.invoice_date_due,
                    'customer_no': record_to_update.customer_name.name,
                    'untaxed_amt': amt_un_tax,
                    'mva': amt_tax,
                    'total': amt_total,
                    'dte_create': record_to_update.invoice_date,
                    'curncy': cur,
                })
            # do calculation for invoice
            # get old credit note and old invoice
            new_invoice = self.env["account.move"].search(
                ['&', ('link_prod_id', '=', create_in_inv.id), ('move_type', '=', 'out_invoice')])
            new_credit = self.env["account.move"].search(
                ['&', ('link_prod_id', '=', create_in_inv.id), ('move_type', '=', 'out_refund')])
            old_credit = self.env["account.move"].search(
                ['&', ('sales_char', '=', create_in_inv.main_sales_id.previous_sales_name),
                 ('move_type', '=', 'out_refund')])
            old_invoice = self.env["account.move"].search(
                ['&', ('sales_char', '=', create_in_inv.main_sales_id.previous_sales_name),
                 ('move_type', '=', 'out_invoice')])

            # calaclute discount per each invoice line
            for lin in old_invoice.invoice_line_ids:
                # CHECKS FOR SAME NAME WITHIN OLD RECOD AND NEW RECORD IF SAME LEST DO MATH
                for recs in old_credit.invoice_line_ids:
                    for new_rec in new_invoice.invoice_line_ids:
                        if lin.name == recs.name and lin.name == new_rec.name:
                            # calculte to be subtotal
                            to_be_subtotal = lin.price_subtotal - recs.price_subtotal
                            # calacultor discount
                            if lin.price_unit == 0 or lin.quantity == 0:
                                new_discount = 0
                            else:
                                new_discount =(100*((lin.price_unit * lin.quantity) - to_be_subtotal ))/ (lin.price_unit * lin.quantity)
                            new_rec.discount = new_discount
                        else:
                            pass

            for lin in old_invoice.invoice_line_ids:
                # CHECKS FOR SAME NAME WITHIN OLD RECOD AND NEW RECORD IF SAME LEST DO MATH
                for recs in old_credit.invoice_line_ids:
                    for new_rec in new_credit.invoice_line_ids:
                        if lin.name == recs.name and lin.name == new_rec.name:
                            # calculte to be subtotal
                            to_be_subtotal = lin.price_subtotal - recs.price_subtotal
                            # calacultor discount
                            if lin.price_unit == 0 or lin.quantity == 0:
                                new_discount = 0
                            else:
                                new_discount =(100*((lin.price_unit * lin.quantity) - to_be_subtotal ))/ (lin.price_unit * lin.quantity)
                            new_rec.discount = new_discount
                        else:
                            pass

    def lest_fix_line_disc(self):
        current_rec = self.env['sale.order'].search([])
        for rec in current_rec:
            created_all = self.env["account.move"].search([('sales_char', '=', rec.name)])
            created_no = self.env["account.move"].search_count([('sales_char', '=', rec.name)])
            if created_no == 1:
                copy_rec = self.env["sale.order"].search([('name', '=', rec.name)])
                for line in copy_rec.order_line:
                    for cp_line in created_all.invoice_line_ids:
                        if line.product_id == cp_line.product_id:
                            cp_line.acc_disAmount = line.disAmount
                            cp_line.linediscPerct = line.linediscPerct

            elif created_no > 1:
                for single_rec in created_all:
                    copy_rec = self.env["sale.order"].search([('name', '=', rec.name)])
                    for line in copy_rec.order_line:
                        for cp_line in single_rec.invoice_line_ids:
                            if line.product_id == cp_line.product_id:
                                cp_line.acc_disAmount = line.disAmount
                                cp_line.linediscPerct = line.linediscPerct
                                
    def amount_all(self):
        #take one record
        for single_rec in self:
            amount_untaxed = amount_tax = 0.0
            #open it and get access it to its order line
            for rec in single_rec.order_line:
                rec.disAmount = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
                dismount = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
                rec.price_subtotal = (rec.price_unit * rec.product_uom_qty) - rec.disAmount - dismount
                amount_untaxed += rec.price_subtotal
                amount_tax += rec.tax_id.amount / 100 * rec.price_subtotal
            single_rec.amount_untaxed = amount_untaxed
            single_rec.amount_tax = amount_tax
            single_rec.amount_total = amount_untaxed + amount_tax
            
            
#     def amount_all(self):
#         for single_rec in self:
#             subtot = amount_untaxed = amount_tax = disc = 0.0
#             for rec in single_rec.order_line:
#                 dicAmnt = rec.linediscPerct / 100 * rec.price_unit * rec.product_uom_qty
#                 disc = rec.discount / 100 * rec.price_unit * rec.product_uom_qty
#                 subtot = rec.price_unit * rec.product_uom_qty - dicAmnt - disc
#                 rec.disAmount = dicAmnt
#                 rec.price_subtotal = subtot
#                 amount_untaxed += subtot
#                 amount_tax += rec.tax_id.amount / 100 * subtot
#             single_rec.amount_untaxed = amount_untaxed
#             single_rec.amount_tax = amount_tax
#             single_rec.amount_total = amount_untaxed + amount_tax

     def action_confirm(self):
        self.state = ""
        #PUSH RECORDS TO PRODUCTION APPLICATION
        for record in self:
            created_all = self.env["prod_order.model"].search_count([('main_sales_id', '=', record.id)])
            temp_ids = []
            if created_all == 0:
                for line in record.order_line:
                    vals = {
                        'name_id': int(line.id),
                        'line_mark': line.linMarking,
                        'product_order': line.name,
                        'product_ints': line.prod_ist,
                        'qunt': line.product_uom_qty,
                    }
                    temp_ids.append((0, 0, vals))
                self.env["prod_order.model"].create(
                    {
                        "main_sales_id": record.id,
                        "pro_order_ids": temp_ids,
                    }
                )
            else:
                pass
            # UPDATE IN QUOTATION CREATED STAGE
            remove_in_q= self.env["week_quot_recs.model"].search([('sales_line_ids', '=', record.id)])
            remove_in_q.unlink()
        production_records = self.env["production_date.model"].search([])
        #CLEAR UP ALL ORDER STOCK TO UPDATE
        for rec in production_records:
            rec.number_of_rec = 0
            rec.amount_total = 0
            rec.amount_untaxed = 0
            rec.amount_tax = 0
            rec.write({'production_recs_id': [(5, 0, 0)]})

        production_records = self.env["invoice_to_be_week.model"].search([])
        for rec in production_records:
            rec.number_of_rec = 0
            rec.amount_total = 0
            rec.amount_untaxed = 0
            rec.amount_tax = 0
            rec.write({'invoice_week_ids': [(5, 0, 0)]})

        #UPDATE IN ORDER STOCK
        production_records = self.env["prod_order.model"].search([])
        for record in production_records:
            # CHECK IF IT IS NEW AND INTO ORDER STOCK
            if record.state == "new":
                production_lines = []
                production_records = self.env["production_date.model"].search(
                    [('delivered_week', '=', record.delivery_week)])
                if production_records.exists():
                    vali = {
                        'production_lines_ids': record.id
                    }
                    production_lines.append((0, 0, vali))
                    production_records.write({
                        'production_recs_id': production_lines})
                production_lines = []
                #ADD IT INTO TO BE INVOICED DASHBOARD
                production_records = self.env["invoice_to_be_week.model"].search(
                    [('week_number', '=', record.delivery_week)])
                if production_records.exists():
                    vali = {
                        'invoice_line_ids': record.id
                    }
                    production_lines.append((0, 0, vali))
                    production_records.write({
                        'invoice_week_ids': production_lines})
            #CHECK IF IT IS PROD ADD INTO TO BE INVOICED
            elif record.state == "prod":
                production_lines = []
                production_records = self.env["invoice_to_be_week.model"].search(
                    [('week_number', '=', record.delivery_week)])
                if production_records.exists():
                    vali = {
                        'invoice_line_ids': record.id
                    }
                    production_lines.append((0, 0, vali))
                    production_records.write({
                        'invoice_week_ids': production_lines})
        return super().action_confirm()

    def custom_action_draft(self):
        for record in self:
            record.state = 'draft'

    def custom_action_confirm(self):
        self.state = "done"
        for record in self:
            created_all = self.env["prod_order.model"].search_count([('main_sales_id', '=', record.id)])
            temp_ids = []
            if created_all == 0:
                for line in record.order_line:
                    vals = {
                        'name_id': int(line.id),
                        'line_mark': line.linMarking,
                        'product_order': line.name,
                        'product_ints': line.prod_ist,
                        'qunt': line.product_uom_qty,
                    }
                    temp_ids.append((0, 0, vals))
                self.env["prod_order.model"].create(
                    {
                        "main_sales_id": record.id,
                        "pro_order_ids": temp_ids,
                    }
                )
            else:
                pass
