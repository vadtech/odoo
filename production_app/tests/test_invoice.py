# coding: utf-8
from odoo.tests import tagged, TransactionCase


@tagged('production_app')
class TestInvoice(TransactionCase):
    def test_invoice_sequence(self):
        partner = self.env['res.partner'].create(
            {'display_name': 'KitKate',
             'name': 'Tim Kate',
             'title': 1,
             'email': 'tim@kate,com'})
        # creating invoice 1
        sale_order_1 = self.env['sale.order'].create(
            {'partner_id': partner.id})
        sale_order_1.action_confirm()
        prod_order_1 = self.env['prod_order.model'].search(
            [('main_sales_id', '=', sale_order_1.id)])
        prod_order_1.action_delivered()
        invoice_no_1 = self.env['account.move'].search(
            [('link_prod_id', '=', prod_order_1.id)]).invoice_no_name

        # creating invoice 2
        sale_order_2 = self.env['sale.order'].create(
            {'partner_id': partner.id})
        sale_order_2.action_confirm()
        prod_order_2 = self.env['prod_order.model'].search(
            [('main_sales_id', '=', sale_order_2.id)])
        prod_order_2.action_delivered()
        invoice_no_2 = self.env['account.move'].search(
            [('link_prod_id', '=', prod_order_2.id)]).invoice_no_name

        invoice_no_1 = int(invoice_no_1)+1
        invoice_no_1 = f'{invoice_no_1:05d}'

        self.assertEqual(invoice_no_1, invoice_no_2)
