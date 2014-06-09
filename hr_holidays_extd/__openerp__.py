{

	'name': 'Leaves Extension',
	'version': '1.0',
	'categroy': 'Human Resources',
	'description': """
This module is an extension of the Leaves module.
==================================================

Allows for group allocation of leaves to employees with pre-defined leave types set with default allocation of days.
			""",
	'author': 'ITI Dev Team',
	'depends': ['base','hr','hr_holidays'],
	'data': [

		'hr_holidays_extd_view.xml',
		
		],
	'installable': True,
	'auto_install': False,
	'sequence': 1,

}
