from openerp.report import report_sxw
import time

class job_cat_byname_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(job_cat_byname_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_job_byname' : self._get_job_byname,
			'get_Current_User': self._get_Current_User,
			'time': time
        })


	def _get_Current_User(self, context=None):


		if context:

			if context['uid']:

				return self.pool.get("res.users").browse(self.cr,self.uid, context['uid'], context=context).name

		return 


	def _get_job_byname(self, form, context=None):
		#job_cat_id = self.pool.get('job.categories').search(self.cr, self.uid, [('job_category', '=', form[0]), ], context=context)
		return self.pool.get('job.categories').browse(self.cr, self.uid, form[0], context=context)

report_sxw.report_sxw('report.job.cat.byname','job.categories','addons/job_categories/report/job_cat_byname_report.mako',parser=job_cat_byname_report)
