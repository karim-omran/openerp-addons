from osv import osv, fields
from tools.translate import _

class emp_disabilities(osv.osv):

	_name = "emp.disabilities"

	_rec_name = "disability_type"

	_columns = {
			'disability_type': fields.char(
				'Disbility Type',
				required=True,
				),
			
			'notes': fields.text(
				'Disability Notes'
				),
		}

	_sql_constraints = [('type_unique', 'unique(disability_type)', 'Disability With The Same Type Already Exists!')]

class hr_employee(osv.osv):
	_name = "hr.employee"
	_inherit = "hr.employee"

	_columns = {
			"disability_type" : fields.many2one(
					'emp.disabilities',
					'Disability Type'
				),
		}

hr_employee()
