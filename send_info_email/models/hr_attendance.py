from odoo import models, api, fields
from  odoo.exceptions import UserError

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model_create_multi
    def create(self, vals_list):
        attendances = super().create(vals_list)
        attendances._send_attendance_email('created')
        return attendances

    def write(self, vals):
        res = super().write(vals)

        if 'check_in' in vals or 'check_out' in vals:
            self._send_attendance_email('edited')
        return res
    
    def unlink(self):
        self._send_attendance_email('deleted')
        res = super().unlink()
        return res

    def _send_attendance_email(self, action):

        for record in self:
            
            if record.employee_id.receive_email and record.check_in or record.check_out:
                if action == 'created':
                    template = self.env.ref('send_info_email.attendance_email_template_create')

                elif action == 'edited':
                    template = self.env.ref('send_info_email.attendance_email_template_write')

                elif action == 'deleted': 
                    template = self.env.ref('send_info_email.attendance_email_template_unlink')
                
                else: continue

                if template:

                    check_in_str = fields.Datetime.context_timestamp(record, record.check_in).strftime("%d/%m/%Y %H:%M:%S") if record.check_in else ''
                    check_out_str = fields.Datetime.context_timestamp(record, record.check_out).strftime("%d/%m/%Y %H:%M:%S") if record.check_out else ''

                    template.with_context({
                        'check_in_str': check_in_str,
                        'check_out_str': check_out_str,
                    }).send_mail(record.id, force_send=True)