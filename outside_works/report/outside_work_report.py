from openerp.report import report_sxw


class sci_inst_byname_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(sci_inst_byname_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_outside_work_by_name' : self._get_outside_work_by_name,
        })


	def _get_outside_work_by_name(self, form, context=None):
		sci_inst_ids = self.pool.get('outside.works.forms').search(self.cr, self.uid, [('start_date', '>=', form['start_date']),('end_date', '<=', form['end_date']),])
		sci_int_recs = self.pool.get('outside.works.forms').browse(self.cr, self.uid, sci_inst_ids, context=context)
		return sci_int_recs
		
report_sxw.report_sxw('report.outside.works.dates','outside.works.forms','addons/outside_works_report/report/outside_work_report.mako',parser=sci_inst_byname_report)

