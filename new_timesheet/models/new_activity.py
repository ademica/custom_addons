from odoo import fields,models

class newActivity(models.Model):
    _name = "new_timesheet.activity"
    _description = "Activities from eSolver"

    code = fields.Char(required = True)
    description = fields.Text(required = True)