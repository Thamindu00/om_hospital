# Patient's data come here
from odoo import api, fields, models

class HospitalAppointment(models.Model): #Creating new class by models.Model
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference', 'patient_id'] # have to search reference field, and have to search on patient_id.
                                            # Saying need to search based on the patient name as well as the reference value.
                                            # we can add what we want to search as a list in many to one field.
    _rec_name = 'patient_id' # Show the rec name of the model as the value from patient id field

    reference = fields.Char(string="Reference", default='New')
    # We need a lookup view, so we create a many-to-one field in odoo - we can see list of patients, newly changed required to
    # true and ondelete to restrict to avoid the data vanish when do the patient deletion if there is use of them in appointments
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, ondelete='restrict')

    # on delete `cascade` for delete the related appointments too when deletion of the patient
    # patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, ondelete='cascade')

    # default is ondelete = 'set null' and when use of the set null we cannot put the required as True
    # if delete the patient, the patient_id field in the appointment will be empty
    # patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, ondelete='set null')
    date_appointment = fields.Date(string="Appointment Date")
    note = fields.Text(string="Note")
    state = fields.Selection([
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'),
        ('done', 'Done'), ('cancel', 'Cancelled')
    ], default='draft', tracking=True)
    appointment_line_ids = fields.One2many(
        'hospital.appointment.line', 'appointment_id', string="Lines"
    )
    # added new total_qty db field to the hospital_appointment db table, actually non stored computed field,
    # there are 2 types of computed fields, 1] stored in the database. 2] not stored in the db, but it will
        # compute on the fly whenever we load it, it will compute.
    # But we can make this to stored in the database by adding `store=True` and put the dependency
    total_qty = fields.Float(
        compute='_compute_total_qty', string="Total Quantity", store=True
    )
    # below is non-stored related field, in that no need to put string attribute again, to store we have to add store=True
    # date_of_birth = fields.Date(string="DOB", related='patient_id.date_of_birth')
    date_of_birth = fields.Date(related='patient_id.date_of_birth', store=True,
                                groups="om_hospital.group_hospital_doctors"
    )

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

    # based on the one-to-many line and quantity field in the one-to-many line, we have to recompute the function
    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    # newly added function for calculate the `total quantity`
    def _compute_total_qty(self):
        for rec in self:
            # total_qty = 0
            # print(rec.appointment_line_ids)
            # below code line will print rec appointment lines id num
            # So we have to do the iteration over a for loop
            # for line in rec.appointment_line_ids:
                # print("line value", line.qty)
                # total_qty = total_qty + line.qty
                # total_qty += line.qty
            # rec.total_qty = total_qty

    #       The same thing that we have done above by the code block which start from `total_qty = 0` to `rec.total_qty = total_qty`
    #       we can implement that in other way using mapped method, just single code line
    # ********************* SPECIAL ****************************************************
            print(rec.appointment_line_ids.mapped('qty'))
            rec.total_qty = sum(rec.appointment_line_ids.mapped('qty'))
    #************************************************************************************

    def _compute_display_name(self):
        for rec in self:
            print("values are: ", f"[{rec.reference}] {rec.patient_id.name}")
            rec.display_name = f"[{rec.reference}] {rec.patient_id.name}"

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

class HospitalAppointmentLine(models.Model): #Creating new class by models.Model
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    # first the main field inside one to many, we have to create many to one field to the parent model
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    qty = fields.Float(string="Quantity")

