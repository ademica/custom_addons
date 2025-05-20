from odoo import fields,models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    activity_id = fields.Many2one('new_timesheet.activity', string='Activity', required=True)
    service_id = fields.Many2one('new_timesheet.service', string='Service', required=True)
