from odoo import fields,models

class newActivity(models.Model):
    _name = "new_timesheet.activity"
    _description = "Activities from eSolver"

    short_code = fields.Char(required = True)
    description = fields.Text(required = True)

    _rec_name = "description"

    _sql_constraints = [
        ('unique_short_code', 'unique(short_code)', 'The short code must be unique.')
    ]