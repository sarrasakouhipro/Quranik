from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Roles
    is_teacher = fields.Boolean(string="Is Teacher", help="Check if this contact is a Quran teacher")
    is_student = fields.Boolean(string="Is Student", help="Check if this contact is a student")

    # Teacher Specifics
    is_english_speaker = fields.Boolean(string="English Speaker")
    quran_reading_ids = fields.Many2many('quran.reading', string="Mastered Readings")
    teacher_bio = fields.Html(string="Teacher Biography", translate=True)

    # Economics
    commission_rate = fields.Float(string="Commission Rate (%)", default=60.0)
    wallet_balance = fields.Float(string="Wallet Balance", readonly=True)

    # Subscription Credits
    session_credits = fields.Integer(string="Remaining Session Credits", default=0)

    # Ce champ permet de lier le prof à son compte de connexion
    user_id = fields.Many2one('res.users', string="Related User", help="The Odoo user account for this teacher")

    program_id = fields.Many2one('quran.program', string="Current Program")
    audience_type = fields.Selection(related='program_id.audience', store=True)
    
    # Pour la séance d'essai
    has_had_trial = fields.Boolean(string="Had Trial Session", default=False)
