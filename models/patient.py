# Patient's data come here
from odoo import api, fields, models

class HospitalPatient(models.Model): #Creating new class by models.Model
    _name = 'hospital.patient'
    _description = 'Patient Master'

    # adding new field in the hospital.patient (Patient Master) object Model
    name = fields.Char(string='Patient Name', required=True)
    date_of_birth = fields.Date(string='DOB')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')