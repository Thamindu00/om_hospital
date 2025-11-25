# Patient's data come here

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class HospitalPatient(models.Model): #Creating new class by models.Model
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    # adding new field in the hospital.patient (Patient Master) object Model
    name = fields.Char(
        string='Patient Name', required=True, tracking=True
    )
    date_of_birth = fields.Date(string='DOB', tracking=True) #making tracking true for the display the changes in the chatter
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender', tracking=True
    )
    # In many to many we have to use the `s` for the field name
    # This is how to define the many to many field
    tag_ids = fields.Many2many( # remember the Many2many is case-sensitive
        #'patient.tag','patient_tag_rel','patient_id','tag_id',string="Tags" # patient_tag_rel is the relation name
        'patient.tag', string="Tags"
    )

    # Inheriting the delete method which is called as unlink method - super the unlink method
    # we can do the below logic in same way by using another way that is API ondelete decorator
    '''
    def unlink(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_("You cannot delete the patient now.\nAppointments existing for this patient: %s" % rec.name))
                # raise UserError(_("You cannot delete the patient now.\nAppointments existing for this patient: %s" % rec.name))
        # we can perform anything here
        return super().unlink()
    '''

    # ondelete decorator in odoo. if any function is defined using this decorator, the function will be executed on deleting the record
    @api.ondelete(at_uninstall=False)
    def _check_patient_appointments(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_("You cannot delete the patient right now." 
                                        "\nAppointments existing for this patient: %s" % rec.name))