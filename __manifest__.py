# Define a Dictionary
{
    'name': 'Hospital Management System',
    'author': 'Thamindu Rajakaruna',
    'license': 'LGPL-3',
    'version': '17.0.1.1',
    'depends': [
        'mail',
        'product' # Unknown co-model product.product in patient.py so we have to add one dependency in order to solve the error
                    # product.product model is coming from the product module in Odoo
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/patient_views.xml',
        'views/patient_readonly_views.xml',
        'views/appointment_views.xml',
        'views/appointment_line_views.xml',
        'views/patient_tag_views.xml',
        'views/menu.xml'
    ]
}