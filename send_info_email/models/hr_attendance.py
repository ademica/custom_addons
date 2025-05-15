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
                    template.send_mail(record.id, force_send=True)



            #print("test mail sent")
            #template = self.env.ref('send_info_email.attendance_email_template')
            #template.send_email(record, )
            #self.env['email_template'].search()
            #pass

            # 1) 3 cases of different templates
        
            # employee = record.employee_id
            # email = employee.work_email 
            # current_user = self.env.user.name

            # if record.check_in: 
            #     check_in_local = fields.Datetime.context_timestamp(record, record.check_in)
            #     formatted_check_in = check_in_local.strftime("%d/%m/%Y %H:%M:%S") 

            # if record.check_out:
            #     check_out_local = fields.Datetime.context_timestamp(record, record.check_out)
            #     formatted_check_out = check_out_local.strftime("%d/%m/%Y %H:%M:%S")

                
            # if employee.receive_email:

            #     subject = f"Attendance {action.capitalize()} Notification"
            #     message = f"""
            #     <p>Hello {employee.name},</p>
                    
            #     <p>Your attendance record with the following data:</p> 
                
            #     <ul>
            #     {f"<li>Checked in at {formatted_check_in}</li>" if record.check_in else ""}
            #     {f"<li>Checked out at {formatted_check_out}</li>" if record.check_out else ""}
            #     </ul>

            #     <p>has been <strong>{action}</strong> by {current_user}</p>
                    
            #     <p>Regards,
            #     <br>HR Team</p>
            #     """

            #     mail_values = {
            #         'subject': subject,
            #         'body_html': f'<p>{message}</p>',
            #         'email_to': email,
            #         'email_from': 'adema.sarajlija@gmail.com'
            #     }
            #     self.env['mail.mail'].create(mail_values).send()