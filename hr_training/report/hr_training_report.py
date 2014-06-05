import time
from openerp.report import report_sxw
from openerp import pooler

class hr_training_report(report_sxw.rml_parse):

	def __init__(self, cr, uid, ids, context):
		
		super(hr_training_report,self).__init__(cr, uid, ids, context=context)	
		self.localcontext.update({
			
			'time':time, 
			'getEmps':self._getEmps,
			'get_Course_Name':self._get_Course_Name, 
		})


	def _getEmps(self, context=None):

		objs = self.pool.get("hr.training.register").search(self.cr, self.uid, [("course","=",self.ids[0])])
		
		employees= self.pool.get("hr.employee").browse(self.cr, self.uid, objs, context=context)


		return employees

	def _get_Course_Name(self, context=None):

		course = self.pool.get("hr.training.course").browse(self.cr, self.uid, self.ids, context=context)
		return course[0].name


report_sxw.report_sxw('report.hr.training.report','hr.training.course','addons/hr_training/report/hr_training_report.mako', parser=hr_training_report)

