from openerp.osv import osv, fields

class job_cat_byname(osv.osv_memory):

	_name = 'job.cat.byname'

	_description = 'print job category report by name'

	_rec_name = 'job_cat_name'

	_columns = {
			'job_cat_name' : fields.many2one(
						'job.categories',
						'Job Category',
						required=True,
						onupdate='cascade',
					),
		}

	def print_report(self, cr, uid, ids, data, context=None):
		
		datas = {
				'model' : 'job.categories',
				'form' : self.read(cr, uid, ids, context=context)[0]['job_cat_name']
			}

		return {
				'type' : 'ir.actions.report.xml',
				'report_name' : 'job.cat.byname',
				'datas' : datas,
			}


job_cat_byname()