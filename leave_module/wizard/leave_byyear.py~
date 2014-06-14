import time
from openerp.osv import osv, fields

class leave_by_year(osv.osv_memory):
	_name = 'leave.by.year'
	_description = 'Print Formal Leave Report'

	_columns = {
			'start_date' : fields.date(
				'From : ',
				size=50,
				required=True,
				),

			'end_date' : fields.date(
				'To : ',
				size=50,
				required=True,
				),
		}



	def print_report(self, cr, uid, ids, data, context=None):

		datas = {

				'form': self.read(cr, uid, ids,['start_date','end_date'], context=context)[0]
			}
		

		
		return {
				'type': 'ir.actions.report.xml',
				'report_name': 'leave.byyear',
				'datas': datas,
				}

leave_by_year()
