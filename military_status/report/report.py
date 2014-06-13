import time
from openerp.report import report_sxw
from openerp import pooler


class report(report_sxw.rml_parse):

	def __init__(self, cr, uid, name, context):
		
		super(report,self).__init__(cr,uid,name,context=context)		
		self.localcontext.update({'time': time ,'getNum': self._getNum ,'get_Current_User': self._get_Current_User})

	
	def _get_Current_User(self, context=None):


		if context:

			if context['uid']:

				return self.pool.get("res.users").browse(self.cr,self.uid, context['uid'], context=context).name

		return 

	def _getNum(self):

		return 1009

report_sxw.report_sxw('report.hr.military.report','hr.military.status','addons/insurance/report/report.mako',parser=report)
