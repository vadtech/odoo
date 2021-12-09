from odoo import fields, models

class add_into_sales(models.Model):
	"""real name of the model"""
	_inherit ="sale.order"
	_description = "Moddification of sales table"
	price_list=fields.Many2one('product.pricelist',string="Price list")
	total_dis=fields.Integer( string='Total Discount')
	total_dis_line=fields.Integer(string='Total line')
	client_order_ref2 = fields.Char(string='Customer Reference 2', copy=False)
	newMarking = fields.Char(string='Marking', copy=False)
	

