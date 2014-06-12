import time
from datetime import datetime
from openerp.report import report_sxw
from openerp import pooler

class course_search(report_sxw.rml_parse):

	def __init__(self, cr, uid, ids, context):
		
		super(course_search,self).__init__(cr, uid, ids, context=context)	
		self.localcontext.update({
			
			'time':time, 
			'get_Course':self._get_Course,
			'get_Current_User':self._get_Current_User,
			'datetime':datetime, 
		})


	def _get_Course(self, form, context=None):

		course_ids = self.pool.get("hr.training.course").search(self.cr, self.uid, [("from_date",">=",form["range_start"]),("from_date","<=",form["range_end"])], context=context)
		
		courses = self.pool.get("hr.training.course").browse(self.cr,self.uid,course_ids,context=context)

		return courses
	
	def _get_Current_User(self, context=None):


		if context:

			if context['uid']:

				return self.pool.get("res.users").browse(self.cr,self.uid, context['uid'], context=context).name

		return 

report_sxw.report_sxw('report.course.search','hr.training.course','addons/hr_training/report/course_search.mako', parser=course_search , header="internal")

