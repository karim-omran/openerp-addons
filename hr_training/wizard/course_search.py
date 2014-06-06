import time

from openerp.osv import osv, fields

class course_search(osv.osv_memory):
    _name = 'course.search'
    _description = 'Courses by date'

    _columns = {
        'range_start': fields.date('Range from', required=True),
        'range_end': fields.date('To', required=True),
    }
    _defaults = {
        'range_start': lambda *a: time.strftime('%Y-%m-%d'),
        'range_end': lambda *a: time.strftime('%Y-%m-%d'),
    }

    def print_report(self, cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return : retrun report
        """
        if context is None:
            context = {}
    	datas = {'ids': context.get('active_ids', [])}
        res = self.read(cr, uid, ids, ['range_start', 'range_end'], context=context)
        res = res and res[0] or {}
        datas['form'] = res
        if res.get('id',False):
            datas['ids']=[res['id']]
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'course.search',	
            'datas': datas,
        }


course_search()
