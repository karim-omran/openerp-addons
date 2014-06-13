from openerp.report import report_sxw
import time
import logging

_logger = logging.getLogger(__name__)

class action_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(action_report, self).__init__(cr, uid, name, context=context)
		self.localcontext.update({
			'get_actions' : self.get_actions,
        })

	def get_actions(self, form, context=None):
		action_ids = self.pool.get('hr.infraction.action').search(self.cr, self.uid, [('employee_id','=',form[0])]) # browse(self.cr, self.uid, [form[0],],context=context)
		actions = self.pool.get('hr.infraction.action').browse(self.cr, self.uid, action_ids, context=context)
		return actions
report_sxw.report_sxw('report.action','hr.infraction.action','addons/hr_custom_infraction/report/action_report.mako',parser=action_report)