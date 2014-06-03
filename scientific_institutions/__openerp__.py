{
	'name' : 'Scientific Institutions',
	'sequence' : 1,
	'version' : '0.1',
	'category' : 'Human Resources',

	'description': """
This Module Allows User To Easily Define New Scientific Institution.
=======================================================================================

This Module Allows User To Define New Scientific Institution And Related Date Such as Study Years, Departments And Qualifications Given.""",
    
    'depends' : ['hr',],
	'data' : [
		'view/scientific_institution_view.xml',
		'workflow/scientific_institution_workflow.xml',
	],

	'installable' : True,
}