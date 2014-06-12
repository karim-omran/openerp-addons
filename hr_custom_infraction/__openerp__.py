{
    'name': 'ISFP Infraction Management',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
Warning/Disciplinary Action Management
========================================
    """,
    'depends': [
        'hr',
        'hr_employee_state',
        'hr_security',
        'hr_transfer',
        'hr_infraction'
    ],
    'data': [
        'hr_custom_infraction_view.xml',
        'report/report_view.xml',
        'wizard/action_report_wizard.xml',
    ],
    'installable': True,
    'active': False,
}
