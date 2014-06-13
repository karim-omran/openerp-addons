{
	'name' : 'Job Categories',
	'version' : '0.1',
	'category' : 'Human Resources',
	'sequence' : 1,
	'description': """
This Module Allows User To Easily Define New Jop Category.
=======================================================================================

This Module Allows User To Define New Jop Category And Its Upper And Lower Salary Limit And Upper Jop Gategory.""",
    
    'depends' : ['hr_contract',],
	'data' : [
		'view/job_categories_view.xml',
		'view/report_view.xml',
		'workflow/job_categories_workflow.xml',
		'wizard/job_cat_byname.xml',
	],

	'installable' : True,
}
