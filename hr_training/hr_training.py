import time
from datetime import *
from openerp.osv import fields, osv
from openerp.tools.translate import _


class hr_training_course(osv.osv):

	_name = "hr.training.course"
	_description = "Register Training Course"
	_columns = {

		'name': fields.char('Course name', required=True),
		'category': fields.char('Category', size=100),
		'from_date': fields.date('From', required=True),
		'to_date': fields.date('To', required=True),
		'attachments': fields.one2many('ir.attachment', 'res_id', 'Attachments'),

		'notes': fields.text('Notes'),
	}

	_defaults = {

		'category': 'miscellaneous',
	
	}

	_sql_constraints = [('course_unique_name_date','unique(name,from_date,to_date)','The same course with the same start and end dates exists')]



	def _check_unique_insenstive(self, cr, uid, ids, context=None):
		
		""" check case insensitive uniqueness of the record
		in terms of course name """

		all_ids = self.search(cr, uid, [], context=context)

		record = self.browse(cr, uid, ids, context=context)

		all_ids.remove(record[0].id)

		for obj in self.browse(cr, uid, all_ids, context=context):

			if obj.name.lower() == record[0].name.lower() and obj.from_date == record[0].from_date:
				
				return False
		return True
					




	def _check_date(self, cr, uid, ids, context=None):
	
		""" check if dates are before current date and
		that the end date of the course is after the begining
		date """

		record = self.browse(cr, uid, ids, context=context)

		from_date = datetime.strptime(record[0].from_date,"%Y-%m-%d")
		to_date = datetime.strptime(record[0].to_date,"%Y-%m-%d")

		if from_date >= datetime.today() and to_date > from_date:
			return True
		else:
			return False



	
	def name_get(self, cr, uid, ids, context=None):
	
		res = []
			
		if context is None:
			context = {}

		if not ids:
			return []
		aux = ''

		for obj in self.browse(cr,uid,ids,context=context):

			if obj.name:
				
				aux = obj.name
			else:

				aux = obj.id
			aux = aux + ' ('

			if obj.from_date:

				aux = aux + obj.from_date

			aux = aux + " - "

			if obj.to_date:

				aux = aux + obj.to_date

			aux += ')'

			res.append((obj.id, aux))
	

		return res









	_constraints = [
		(_check_unique_insenstive, 'Course name and dates must be unique', ['name','from_date','to_date']),
		(_check_date, 'Incorrect Date Values', ['from_date','to_date'])
	]



	_order = 'from_date asc'


class register_employee(osv.osv):

	_name = "hr.training.register"
	_description = "Register Employees for Training Courses"
	_columns = {

		'employee': fields.many2one("hr.employee", "Employee", required=True, select=True),
		'course': fields.many2one("hr.training.course", "Course", required=True),
	
	}

	_sql_constraints = [('unique_reg', 'unique(employee,course)' , "Employee Already assigned to Course")]

	_order = "course asc"

	
	def name_get(self, cr, uid, ids, context=None):
	
		res = []
			
		if context is None:
			context = {}

		if not ids:
			return []
		aux = ''

		for obj in self.browse(cr,uid,ids,context=context):

			if obj.employee:
				
				aux = obj.employee.name
			else:

				aux = obj.id
			aux = aux + ' ('

			if obj.course:

				aux = aux + obj.course.name

			aux = aux + " - "


			res.append((obj.id, aux))
	

		return res

class hr_employee(osv.osv):

	_name = "hr.employee"
	_inherit = "hr.employee"
	_columns = {

		'training_id': fields.one2many('hr.training.register', 'employee', 'Training', help="These are the training courses the employee had."),
	
	}

hr_employee()

