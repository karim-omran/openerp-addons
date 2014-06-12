{
	'name' : 'Personal Information Extension',
	'version' : '0.1',
	'category' : 'Human Resources',
	'sequence' : 1,
	'description': """
This Module Allows User To Extend Personal Information Of Employees.
====================================================================

This Module Allows User To Extend Employees Personal Information Like Nationality And Marital State.""",
    
    'depends' : ['hr',],
	'data' : [
		'view/personal_inf_ext_view.xml',
	],

	'installable' : True,
}
