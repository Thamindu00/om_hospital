# Patient's data come here
from odoo import api, fields, models

class HospitalAppointment(models.Model): #Creating new class by models.Model
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_name = 'patient_id' # Show the rec name of the model as the value from patient id field

    reference = fields.Char(string="Reference", default='New')
    # We need a lookup view, so we create a many-to-one field in odoo - we can see list of patients
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    date_appointment = fields.Date(string="Date")
    note = fields.Text(string="Note")
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'),
        ('done', 'Done'), ('cancel', 'Cancelled')
    ], default='draft', tracking=True)

    @api.model_create_multi
    # Added below new 2 lines of code
    # This process is called as inheriting or by supering the create method, by default when we hit on the new Appointments button
    # and clicking the save, the create method of odoo getting executed. The create method is inherited from the `models.Model`
    # What the below create method do is that based on the entered value on the form it will create a record inside the Postgre table
    # So the all the values will be received inside this method
    def create(self, vals_list):
        print("odoo mates", vals_list)
        # Iterating first of all elements of the dictionary can hold the multiple values for the creation multiple records at
        # the same time not directly from the UI but from the code side can create multiple values.
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                # Inside the ir.sequence model have a function to that can pass a code and it will return the next value from the sequence.
                # Assign that value to the reference field. Then that value pass to the odoo method & it will create a sequence value
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') # Need next sequential value of this sequence
        return super().create(vals_list)

    # In ORM self is looking for the current record set, so can assume self will be giving the current record
    def action_confirm(self):
        for rec in self:
            # Inside rec we have record set, then by using the dot operator writing value to the `state` field
            # Here assigning value to that field
            rec.state = 'confirmed'

            # Print as "Button is clicked hospital.appointment(10,) hospital.appointment(10,)"
            # print("Button is clicked", self, rec)

            # Print as "Reference is... HP00004"
            # print("Reference is...", self.reference)

            # Same as above we can access the other fields data too
            # print("Note: ", self.note)

    def action_ongoing(self):
        for rec in self:
            rec.state = 'ongoing'
    def action_done(self):
        for rec in self:
            rec.state = 'done'
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

