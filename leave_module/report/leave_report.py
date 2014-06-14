from openerp.report import report_sxw

class leave_by_year_report(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		super(leave_by_year_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_leave_byear' : self._get_leave_byear,
        })


	def _get_leave_byear(self, form, context=None):
		leave_ids = self.pool.get('formal.vacations').search(self.cr, self.uid, [('start_date', '>=', form['start_date']),('end_date', '<=', form['end_date']),])
		leave_recs = self.pool.get('formal.vacations').browse(self.cr, self.uid, leave_ids, context=context)
		return leave_recs
report_sxw.report_sxw('report.leave.byyear','formal.vacations','addons/leave_module/report/leave_report.mako',parser=leave_by_year_report)

