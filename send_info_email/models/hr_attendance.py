from odoo import models, api, fields

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    @api.model_create_multi
    def create(self, vals):
        attendance = super().create(vals)
        attendance.send_attendance_email('created')
        return attendance

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            if 'check_in' in vals or 'check_out' in vals:
                record.send_attendance_email('edited')
        return res
    
    def unlink(self):
        self.send_attendance_email('deleted')
        res = super().unlink()
        return res

    def send_attendance_email(self, action):

        for record in self: 
        
            employee = record.employee_id
            email = employee.work_email 
            current_user = self.env.user.name

            if record.check_in: 
                check_in_local = fields.Datetime.context_timestamp(record, record.check_in)
                formatted_check_in = check_in_local.strftime("%d/%m/%Y %H:%M:%S") 
            else: None

            if record.check_out:
                check_out_local = fields.Datetime.context_timestamp(record, record.check_out)
                formatted_check_out = check_out_local.strftime("%d/%m/%Y %H:%M:%S")
            else: None

                
            if employee.receive_email:

                subject = f"Attendance {action.capitalize()} Notification"
                message = f"""
                <p>Hello {employee.name},</p>
                    
                <p>Your attendance record with the following data:</p> 
                
                <ul>
                {f"<li>Checked in at {formatted_check_in}</li>" if record.check_in else ""}
                {f"<li>Checked out at {formatted_check_out}</li>" if record.check_out else ""}
                </ul>

                <p>has been <strong>{action}</strong> by {current_user}</p>
                    
                <p>Regards,
                <br>HR Team</p>
                """

                mail_values = {
                    'subject': subject,
                    'body_html': f'<p>{message}</p>',
                    'email_to': email,
                    'auto_delete': True,
                    'email_from': 'adema.sarajlija@gmail.com'
                }
                self.env['mail.mail'].create(mail_values).send()