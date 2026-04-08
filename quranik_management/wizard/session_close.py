from odoo import models, fields, api

class QuranSessionCloseWizard(models.TransientModel):
    _name = 'quran.session.close.wizard'
    _description = 'Wizard to close session'

    session_id = fields.Many2one('quran.session', string="Session")
    progress_notes = fields.Text(string="Progress Details", required=True)
    homework = fields.Text(string="Next Homework", required=True)
    technical_score = fields.Selection([
        ('1', 'Beginner'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Excellent')
    ], string="Student Performance", required=True)

    def action_confirm_close(self):
        session = self.session_id
        session.write({
            'progress_details': self.progress_notes,
            'homework': self.homework,
            'technical_score': self.technical_score,
            'actual_end_time': fields.Datetime.now(),
            'state': 'done'
        })

        # LOGIQUE DE CRÉDIT
        if session.is_trial:
            # C'est un essai : on ne déduit rien, on marque juste l'élève
            session.student_id.has_had_trial = True
        else:
            # Séance normale : on déduit 1 crédit
            if session.student_id.session_credits > 0:
                session.student_id.session_credits -= 1
            else:
                # Optionnel : envoyer une alerte si l'élève n'a plus de crédit
                pass
        
        # Envoyer l'email automatique avec le lien vers le Survey
        template = self.env.ref('quranik_management.email_template_session_report')
        template.send_mail(self.session_id.id, force_send=True)
