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

    # --- Constraints ---
    @api.constrains('teacher_id', 'start_datetime', 'duration')
    def _check_teacher_overlap(self):
        for record in self:
            # Search for sessions for the same teacher that overlap the current time range
            overlap = self.search([
                ('id', '!=', record.id),
                ('teacher_id', '=', record.teacher_id.id),
                ('state', '!=', 'cancel'),
                ('start_datetime', '<', record.end_datetime),
                ('end_datetime', '>', record.start_datetime),
            ])
            if overlap:
                raise ValidationError(_("This teacher already has a session scheduled during this time!"))

    # --- Compute Fields ---
    @api.depends('start_datetime', 'duration')
    def _compute_end_datetime(self):
        for record in self:
            if record.start_datetime:
                record.end_datetime = record.start_datetime + timedelta(hours=record.duration)
            else:
                record.end_datetime = False

    # --- Actions ---
    def action_complete(self):
        for record in self:
            if record.student_id.session_credits <= 0:
                raise ValidationError(_("The student has no remaining credits to complete this session!"))
            
            # Deduct 1 credit
            record.student_id.session_credits -= 1
            record.write({'state': 'done'})
            
    def action_cancel(self):
        self.write({'state': 'cancel'})
