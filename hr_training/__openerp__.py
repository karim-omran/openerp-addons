{

	'name': 'Training',
	'version': '1.0',
	'category': 'Human Resources',
	'description': """
This module is for managing Training in a Company.
===================================================

Registers new training courses and their details , registers employees to these
courses and keeps track of both.
	               """,
	'author': 'ITI Dev Team',
	'depends': ['hr','knowledge'],
	'data': [
		
		'hr_training_view.xml',
		'hr_training_report.xml',
		'wizard/course_search.xml',

	],
	'installable': True,
	'auto_install': False,

}
