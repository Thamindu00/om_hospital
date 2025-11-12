# Patient's data come here
from odoo import api, fields, models

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
