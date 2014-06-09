from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time
from attendance_analysis import attendance_analysis
import logging
from datetime import datetime
 
class hr_attendance(osv.osv):
	_name = 'hr.attendance'
	_inherit = 'hr.attendance'
	_description = 'attendance modification'
	_columns = {

			'sign_in_time' : fields.float('Sign in time',required=True,),
			
			'mintues_late' : fields.float('Mintues late',required=True,),
		}
	
	def cal_late_in_mins (self, cr, uid, ids, sign_in_time, employee_id=None, context=None):
		res = {}
		working_hours = self.pool.get("hr.contract").search(cr, uid, [("employee_id",'=', employee_id)], context=context)#select rakm el 3a2d
		id_hours_from = self.pool.get("resource.calendar.attendance").search(cr, uid, [("calendar_id",'=', working_hours[0])], context=context) #select el 3a2d nafsoh b el data bat3toh
		hours_from =  self.pool.get("resource.calendar.attendance").read(cr, uid, [id_hours_from[0]], context=context) #select el work_from hours mn el 3a2d 
		mintues_late = sign_in_time - hours_from[0]['hour_from']

		id_company_id = self.pool.get("resource.calendar").search(cr, uid, [("id",'=', id_hours_from[0])], context=context)
		company_id =  self.pool.get("resource.calendar").read(cr, uid, [id_company_id[0]], context=context)
				
		id_day_late = self.pool.get("res.company").search(cr, uid, [("id", '=', company_id[0]['company_id'][0])], context=context)		
		day_late =  self.pool.get("res.company").read(cr, uid, [id_day_late[0]], context=context)[0]
	
		#date = self.read(cr,uid,ids,['name'],context=context)[0]
		#hrs = time.strptime(date['name'].split(" ")[1], "%H:%M:%S")[3]
		#mins = time.strptime(date['name'].split(" ")[1], "%H:%M:%S")[4]
		#signTime = float(str(hrs)+'.'+str(mins))
	
		late = mintues_late - day_late['day_late']

		#if late < 0.00 :
			#late = 0.00
		res['mintues_late'] = late

		return {'value':res}
		
		
		
		


hr_attendance()

