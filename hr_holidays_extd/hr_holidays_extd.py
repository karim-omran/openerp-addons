import datetime
import time
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _



class motherhood_leaves(osv.osv):

	_name = 'motherhood.leaves'

	_description = 'motherhood leaves model'

	_rec_name = 'child_order'

	_columns = {

			'child_order' : fields.integer(
					'Child Order',
					required=True,
				),

			'leave_balance' : fields.integer(
					'Leave Balance',
					required=True,
				),

		}


	_sql_constraints = [('leave_uniq','unique(child_order, leave_balance)', 'Motherhood Leave With The Same Data Already Exist!')]


	def _check_fields(self, cr, uid, ids, context=None):
		records = self.browse(cr, uid, ids, context=context)
		for rec in records:
			if rec.child_order <= 0 or rec.leave_balance <= 0:
				return False
			else:
				return True

	_constraints = [(_check_fields, 'Error : Fiels Must Be Positive Number Higher Than 0!', ['child_order', 'leave_balance']),]





class pilgrimage_leaves(osv.osv):

	_name = 'pilgrimage.leaves'

	_description = 'pilgrimage leaves model'

	_rec_name = 'religion'

	_columns = {

			'religion' : fields.selection(
				[('muslim', 'Muslim'), ('cristian', 'Cristian'),],
				'Religion',
				required=True,
				),

			'leave_balance' : fields.integer(
					'Leave Balance',
					required=True,
				),

		}

	_sql_constraints = [('religion_uniq','unique(religion)', ' Pilgrimage Leaves With The Same Data Already Exist!')]


	def _check_fields(self, cr, uid, ids, context=None):
		records = self.browse(cr, uid, ids, context=context)
		for rec in records:
			if rec.leave_balance <=0:
				return False
			else:
				return True


	_constraints = [(_check_fields, 'Error : Leave Balance Be Positive Number And Less Than 100!', ['leave_balance']),]








class leaves_service_time(osv.osv):

	_name = "leaves.service.time"
	_description = "leaves structure according to years of service"
	_columns = {

		'from': fields.integer('Years of service',required=True),
		'to': fields.integer('To',required=True),
		'allocation': fields.integer('Allocated leave',required=True),
		
		}

	_sql_constraints=[('unique_record','unique(from,to)','Service years records already there')]






class hr_holidays_status(osv.osv):

	_name = "hr.holidays.status"
	_description = "default allocation for leave types"
	_inherit = "hr.holidays.status"
	
	_columns = {

		'default_allocation': fields.integer('Allocation'),
		'transfer_allocation': fields.boolean('Transfer overflow', help='Allows you to transfer last years remaining holidays for this years'),

		'allocation_type': fields.selection([('normal','normal'),('religion','religion'),('years_service','years_service')],"Allocation based on",required=True),

	}

#remember to put constraints on allocation types

hr_holidays_status()
