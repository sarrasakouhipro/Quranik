from odoo import models, fields, api

class QuranSession(models.Model):
    _name = 'quran.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Quran Session"

    teacher_id = fields.Many2one('res.partner', string="Teacher", domain=[('is_teacher', '=', True)])
    student_id = fields.Many2one('res.partner', string="Student", domain=[('is_student', '=', True)])
    
    start_datetime = fields.Datetime(string="Start Time", required=True)
    duration = fields.Float(string="Duration (Hours)", default=1.0)
    meeting_url = fields.Char(string="Meeting Link")

    state = fields.Selection([
        ('draft', 'Scheduled'),
        ('done', 'Completed'),
        ('absent', 'Student Absent'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)
    
    progress_details = fields.Text(string="Progress (Surah/Ayat)", translate=True)
    technical_score = fields.Selection([
        ('1', 'Beginner'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Excellent')
    ], string="Technical Rating")
    
    moral_value_ids = fields.Many2many('quran.value', string="Moral Values Focus")
    homework = fields.Text(string="Next Homework", translate=True)

# N'oubliez pas d'ajouter ces classes aussi si elles sont dans le même fichier
class QuranReading(models.Model):
    _name = 'quran.reading'
    _description = "Quran Reading"
    name = fields.Char(string="Name", required=True, translate=True)

class QuranValue(models.Model):
    _name = 'quran.value'
    _description = "Moral Value"
    name = fields.Char(string="Name", required=True, translate=True)
