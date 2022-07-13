from odoo import fields, models, api ,_
from datetime import datetime
import requests
import base64

class add_into_product_temp(models.Model):
	"""real name of the model"""
	_inherit ="product.template"
	_description="Products Template Edits"
	model = fields.Selection(
		string='Model',
		default = 'other',
		selection=[
		('lean', 'Lean'),
		('zeta', 'Zeta'),
		('pivot', 'Pivot'),
		('nexus', 'Nexus'),
		('meet', 'Meet'),
		('salina', 'Salina'),
		('santana', 'Santana'),
		('bankett', 'Bankett'),
		('other', 'Other')])


class ProductImage(models.Model):
    _inherit = 'product.template'

    image_url = fields.Char(string='Image URL')

    @api.onchange('image_url')
    def _onchange_image_url(self):
        """ function to load image from URL """
        image = False
        if self.image_url:
            image = base64.b64encode(requests.get(self.image_url).content)
        self.image_1920 = image

    def load_pictures(self):
        for rec in self:
            image = False
            if rec.image_url:
                image = base64.b64encode(requests.get(rec.image_url).content)
            rec.image_1920 = image

class ProductVariantImage(models.Model):
    _inherit = 'product.product'

    image_url = fields.Char(string='Image URL')

    @api.onchange('image_url')
    def _onchange_image_url(self):
        """ function to load image from URL in product variant"""
        image = False
        if self.image_url:
            image = base64.b64encode(requests.get(self.image_url).content)
        self.image_1920 = image
