from openerp.report import report_sxw
from datetime import datetime
import calendar
import time

class employee_permission_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(employee_permission_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_permissions_of_month' : self._get_permissions_of_month,
			'get_Current_User': self._get_Current_User,
			'time': time,
        })

	def _get_Current_User(self, context=None):


		if context:

			if context['uid']:

				return self.pool.get("res.users").browse(self.cr,self.uid, context['uid'], context=context).name

		return 


	def _get_permissions_of_month(self, form, context=None):
		year=form['year']
		month=form['month']

		last_day = calendar.monthrange(int(year), int(month))[1]

		date_from =datetime.strptime((str(month)+'-'+str(01)+'-'+str(year)),"%m-%d-%Y")		
		date_to = datetime.strptime((str(month)+'-'+str(last_day)+'-'+str(year)),"%m-%d-%Y")

   
		ids_ = self.pool.get('hr.permission').search(self.cr, self.uid, [('date_of_permission', '>=',date_from),('date_of_permission','<=',date_to)]) # browse(self.cr, self.uid, [form[0],],context=context)
		recs = self.pool.get('hr.permission').browse(self.cr, self.uid,ids_, context=context)
		return recs

report_sxw.report_sxw('report.employee.permission.report','hr.permission','addons/hr_permission/report/employee_permission_report.mako',parser=employee_permission_report)

