from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time


class job_categories(osv.osv):
	_name = 'job.categories'

	_description = 'job Category'

	_rec_name = 'job_category'

	_columns = {

			'job_category' : fields.char(
				'Category Name',
				size=100,
				required=True,
				),
			
			'lower_limit' : fields.float(
				'Lower Salary Limit',
				digits=(12,2),
				required=True,
				),
			
			'upper_limit' : fields.float(
				'Upper Salary Limit',
				digits=(12,2),
				required=True,
				),

			'upper_category' : fields.many2one(
				'job.categories',
				'Upper Category',
				ondelete='set null',
				onupdate='cascade',
				),
		}

	_sql_constraints = [('job_uniq','unique(job_category)', 'Job Category With The Same Name Already Exist!')]

	_order = 'job_category asc'


	def _check_limit(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		for data in record:
			if data.lower_limit < 0 or data.upper_limit < 0 :
				return False
			else:
				return True

	_constraints = [(_check_limit, 'Error : Lower And Upper Limit Must Be Positive!', ['lower_limit', 'upper_limit',]),]


class hr_contract(osv.osv):
	_name = "hr.contract"
	_inherit = "hr.contract"
	
	_columns = {

			"emp_job_category" : fields.many2one('job.categories', 'Job Category'),

		}

hr_contract()
