import time
from openerp.osv import osv, fields
import logging

_logger = logging.getLogger(__name__)

class action_employee_report(osv.osv_memory):
	_name = 'action.report'
	_description = 'Print Actions Report'

	_columns = {
			'employee' : fields.many2one(
				'hr.employee',
				'Employee Name',
				required=True,
				),
		}



	def print_report(self, cr, uid, ids,data, context=None):
		datas = {
				'model': 'hr.infraction.action',
				'form': self.read(cr, uid, ids, context=context)[0]['employee'],
			}
		
		return {
				'type': 'ir.actions.report.xml',
				'report_name': 'action',
				'datas': datas,
				}

action_employee_report()
