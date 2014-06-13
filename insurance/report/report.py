import time
from openerp.report import report_sxw
from openerp import pooler


class report(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		
		super(report,self).__init__(cr,uid,name,context=context)		
		self.localcontext.update({'time': time ,'getNum': self._getNum ,})


	def _getNum(self):

		return 1009

report_sxw.report_sxw('report.hr.insurance.report','hr.insurance','addons/insurance/report/report.mako',parser=report)
