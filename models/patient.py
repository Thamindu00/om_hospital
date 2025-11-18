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
    # In many to many we have to use the `s` for the field name
    # This is how to define the many to many field
    tag_ids = fields.Many2many( # remember the Many2many is case-sensitive
        #'patient.tag','patient_tag_rel','patient_id','tag_id',string="Tags" # patient_tag_rel is the relation name
        'patient.tag', string="Tags"
    )
