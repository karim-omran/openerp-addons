from openerp.osv import osv, fields
from openerp.tools.translate import _
from datetime import *

class outside_works(osv.osv):
	_name = 'outside.works'

	_description = 'outside works model'

	_rec_name = 'type'

	_columns = {
			'type' : fields.char(
				'Outside Work Type',
				size=100,
				required=True,
				),
		}

	_sql_constraints = [('type_unique', 'unique(type)', 'Outside Work With The Same Type Already Exists!')]

	_order = 'type asc'



class outside_work_forms(osv.osv):
	_name = 'outside.works.forms'

	_description = 'outside works forms model'

	_rec_name = 'outside_work_type'

	_columns = {

			'employee' : fields.many2one(
				'hr.employee',
				'Employee',
				ondelete='cascade',
				onupdate='cascade',
				required=True,
				),
			
			'outside_work_type' : fields.many2one(
				'outside.works',
				'Outside Work Type',
				ondelete='cascade',
				onupdate='cascade',
				required=True,
				),

			'start_date' : fields.date(
				'Start Date',
				required=True,
				),

			'end_date' : fields.date(
				'End Date',
				required=True,
				),

			'notes' : fields.text(
				'Notes',
				),

		}

	_order = 'employee asc'


	def _check_dates(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		for data in record:
			if data.end_date < data.start_date:
				return False
			else:
				return True

	_constraints = [(_check_dates, 'Error : Start Date Must Be After End Date!', ['start_date', 'end_date',]),]
