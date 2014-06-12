from openerp.osv import osv,fields
from openerp.tools.translate import _
import time
import datetime

class hr_employee(osv.osv):
	_name = "hr.employee"
	_inherit = "hr.employee"
	_columns = { 
		'available_perm' : fields.integer('Available permissions', required=True),
	}
	_defaults = {

		'available_perm': 1
	}


hr_employee()

class hr_permission(osv.osv):
	_name = "hr.permission"
	_description = "Ask for a permission"
	_columns = { 
		'employee_name':fields.many2one('hr.employee', 'Employee name', required=True),
		'type_of_permission':fields.many2one('hr.typeofpermission', 'Type of permission', required=True),
		'date_of_permission':fields.date('Date',required=True),
		'available_permission':fields.integer('Permissions', required=True),
		'state': fields.selection([('draft', 'New'),
            ('open', 'Accepted'),
            ('cancel', 'Refused'),
            ('close', 'Done')],
            'Status', readonly=True, track_visibility='onchange',
        )
	}
	_defaults = {
		  'state': lambda *a: 'draft',
			'available_permission':1,
	}
 
	def _check_date(self, cr, uid, ids, context=None):
		now = datetime.date.today().strftime("%Y-%m-%d")
		record = self.browse(cr, uid, ids, context=context)
		if record[0].date_of_permission < now:
			return False 
		else:
			return True
	

	_constraints = [(_check_date, 'Error : Date must be today or after that', ['date_of_permission']),]
								


	def permission_cancel(self, cr, uid, ids, context=None):
		return self.write(cr, uid, ids, {'state': 'cancel'}, context=context)

	def permission_open(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'open'}, context=context)

	def permission_close(self, cr, uid, ids,employee_name,context={}):
		new_permission = 0		
		if employee_name:
			ids_ = self.pool.get("hr.employee").search(cr, uid, [("name","=",employee_name.name)], context=context)
			obj = self.pool.get("hr.employee").browse(cr, uid, ids_, context=context)
			if obj[0].available_perm <= 3:
				new_permission = obj[0].available_perm + 1
		if new_permission != 4:	
			self.pool.get("hr.employee").write(cr, uid, ids_, {'available_perm':new_permission}, context=context)
			return self.write(cr, uid, ids, {'state': 'close'}, context=context)
		else:
			
			new_permission = obj[0].available_perm + 1
			self.pool.get("hr.employee").write(cr, uid, ids_, {'available_perm':new_permission}, context=context)
			self.write(cr, uid, ids, {'state': 'close'}, context=context)
			cr.commit()
			raise osv.except_osv(_('Warning'),_('Employee has no available permissions '))

			return 

	def permission_draft(self, cr, uid, ids, context={}):
		return self.write(cr, uid, ids, {'state': 'draft'}, context=context)

	def onchange_select_permission(self, cr, uid, ids, employee_name, context=None):
		res = {}
		if employee_name:
			obj = self.pool.get('hr.employee').browse(cr, uid, [employee_name] , context = context)
			res['available_permission'] = obj[0].available_perm
		return {'value': res}
	def set_month_permission(self, cr, uid, ids=all, context=None):
			ids_ = self.pool.get("hr.employee").search(cr, uid, [("available_perm","<>",2)], context=context)
			for id_ in ids_ :
				self.pool.get("hr.employee").write(cr,uid ,id_ ,{"available_perm":2},context=None)		
			return
class hr_typeofpermission(osv.osv):
	_name = 'hr.typeofpermission'
	_rec_name = 'type_of_permission'
	_description = 'Type of permission'
	_columns = {
			'type_of_permission' : fields.char('Type of permission', size=50, required=True,),
		}
	_sql_constrains = [
			('type_of_permission', 'unique(type_of_permission)', 'Type of permission Must Be Unique'),
		]



