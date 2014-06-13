import time

from openerp.osv import osv, fields

class hr_attendance_bymonth(osv.osv_memory):
    _name = 'hr.outside.works'
    _description = 'Print outside works for employees in a duration'
    _columns = {
        'start_date' : fields.date(
				'Start Date',
				required=True,
				),

        'end_date' : fields.date(
				'End Date',
				required=True,
				),
    }

    def print_report(self, cr, uid, ids, data, context=None):
        
        record = self.read(cr, uid, ids,['start_date', 'end_date'], context=context)[0]


        datas = {
                'model': 'outside.works.forms',
                'form': record
                }

        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'outside.works.dates',
                   'datas': datas,
                }

hr_attendance_bymonth()

