import openerp
from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


#===============================SCIENTIFIC INSTITUTION CLASS=============================

class scientific_institution(osv.osv):

	_name = 'scientific.institution'

	_description = 'scientific institution model'

	_rec_name = 'inst_name'

	_columns = {

			'inst_name' : fields.many2one(
					'institution.name',
					'Institution Name',
					onupdate='cascade',
					required=True,
				),

			'study_years' : fields.selection(
				[(3, '3'), (4, '4'), (5, '5'), (7, '7')],
				'Study Years',
				required=True,
				),

			'department' : fields.many2one(
					'institution.department',
					'Department',
					onupdate='cascade',
					required=True,
				),

			'qual_degree' : fields.many2one(
					'institution.qualification',
					'Qualification',
					onupdate='cascade',
					required=True,
				),

		}

	_sql_constraints = [('rec_uniq','unique(inst_name,study_years,department,qual_degree)', 'Institution With The Same Data Already Exist!')]

#==========================================================================================

#============================ INSTITUTION NAME CLASS==================================

class institution_name(osv.osv):
	_name = 'institution.name'

	_rec_name = 'inst_name'

	_description = 'institution name model'
	
	_columns = {

			'inst_name' : fields.char(
				'Institution Name',
				size=200,
				required=True,
				),
		}

	_defaults = {
			'inst_name' : '',
		}

	_sql_constraints = [('inst_uniq','unique(inst_name)', 'Institution With The Same Name Already Exist!')]

#==========================================================================

#======================== INSTITUTION DEPARTMENT CLASS=====================

class institution_department(osv.osv):

	_name = 'institution.department'

	_description = 'scientific institution departments model'

	_rec_name = 'dep_name'

	_order = 'dep_name asc'

	_columns = {
			
			'dep_name' : fields.char(
					'Department',
					size=60,
					required=True,
				),

		}

	_defaults = {
			'dep_name' : '',
		}

	_sql_constraints = [('dep_uniq','unique(dep_name)', 'Department With The Same Name Already Exist!')]


#======================================================================================

#============================ INSTITUTION QUALIFICATIONS CLASS=========================

class institution_qualification(osv.osv):

	_name = 'institution.qualification'

	_description = 'scientific institution degrees model'

	_rec_name = 'qual_degree'

	_order = 'qual_degree asc'

	_columns = {

			'qual_degree' : fields.char(
					'Qualification',
					size=60,
					required=True,
				),

		}

	_defaults = {
			'qual_degree' : '',
		}

	_sql_constraints = [('qual_uniq','unique(qual_degree)', 'Qualification With The Same Name Already Exist!')]


#======================================================================================


class hr_employee(osv.osv):
	_name = "hr.employee"
	_inherit = "hr.employee"

	_description = "This Model Extends Employee Directory To Adds Employee Qualification"

	_columns = {

			'employee_qualification': fields.many2one(
					'scientific.institution',
					'Employee Qualification',
				),
		}

hr_employee()