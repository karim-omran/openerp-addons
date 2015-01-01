from datetime import datetime
import time
from openerp import netsvc, tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

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

	_constraints = [(_check_fields, 'Error : Fiedls Must Be Positive Number Higher Than 0!', ['child_order', 'leave_balance']),]





class pilgrimage_leaves(osv.osv):

	_name = 'pilgrimage.leaves'

	_description = 'pilgrimage leaves model'

	_rec_name = 'religion'

	_columns = {

			'religion' : fields.selection(
				[('muslim', 'Muslim'), ('christian', 'Christian'),],
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


			return {'value':{'number_of_days_temp':res}}



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


	def leaves_allocation_cron_job(self, cr, uid, ids=all, context=None):
		
		# get today information
		day = datetime.today().day
		month = datetime.today().month

		# this function should run at date 1/1 every year
		if day == 1 and month == 1:

			emp_gender = None
			emp_children = None
			emp_religion = None

			# get all employee ids
			all_emp_ids = self.pool.get('hr.employee').search(cr, uid, [])
			
			for emp_id in all_emp_ids:
				# get information stored in each employee object
				emp_info = self.pool.get('hr.employee').browse(cr, uid, emp_id)

				if emp_info.gender:
					emp_gender = emp_info.gender
				if emp_info.children:
					emp_children = emp_info.children
				if emp_info.religion:
					emp_religion = emp_info.religion


				# get each employee contract
				emp_contract_id = self.pool.get('hr.contract').search(cr ,uid, [('employee_id','=',emp_id)])
				
				# if employee has a contract registered years of service leave
				if emp_contract_id:
					emp_contract = self.pool.get('hr.contract').browse(cr, uid, emp_contract_id[0])
					emp_start_service = datetime.strptime(emp_contract.date_start,"%Y-%m-%d")
					years_of_service = (datetime.now()-emp_start_service).days/365

					service_leave_id = self.pool.get('leaves.service.time').search(cr, uid, [('from_', '<=', years_of_service), ('to_', '>=' , years_of_service)])
					holiday_status_id = self.pool.get('hr.holidays.status').search(cr, uid, [('allocation_type', '=', '3')])
					holiday_status_rec = self.pool.get('hr.holidays.status').browse(cr, uid, holiday_status_id[0])

					if service_leave_id and holiday_status_id and holiday_status_rec.transfer_allocation:
						leave_period = self.pool.get('leaves.service.time').browse(cr, uid, service_leave_id[0]).allocation

						# save new leave to database --> don't try to create it with validate state directly "will not work" :)
						holiday_id = self.pool.get('hr.holidays').create(cr, uid, {
								'holiday_status_id' : holiday_status_id[0],
								'employee_id' : emp_id,
								'department_id' : emp_info.department_id.id,
								'user_id' : uid,
								'name' : holiday_status_rec.name,
								'number_of_days' : float(leave_period),
								'number_of_days_temp' : leave_period,
								'holiday_type' : 'employee',
								'state' : 'confirm',
								'manager_id' : emp_info.parent_id.id,
								'type' : 'add',
							})
						
						# change leave state to be confirmed
						self.pool.get('hr.holidays').write(cr, uid, [holiday_id,], {
								'state' : 'validate',
							})

						

				# if female employee and has contract add motherhood leave to new years leaves
				if emp_gender == "female" and emp_children > 0 and emp_contract_id:
					motherhood_leave_id = self.pool.get('motherhood.leaves').search(cr, uid, [('child_order', '=', emp_children)])
					holiday_status_id = self.pool.get('hr.holidays.status').search(cr, uid, [('allocation_type', '=', '4')])
					holiday_status_rec = self.pool.get('hr.holidays.status').browse(cr, uid, holiday_status_id[0])

					# if motherhood leave rule id found and holiday stored in holidays types and leave can be transfered to next year.
					if motherhood_leave_id and holiday_status_id and holiday_status_rec.transfer_allocation: 
						leave_period = self.pool.get('motherhood.leaves').browse(cr, uid, motherhood_leave_id[0]).leave_balance
						
						# save new leave to database 
						holiday_id = self.pool.get('hr.holidays').create(cr, uid, {
								'holiday_status_id' : holiday_status_id[0],
								'employee_id' : emp_id,
								'department_id' : emp_info.department_id.id,
								'user_id' : uid,
								'name' : holiday_status_rec.name,
								'number_of_days' : float(leave_period),
								'number_of_days_temp' : leave_period,
								'holiday_type' : 'employee',
								'state' : 'confirm',
								'manager_id' : emp_info.parent_id.id,
								'type' : 'add',
							})
						# change leave state to be confirmed
						self.pool.get('hr.holidays').write(cr, uid, [holiday_id,], {
								'state' : 'validate',
							})
					# if exeeded maximum number of children
					elif holiday_status_id and holiday_status_rec.transfer_allocation:
						all_moth_leaves_ids = self.pool.get("motherhood.leaves").search(cr, uid, [])
						leave_objs = self.pool.get("motherhood.leaves").browse(cr, uid, all_moth_leaves_ids ,context=context)
						max_leave_period = max([leave.leave_balance for leave in leave_objs])
						
						holiday_id = self.pool.get('hr.holidays').create(cr, uid, {
									'holiday_status_id' : holiday_status_id[0],
									'employee_id' : emp_id,
									'department_id' : emp_info.department_id.id,
									'user_id' : uid,
									'name' : holiday_status_rec.name,
									'number_of_days' : float(max_leave_period),
									'number_of_days_temp' : max_leave_period,
									'holiday_type' : 'employee',
									'state' : 'confirm',
									'manager_id' : emp_info.parent_id.id,
									'type' : 'add',
								})
						# change leave state to be confirmed
						self.pool.get('hr.holidays').write(cr, uid, [holiday_id,], {
								'state' : 'validate',
							})


				# if employee is muslim or christian and has contract add pilgrimage leave balance
				if emp_contract_id:
					pilgrimage_leave_id = self.pool.get('pilgrimage.leaves').search(cr, uid, [('religion', '=', emp_religion)])
					holiday_status_id = self.pool.get('hr.holidays.status').search(cr, uid, [('allocation_type', '=', '2')])
					holiday_status_rec = self.pool.get('hr.holidays.status').browse(cr, uid, holiday_status_id[0])

					# if pilgrimage leave rule found and holiday stored in holidays types
					if pilgrimage_leave_id and holiday_status_id and holiday_status_rec.transfer_allocation:
						leave_period = self.pool.get('pilgrimage.leaves').browse(cr, uid, pilgrimage_leave_id[0]).leave_balance

						# save new leave to database 
						holiday_id = self.pool.get('hr.holidays').create(cr, uid, {
								'holiday_status_id' : holiday_status_id[0],
								'employee_id' : emp_id,
								'department_id' : emp_info.department_id.id,
								'user_id' : uid,
								'name' : holiday_status_rec.name,
								'number_of_days' : float(leave_period),
								'number_of_days_temp' : leave_period,
								'holiday_type' : 'employee',
								'state' : 'confirm',
								'manager_id' : emp_info.parent_id.id,
								'type' : 'add',
							})
						# change leave state to be confirmed
						self.pool.get('hr.holidays').write(cr, uid, [holiday_id,], {
								'state' : 'validate',
							})

			return True



hr_holidays()	
