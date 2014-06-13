from openerp.report import report_sxw


class sci_inst_byname_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(sci_inst_byname_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_inst_byname' : self._get_inst_byname,
        })


	def _get_inst_byname(self, form, context=None):

		sci_inst_ids = self.pool.get('scientific.institution').search(self.cr, self.uid, [('inst_name', 'like', form[0]),]) # browse(self.cr, self.uid, [form[0],],context=context)
		sci_int_recs = self.pool.get('scientific.institution').browse(self.cr, self.uid, sci_inst_ids, context=context)
		return sci_int_recs
report_sxw.report_sxw('report.sci.inst.byname','scientific.institution','addons/scientific_institutions/report/sci_inst_byname_report.mako',parser=sci_inst_byname_report)

