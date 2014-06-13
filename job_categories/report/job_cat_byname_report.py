from openerp.report import report_sxw


class job_cat_byname_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(job_cat_byname_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_job_byname' : self._get_job_byname,
        })


	def _get_job_byname(self, form, context=None):
		#job_cat_id = self.pool.get('job.categories').search(self.cr, self.uid, [('job_category', '=', form[0]), ], context=context)
		return self.pool.get('job.categories').browse(self.cr, self.uid, form[0], context=context)

report_sxw.report_sxw('report.job.cat.byname','job.categories','addons/job_categories/report/job_cat_byname_report.mako',parser=job_cat_byname_report)
