from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class hr_attendance(osv.osv):
	_name = 'hr.attendance'
	_inherit = 'hr.attendance'
	_description = 'attendance modification'
	

	def cal_late (self, cr, uid, ids, field_name, arg, context):
		_logger.info(ids[0])
		res = {}
		obj=self.browse(cr, uid, ids[0])
		_logger.info(obj.action)
		if obj.action=='sign_in':
			working_hours = self.pool.get("hr.contract").search(cr, uid, [("employee_id",'=', obj.employee_id.id)], context=context)[0]#select rakm el 3a2d
			contract_obj= self.pool.get("hr.contract").browse(cr, uid,working_hours, context=context)
			if working_hours:
				hrs = time.strptime(obj.name.split(" ")[1], "%H:%M:%S")[3]
				mins = time.strptime(obj.name.split(" ")[1], "%H:%M:%S")[4]
				signTime = float(str(hrs)+'.'+str(mins))
				mintues_late = signTime - contract_obj.working_hours.attendance_ids[0].hour_from 
				late = mintues_late - contract_obj.working_hours.company_id.day_late
				if late < 0.00 :
					late = 0.00
				return {ids[0]:late}
		else:
			return {ids[0]:0}
	_columns = {			
			'mintues_late' : fields.function( cal_late, type='float', method=True, string='Minutes Late', store=True),
		}

hr_attendance()
class res_company(osv.osv):
	_name = 'res.company'
	_inherit = 'res.company'
	_columns = {
							'day_late' : fields.float('Day_late'),
							'max_late' : fields.float('Max_late'),
							'month_late' : fields.float('Month_late'),
							'number_of_permissions' : fields.integer('Number of permissions'),
}

