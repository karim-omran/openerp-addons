{
	'name' : 'Allowances employee Info',
	'version' : '0.1',

	'description': """
This Module Allows User To Easily Define Table Sheet.
=======================================================================================

This Module Allows User To Define table sheet""",
    
    'depends' : [
    		'hr_contract',
    		'report_webkit',
    		],
	'data' : ['view/employee_contract_view.xml',

	],

	'installable' : True,
}
