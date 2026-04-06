from odoo import models, fields

class QuranProgram(models.Model):
    _name = 'quran.program'
    _description = "Quran Program"

    name = fields.Char(string="Program Name", required=True)
    audience = fields.Selection([
        ('kids', 'Children'),
        ('teens', 'Teenagers'),
        ('adults', 'Adults')
    ], string="Audience", required=True)
    
    sessions_per_week = fields.Integer(string="Sessions / Week", default=1)
    duration = fields.Float(string="Session Duration (Hours)", default=1.0)
    price = fields.Float(string="Monthly Price")
    active = fields.Boolean(default=True)
