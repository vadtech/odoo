from odoo import fields, models, api,_
import datetime
from odoo.exceptions import ValidationError
from datetime import date
from datetime import timedelta


class add_into_mail_templates(models.Model):
    _inherit = 'mail.template'

    template_lang=fields.Selection(
        string='Template language',
        default='eng',
        selection=[
        ('eng','English'),
        ('nor','Norwegian')])


class email_wizard_temp(models.TransientModel):
    _inherit = 'mail.compose.message'

    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="['&',('model', '=', model),('create_uid','=',uid)]")


    # def _cal_domain(self):
    #      template_id = self.env['mail.template'].search(['&',('create_uid','=',self.env.uid)]).id