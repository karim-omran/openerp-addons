import time
from openerp.osv import osv, fields

class sci_inst_by_name(osv.osv_memory):
	_name = 'sci.inst.by.name'
	_description = 'Print Scientific Institution Report'

	_columns = {
			'sci_inst_name' : fields.many2one(
				'institution.name',
				'Institution',
				required=True,
				),
		}



	def print_report(self, cr, uid, ids, data, context=None):

		datas = {
				'model': 'scientific.institution',
				'form': self.read(cr, uid, ids, context=context)[0]['sci_inst_name']
			}
		

		
		return {
				'type': 'ir.actions.report.xml',
				'report_name': 'sci.inst.byname',
				'datas': datas,
				}

sci_inst_by_name()
