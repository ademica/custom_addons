from odoo import fields,models

class newService(models.Model):
    _name = "new_timesheet.service"
    _description = "Services from eSolver"

    code = fields.Char(required = True)
    description = fields.Text(required = True)