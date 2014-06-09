from datetime import datetime
import time
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _



class hr_employee(osv.osv):

	_name = "hr.employee"

	_description = "Adding leaves specific details"

	_inherit = "hr.employee"

	_columns = {


		'religion': fields.selection([('muslim','muslim'),('christian','christian')],'religion',required=True),
		
	}
	
	_defaults = {

		'religion':'muslim',

	}


hr_employee()

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
				[('muslim', 'Muslim'), ('christian', 'Cristian'),],
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

		'from_': fields.integer('From',required=True),
		'to_': fields.integer('To',required=True),
		'allocation': fields.integer('Allocated leave',required=True),
		
		}

	_sql_constraints=[('unique_record','unique(from_,to_)','Service years records already there')]






class hr_holidays_status(osv.osv):

	_name = "hr.holidays.status"
	_description = "default allocation for leave types"
	_inherit = "hr.holidays.status"
	
	_columns = {

		'default_allocation': fields.integer('Allocation'),
		'transfer_allocation': fields.boolean('Transfer overflow', help='Allows you to transfer last years remaining holidays for this years'),

		'allocation_type': fields.selection([('1','Default allocation'),('2','Religion'),('3','Years of Service'),('4','Motherhood Leaves')],"Allocation based on",required=True),

	}

	_defaults = {

		'allocation_type': 'Default allocation',


	}

#remember to put constraints on allocation types

hr_holidays_status()


class hr_holidays(osv.osv):


	_name = "hr.holidays"
	_description = "Overriding default allocation scheme"
	_inherit = "hr.holidays"



	def get_Current_allocation_scheme(self, cr, uid, ids, employee_id, holiday_status_id, context=None):

		if context is None:
        		context = {}
		if employee_id and holiday_status_id:
			leave_type = self.pool.get("hr.holidays.status").browse(cr, uid, [holiday_status_id], context=context)[0].allocation_type
			res = 0

			if leave_type:

				if leave_type == '1':

					ids_ = self.pool.get("hr.holidays.status").search(cr,uid ,[('allocation_type','=',leave_type)])
					res = self.pool.get("hr.holidays.status").browse(cr, uid, ids_, context=context)[0].default_allocation	

				elif leave_type == '2':
	
					ids_ = self.pool.get("hr.employee").search(cr, uid, [('id','=',employee_id)])
					employee_religion = self.pool.get("hr.employee").browse(cr, uid, ids_, context=context)[0].religion

					ids_= self.pool.get("pilgrimage.leaves").search(cr, uid, [('religion','=',employee_religion)])
					res = self.pool.get("pilgrimage.leaves").browse(cr, uid, ids_, context=context)[0].leave_balance
			
				elif leave_type == '3':


					
					#ids_ = self.pool.get("hr.employee").search(cr, uid, [('id','=',employee_id)])
					#employee_name = self.pool.get("hr.employee").browse(cr, uid, ids_, context=context)[0].name

					ids_ = self.pool.get("hr.contract").search(cr , uid,[('employee_id','=',employee_id)])
	
					if ids_:

						contract_start = self.pool.get("hr.contract").browse(cr, uid, ids_ ,context=context)[0].date_start
						date_start = datetime.strptime(contract_start,"%Y-%m-%d")

						years_of_service = (datetime.now()-date_start).days/365

						ids_ = self.pool.get("leaves.service.time").search(cr, uid, [])
						objs = self.pool.get("leaves.service.time").browse(cr, uid, ids_ ,context=context)

						for obj in objs:

							if years_of_service >= obj.from_ and years_of_service <= obj.to_:

								res = obj.allocation



				elif leave_type == '4':

					
					ids_ = self.pool.get("hr.employee").search(cr, uid, [('id','=',employee_id)])
					children = self.pool.get("hr.employee").browse(cr, uid, ids_, context=context)[0].children
				
					if children == 0:
						res = 0
					else:

						ids_ = self.pool.get("motherhood.leaves").search(cr, uid, [('child_order','=',children)])
						if not ids_:

							ids_ = self.pool.get("motherhood.leaves").search(cr, uid, [])
							objs = self.pool.get("motherhood.leaves").browse(cr, uid, ids_ ,context=context)
							max_child = max([x.child_order for x in objs])

							for x in objs:
								if x.child_order == max_child:
									res = x.leave_balance

						res = self.pool.get("motherhood.leaves").browse(cr ,uid, ids_, context=context)[0].leave_balance


			return {'value':{'number_of_days_temp':res }}



	def _check_for_contract(self, cr, uid, ids, context=None):

		rec = self.browse(cr, uid, ids)[0]
		contract = self.pool.get("hr.contract").search(cr ,uid, [('employee_id','=',rec.employee_id.id)])
		if contract:
			return True
		return False


	def _default_holiday_status(self, cr, uid, ids, context=None):
		
		
		if context is None:
			context = {}

		ids_ = self.pool.get("hr.holidays.status").search(cr, uid, [])
		return self.pool.get("hr.holidays.status").browse(cr, uid, ids_[0], context=context).id

	_constraints = [(_check_for_contract,'Employee has no contract specified',['holiday_status_id'])]

	_defaults = {

		'holiday_status_id':_default_holiday_status,
	}



hr_holidays()	
