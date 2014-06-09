import time
from openerp.osv import osv, fields

class permission_per_month(osv.osv_memory):
	_name = 'permission.per.month'
	_description = 'Print Employee Permission Report'


	def _get_selection(self, cursor, user_id, context=None):
		return (('1','1'), ('2', '2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10'), ('11','11'), ('12','12'))


	_columns = {
			'month' : fields.selection( _get_selection, 'Month', reqiured=True),
			'year' : fields.char('Year',required=True,),
		}


	def print_report(self, cr, uid, ids, data, context=None):
		record = self.pool.get('permission.per.month').read(cr,uid,ids,['month','year'],context=context)[0]

		datas = {
				'form': record
			}
			
		return {
				'type': 'ir.actions.report.xml',
				'report_name': 'employee.permission.report',
				'datas': datas,
				}

permission_per_month()
