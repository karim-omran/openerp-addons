import time
from openerp.osv import osv, fields

import logging
_logger = logging.getLogger(__name__)


class select_permission_for_employee(osv.osv_memory):
	_name = 'select.permission.for.employee'
	_description = 'Print Employee Permission Report'

	def _get_selection(self, cursor, user_id, context=None):
		return (('1','1'), ('2', '2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12'))

	_columns = {
			'month' : fields.selection( _get_selection, 'Month', reqiured=True),
			'year' : fields.char('Year',required=True,),
			'employee_name' : fields.many2one('hr.employee', 'Employee name'),
		}

	_rec_name = 'employee_name'
	def print_report(self, cr, uid, ids, data, context=None):
		record = self.pool.get('select.permission.for.employee').read(cr,uid,ids,['month','year','employee_name'],context=context)[0]
		_logger.info("wizard 24")
		_logger.info(record)
		datas = {
				'form': record
			}
		_logger.info("wizard 29")
		_logger.info(datas)
		return {
				'type': 'ir.actions.report.xml',
				'report_name': 'employees.report',
				'datas': datas,
				}

select_permission_for_employee()
