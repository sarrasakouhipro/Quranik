from odoo import models, fields, api, _, SUPERUSER_ID


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    stop_all_bookings = fields.Boolean(
        string="Stop Receiving Appointment Bookings",
        config_parameter='thoo8.appointment.request.stop_all_bookings',
        help="If enabled, no new appointment bookings will be accepted."
    )
    stop_when_reached = fields.Boolean(
        string="Stop Accepting Appointments When Maximum Reached",
        config_parameter='thoo8.appointment.request.stop_when_reached',
        help="If enabled, bookings will stop once the allowed number is reached."
    )
    max_daily_bookings = fields.Integer(
        string="Maximum Daily Bookings",
        config_parameter='thoo8.appointment.request.max_daily_bookings',
        default=50,
        help="The allowed number of daily bookings through the portal."
    )
    enable_mobile_verification = fields.Boolean(
        string="Enable Mobile Verification",
        config_parameter='thoo8.appointment.request.enable_mobile_verification',
        help="If enabled, customers must verify their mobile number before booking an appointment."
    )
    enable_id_card_verification = fields.Boolean(
        string="Enable ID Card Verification",
        config_parameter='thoo8.appointment.request.enable_id_card_verification',
        help="If enabled, the system will enforce ID card verification during the appointment booking."
    )

    def set_default_config(cr, registry):
        env = api.Environment(cr, SUPERUSER_ID, {})
        params = env['ir.config_parameter'].sudo()

        if not params.get_param('thoo8.appointment.request.enable_id_card_verification'):
            params.set_param('thoo8.appointment.request.enable_id_card_verification', True)

