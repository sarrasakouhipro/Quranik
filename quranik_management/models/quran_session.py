from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import datetime 
import uuid


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
        ('in_progress', 'In Progress'),
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

    actual_start_time = fields.Datetime(string="Actual Start", readonly=True)
    actual_end_time = fields.Datetime(string="Actual End", readonly=True)
    duration_minutes = fields.Integer(string="Duration (min)", compute="_compute_duration")
    
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


    @api.model
    def create(self, vals):
        # Générer un identifiant unique pour la salle de réunion
        session_uuid = uuid.uuid4().hex[:10]
        # On utilise Jitsi pour la facilité (pas d'API payante)
        vals['meeting_url'] = f"https://meet.jit.si/Quranik_{session_uuid}"
        return super(QuranSession, self).create(vals)

    def action_send_reminder(self):
        template = self.env.ref('quranik_management.email_template_quran_session_reminder')
        for record in self:
            template.send_mail(record.id, force_send=True)


    @api.depends('actual_start_time', 'actual_end_time')
    def _compute_duration(self):
        for rec in self:
            if rec.actual_start_time and rec.actual_end_time:
                diff = rec.actual_end_time - rec.actual_start_time
                rec.duration_minutes = int(diff.total_seconds() / 60)
            else:
                rec.duration_minutes = 0

    def action_start_session(self):
        """Démarre la séance, enregistre l'heure et ouvre Jitsi"""
        self.write({
            'state': 'in_progress',
            'actual_start_time': fields.Datetime.now()
        })
        return {
            'type': 'ir.actions.act_url',
            'url': self.meeting_url,
            'target': 'new',
        }

    def action_open_close_wizard(self):
        """Ouvre la fenêtre pour noter les devoirs et terminer la séance"""
        return {
            'name': _('End Session Notes'),
            'type': 'ir.actions.act_window',
            'res_model': 'quran.session.close.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_session_id': self.id}
        }

    survey_url = fields.Char(string="Feedback Link", compute="_compute_survey_url")

    def _compute_survey_url(self):
        base_url = "https://votre-odoo.com/survey/start/votre-id-sondage"
        for rec in self:
            # On ajoute l'ID de la session en paramètre pour savoir d'où vient la réponse
            rec.survey_url = f"http://elearning.quranik.org/survey/start/462b81bf-6736-44e5-bfd1-16fb55df2426?session_id={rec.id}&student={rec.student_id.name}"

class QuranReading(models.Model):
    _name = 'quran.reading'
    _description = "Quran Reading"
    name = fields.Char(string="Name", required=True)

class QuranValue(models.Model):
    _name = 'quran.value'
    _description = "Moral Value"
    name = fields.Char(string="Name", required=True)
