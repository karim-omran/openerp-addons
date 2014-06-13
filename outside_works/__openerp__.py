{
	'name' : 'Outside Work',
	'version' : '0.1',
	'author' : 'Karim Omran',
	'category' : 'Human Resources',
	'sequence' : 1,
	'description': """
This Module Allows User To Easily Define New Outside Works.
=======================================================================================

This Module Allows User To Define New Outside Works.""",

	'depends' : ['base','hr_contract'],
	'data' : [
		'view/outside_works_view.xml',
		'view/report_view.xml',
		'wizard/hr_attendance_bymonth_view.xml',
	],

	'installable' : True,

}
