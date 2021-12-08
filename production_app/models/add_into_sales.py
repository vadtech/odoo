from odoo import fields, models

class add_into_sales(models.Model):
	"""real name of the model"""
	_inherit ="sale.order"
	_description = "Moddification of sales table"
	price_list=fields.Many2one('product.pricelist',string="Price list")
	delv_terms=fields.Selection(
        string='Delivery Terms',
        default='del_1',
        selection=[
        ('del_1','delivery 1'),
        ('del_2','delivery 2'),
        ('del_3','delivery 3'),
        ('del_4','delivery 4')])
	total_dis=fields.Integer( string='Total Discount')
	total_dis_line=fields.Integer(string='Total line')
	all_del=fields.Boolean(string="All Iteams as Delivered?",default="False")
	client_order_ref2 = fields.Char(string='Customer Reference 2', copy=False)
	newMarking = fields.Char(string='Marking', copy=False)
	

