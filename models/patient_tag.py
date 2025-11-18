# Patient's data come here
from odoo import api, fields, models

class PatientTag(models.Model): #Creating new class by models.Model
    _name = 'patient.tag'
    _description = 'Patient Tag'
    _order = 'sequence, id'

    # adding new field in the patient.tag (Patient Tag) object Model
    name = fields.Char(
         string='Patient Name', required=True,
    )

    sequence = fields.Integer(default=10)