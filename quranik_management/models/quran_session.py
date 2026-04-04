from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class QuranSession(models.Model):
    _name = 'quran.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Quran Session"

    teacher_id = fields.Many2one('res.partner', string="Teacher", domain=[('is_teacher', '=', True)], required=True)
    student_id = fields.Many2one('res.partner', string="Student", domain=[('is_student', '=', True)], required=True)
    
    start_datetime = fields.Datetime(string="Start Time", required=True, tracking=True)
    duration = fields.Float(string="Duration (Hours)", default=1.0, required=True)
    end_datetime = fields.Datetime(string="End Time", compute="_compute_end_datetime", store=True)
    
    meeting_url = fields.Char(string="Meeting Link")

    state = fields.Selection([
        ('draft', 'Scheduled'),
        ('done', 'Completed'),
        ('absent', 'Student Absent'),
        ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    progress_details = fields.Text(string="Progress Details")
    homework = fields.Text(string="Homework")
    technical_score = fields.Selection([
        ('1', 'Beginner'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Excellent')
    ], string="Technical Rating")
    moral_value_ids = fields.Many2many('quran.value', string="Moral Values")

    @api.depends('start_datetime', 'duration')
    def _compute_end_datetime(self):
        for record in self:
            if record.start_datetime:
                record.end_datetime = record.start_datetime + timedelta(hours=record.duration)
            else:
                record.end_datetime = False

    def action_complete(self):
        for record in self:
            if record.student_id.session_credits <= 0:
                raise ValidationError(_("The student has no remaining credits!"))
            record.student_id.session_credits -= 1
            record.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

class QuranReading(models.Model):
    _name = 'quran.reading'
    _description = "Quran Reading"
    name = fields.Char(string="Name", required=True)

class QuranValue(models.Model):
    _name = 'quran.value'
    _description = "Moral Value"
    name = fields.Char(string="Name", required=True)
