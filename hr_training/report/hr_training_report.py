import time
from datetime import datetime
from openerp.report import report_sxw
from openerp import pooler

class hr_training_report(report_sxw.rml_parse):

	def __init__(self, cr, uid, ids, context):
		
		super(hr_training_report,self).__init__(cr, uid, ids, context=context)	
		self.localcontext.update({
			
			'time':time, 
			'getEmps':self._getEmps,
			'datetime':datetime,
			'get_Course_Name':self._get_Course_Name,
			'get_Current_User':self._get_Current_User, 
		})


	def _getEmps(self, context=None):

		objs = self.pool.get("hr.training.register").search(self.cr, self.uid, [("course","=",self.ids[0])])
		employees_ids = self.pool.get("hr.training.register").browse(self.cr, self.uid, objs, context=context)
		id_list = [ x.employee.id for x in employees_ids ] 
		employees= self.pool.get("hr.employee").browse(self.cr, self.uid, id_list, context=context)


		return employees

	def _get_Current_User(self, context=None):


		if context:

			if context['uid']:

				return self.pool.get("res.users").browse(self.cr,self.uid, context['uid'], context=context).name

		return 


	def _get_Course_Name(self, context=None):

		course = self.pool.get("hr.training.course").browse(self.cr, self.uid, self.ids, context=context)
		return course[0].name


report_sxw.report_sxw('report.hr.training.report','hr.training.course','addons/hr_training/report/hr_training_report.mako', parser=hr_training_report)

