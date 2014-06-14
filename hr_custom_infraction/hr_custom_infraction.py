from openerp.osv import fields, osv
from openerp import netsvc
from hr_infraction.hr_infraction import hr_infraction
import logging
from datetime import datetime
import calendar
_logger = logging.getLogger(__name__)

class hr_infraction_category(osv.Model):
    _name = 'hr.infraction.category'
    _inherit ='hr.infraction.category'
    _columns = {
        'infraction_number':fields.integer('infraction number'),
        'penalty_days':fields.integer('penalty days',required=True),
        'discount':fields.selection([('Total','Total'),('Basic','Basic')],'Discount from',required=True,translated=True)
    }
    _defaults = {
        'infraction_number': 0
    }

hr_infraction_category()

ACTION_TYPE_SELECTION = [
    ('warning_verbal', 'Verbal Warning'),
    ('warning_letter', 'Written Warning'),
    ('transfer', 'Transfer'),
    ('suspension', 'Suspension'),
    ('dismissal', 'Dismissal'),
    ('discount_days','Discount days'),
    ]
class hr_infraction_custom_action(osv.Model):
    _inherit = 'hr.infraction.action'
    _columns = {
        'type': fields.selection(ACTION_TYPE_SELECTION, 'Type', required=True),
        }
hr_infraction_custom_action()
class hr_action(osv.TransientModel):
    _inherit='hr.infraction.action.wizard' 
    _columns={
		'action_type': fields.selection(ACTION_TYPE_SELECTION, 'Action', required=True),
        'penalty_days_value':fields.float('penalty days value'),
        }    

    def take_action(self,cr,uid,ids,context=None):
        infraction_id = context.get('active_id', False)
        obj = self.pool.get("hr.infraction").browse(cr,uid,[infraction_id],context=context)[0]
        id_= obj.employee_id.id
        cat_id = obj.category_id.id
        infraction_category_ids= self.pool.get("hr.infraction.category").search(cr,uid,[("id","=",cat_id)], context=context)
        penalty_days = self.pool.get("hr.infraction.category").browse(cr, uid, infraction_category_ids, context=context)[0].penalty_days
        discountFrom = self.pool.get("hr.infraction.category").browse(cr, uid, infraction_category_ids, context=context)[0].discount
        res = {}
        if discountFrom == "Basic":
            contract_obj= self.pool.get("hr.contract")
            contract_data=contract_obj.search(cr,uid,[('employee_id','=',id_)])
            emp_wage = contract_obj.browse(cr,uid,contract_data,context)
            daily_wage = emp_wage[0].wage/30
            days_value=daily_wage*penalty_days
            res['penalty_days_value'] = days_value
        return {'value':res}



    def create_action(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        infraction_id = context.get('active_id', False)
        if not infraction_id:
            return False
        data = self.read(cr, uid, ids[0], context=context)
        vals = {
            'infraction_id': infraction_id,
            'type': data['action_type'],
            'memo': data.get('memo', False),
        }
        action_id = self.pool.get('hr.infraction.action').create(
            cr, uid, vals, context=context)

        # Update state of infraction, if not already done so
        #
        infraction_obj = self.pool.get('hr.infraction')
        infraction_data = infraction_obj.read(
            cr, uid, infraction_id, ['employee_id', 'state'],
            context=context)
        if infraction_data['state'] == 'confirm':
            netsvc.LocalService(
                'workflow').trg_validate(uid, 'hr.infraction', infraction_id,
                                         'signal_action', cr)
        infraa_obj = self.pool.get('hr.infraction.action')
        imd_obj = self.pool.get('ir.model.data')
        iaa_obj = self.pool.get('ir.actions.act_window')
        # If the action is a warning create the appropriate record, reference it from the action,
        # and pull it up in the view (in case the user needs to make any changes.
        #
        if data['action_type'] in ['warning_verbal', 'warning_letter']:
            vals = {
                'name': (data['action_type'] == 'warning_verbal' and 'Verbal' or 'Written') + ' Warning',
                'type': data['action_type'] == 'warning_verbal' and 'verbal' or 'written',
                'action_id': action_id,
            }
            warning_id = self.pool.get('hr.infraction.warning').create(
                cr, uid, vals, context=context)
            infraa_obj.write(cr, uid, action_id, {
                             'warning_id': warning_id}, context=context)

            res_model, res_id = imd_obj.get_object_reference(
                cr, uid, 'hr_infraction',
                'open_hr_infraction_warning')
            dict_act_window = iaa_obj.read(cr, uid, res_id, [])
            dict_act_window['view_mode'] = 'form,tree'
            dict_act_window['domain'] = [('id', '=', warning_id)]
            return dict_act_window

        # If the action is a departmental transfer create the appropriate record, reference it from
        # the action, and pull it up in the view (in case the user needs to make any changes.
        #
        elif data['action_type'] == 'transfer':
            xfer_obj = self.pool.get('hr.department.transfer')
            ee = self.pool.get(
                'hr.employee').browse(cr, uid, infraction_data['employee_id'][0],
                                      context=context)
            _tmp = xfer_obj.onchange_employee(
                cr, uid, None, ee.id, context=context)
            vals = {
                'employee_id': ee.id,
                'src_id': _tmp['value']['src_id'],
                'dst_id': data['new_job_id'][0],
                'src_contract_id': _tmp['value']['src_contract_id'],
                'date': data['xfer_effective_date'],
            }
            xfer_id = xfer_obj.create(cr, uid, vals, context=context)
            infraa_obj.write(cr, uid, action_id, {
                             'transfer_id': xfer_id}, context=context)

            res_model, res_id = imd_obj.get_object_reference(
                cr, uid, 'hr_transfer',
                'open_hr_department_transfer')
            dict_act_window = iaa_obj.read(cr, uid, res_id, [])
            dict_act_window['view_mode'] = 'form,tree'
            dict_act_window['domain'] = [('id', '=', xfer_id)]
            return dict_act_window

        # The action is dismissal. Begin the termination process.
        #
        elif data['action_type'] == 'dismissal':
            term_obj = self.pool.get('hr.employee.termination')
            wkf = netsvc.LocalService('workflow')
            ee = self.pool.get(
                'hr.employee').browse(cr, uid, infraction_data['employee_id'][0],
                                      context=context)

            # We must create the employment termination object before we set
            # the contract state to 'done'.
            res_model, res_id = imd_obj.get_object_reference(
                cr, uid, 'hr_infraction', 'term_dismissal')
            vals = {
                'employee_id': ee.id,
                'name': data['effective_date'],
                'reason_id': res_id,
            }
            term_id = term_obj.create(cr, uid, vals, context=context)
            infraa_obj.write(cr, uid, action_id, {
                             'termination_id': term_id}, context=context)

            # End any open contracts
            for contract in ee.contract_ids:
                if contract.state not in ['done']:
                    wkf.trg_validate(
                        uid, 'hr.contract', contract.id, 'signal_pending_done', cr)

            # Set employee state to pending deactivation
            wkf.trg_validate(
                uid, 'hr.employee', ee.id, 'signal_pending_inactive', cr)

            # Trigger confirmation of termination record
            wkf.trg_validate(
                uid, 'hr.employee.termination', term_id, 'signal_confirmed', cr)

            res_model, res_id = imd_obj.get_object_reference(
                cr, uid, 'hr_employee_state',
                'open_hr_employee_termination')
            dict_act_window = iaa_obj.read(cr, uid, res_id, [])
            dict_act_window['domain'] = [('id', '=', term_id)]
            return dict_act_window
        

        elif data['action_type'] == 'discount_days':
            _logger.info("-------------------IN Discount Days----------------------------")
            _logger.info(data['action_type'])
            _logger.info("---------------------------------------------------------------")
            ee = self.pool.get(
                'hr.employee').browse(cr, uid, infraction_data['employee_id'][0],
                                      context=context)
            infraction_id = context.get('active_id', False)
            vals={
            'infraction':infraction_id,
            'employee':ee.id,
            'penalty_value':data['penalty_days_value'],
            }
            discount_id = self.pool.get('hr.infraction.action.discount').create(
                cr, uid, vals, context=context)
            return True
            
        return True
hr_action()

class hr_infraction_action_discount(osv.Model):
    
	_name = 'hr.infraction.action.discount'
	
	def _get_Days(self, cr, uid, ids, name, arg, context=None):

		if context is None:
			context = {}

		return {ids[0]:self.browse(cr, uid, ids, context=context)[0].infraction.category_id.penalty_days}

	_columns = {
        	'employee':fields.many2one('hr.employee','Employee', readonly=True),
		'infraction':fields.many2one('hr.infraction','Infraction', readonly=True),
		'penalty_value':fields.float('penalty value',readonly=True),
		'actual_penalty':fields.float('actual penalty'),
		'confirmed':fields.boolean('confirmed'),
		'state':fields.selection([('totaly_paied','Totaly paied'),('decreased','Decreased'),('exempt','Exempt'),('installment','Installment')],'state',translated=True),
		'days': fields.function(_get_Days,string="days",type='float',store=True)
    	}
hr_infraction_action_discount()

class infraction_overflow(osv.osv):

	_name = "infraction.overflow"
	_description = "Keep record of overflow infractions from each month"
	_columns = {

		'employee_id': fields.integer('Employee'),
		'infraction_id': fields.integer('Infraction'),

	}



class hr_employee(osv.osv):

	_name = "hr.employee"
	_inherit = "hr.employee"
	_description = "Add infraction deduction fields"
	
	

	def _get_Infraction(self , cr, uid, ids, field_name, arg, context=None):

		penalty_days = 0
		penalty_deduction = 0		

		if context is None:
			context = {}

		employee_id = self.browse(cr, uid, ids, context=context)[0].id
		ids_ = self.pool.get("infraction.overflow").search(cr, uid, [('employee_id','=',employee_id)])
		overflow_id = self.pool.get("infraction.overflow").browse(cr, uid, ids_, context=context)
		ids_ = [ x.infraction_id for x in overflow_id ]
		overflow_rec = self.pool.get("hr.infraction.action.discount").browse(cr, uid, ids_, context=context)	

		for obj in overflow_rec:

			flag = 0
			if obj.actual_penalty :

				days_calc = int(obj.actual_penalty/(obj.employee.contract_id.wage/30))
				
				flag = 1
			else :
				days_calc = obj.days		

			if penalty_days+days_calc > 5:

				update_days = days_calc+penalty_days - 5
				penalty_days = 5
				#recalculate penalty
				new_pen = update_days * obj.employee.contract_id.wage/30
				#update record
				penalty_deduction = 5 * obj.employee.contract_id.wage/30
				if flag:

					self.pool.get("hr.infraction.action.discount").write(cr, uid, [obj.id], {'actual_penalty': new_pen, })
	
				else:
					
					self.pool.get("hr.infraction.action.discount").write(cr, uid, [obj.id], {'days': update_days, 'penalty_value': new_pen, })
				
				break

			else:
				penalty_days += days_calc
				
				if flag:
					penalty_deduction += obj.actual_penalty 
				else:
					penalty_deduction += obj.penalty_value
		
				ids_ = self.pool.get("infraction.overflow").search(cr, uid, [('infraction_id','=',obj.id)])
				self.pool.get("infraction.overflow").unlink(cr, uid, ids_)
				self.pool.get("hr.infraction.action.discount").unlink(cr, uid, [obj.id])



		curr_month = datetime.now().month
		curr_year = datetime.now().year
		range_ = calendar.monthrange(curr_year,curr_month)
		begin_month = datetime.strptime('1-%d-%d' % (curr_month,curr_year),"%d-%m-%Y")
		end_month = datetime.strptime('%d-%d-%d' % (range_[1],curr_month,curr_year),"%d-%m-%Y")
		
		
		rec_ids = self.pool.get("hr.infraction.action.discount").search(cr, uid, [('employee','=',employee_id),('create_date','>=',begin_month),('create_date','<=',end_month)])

		if rec_ids:

			

			records = self.pool.get("hr.infraction.action.discount").browse(cr, uid, rec_ids, context=context)

			if penalty_days > 5:

				for rec in records:
			
					self.pool.get("infraction.overflow").create(cr , uid, { 'employee_id':rec.employee ,'infraction_id':rec.id })

			else:

				
				for rec in records:

					
					
					if penalty_days == 5:
			
						
						self.pool.get("infraction.overflow").create(cr, uid,  {'employee_id':rec.employee,'infraction_id':rec.id})
			
						pass

					flag = 0
					if rec.actual_penalty :

						days_calc = int(rec.actual_penalty/(rec.employee.contract_id.wage/30))  							
						flag = 1
					else :
						days_calc = rec.days		

					if penalty_days+days_calc > 5:
				
						update_days = (days_calc+penalty_days) - 5
						penalty_days = 5
						#recalculate penalty
						new_pen = update_days * rec.employee.contract_id.wage/30
						penalty_deduction = 5 * rec.employee.contract_id.wage/30
						#update record
						if flag:

							self.pool.get("hr.infraction.action.discount").write(cr, uid, [rec.id], {'actual_penalty': new_pen, })
	
						else:
					
							self.pool.get("hr.infraction.action.discount").write(cr, uid, [rec.id], {'days': update_days, 'penalty_value':new_pen, })

						self.pool.get("infraction.overflow").create(cr, uid, {'employee_id':rec.employee,'infraction_id':rec.id})

					else:
						penalty_days += days_calc
				
						if flag:
							penalty_deduction += rec.actual_penalty 
						else:
							penalty_deduction += rec.penalty_value
		
						
						self.pool.get("hr.infraction.action.discount").unlink(cr, uid, [rec.id])
				
		res = {}
		res[ids[0]] = penalty_deduction
		return res

	_columns = {


		'total_infraction': fields.function(_get_Infraction,type='float'),

	}

	
hr_employee()





