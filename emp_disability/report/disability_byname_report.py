from openerp.report import report_sxw
import logging
_logger = logging.getLogger(__name__)

class disability_byname_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(disability_byname_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
            
			'_get_inst_byname' : self._get_inst_byname,
        })


	def _get_inst_byname(self, form, context=None):
		disability_ids = self.pool.get('hr.employee').search(self.cr, self.uid, [('disability_type', '=', form[0]),])
		_logger.info('********************______**********************')
		_logger.info(disability_ids)
		_logger.info('********************______**********************')
		disability_recs = self.pool.get('hr.employee').browse(self.cr, self.uid, disability_ids, context=context)
		return disability_recs
report_sxw.report_sxw('report.disability.byname.new.report','emp.disabilities','addons/emp_disability/report/sci_inst_byname_report.mako',parser=disability_byname_report)

