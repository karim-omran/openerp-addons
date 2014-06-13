from osv import osv, fields
import openerp
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from openerp import netsvc, tools, pooler


class military_status(osv.osv):
		
	_name = 'hr.military.status'
	_rec_name = 'status'
	_columns = {
		'employee_name' : fields.many2one(
				'hr.employee',
				'Employee name',
				required = True,), 
		
		'status' : fields.selection(
				[('postpone','Postpone'),
				('exepmted','Exepmted'),
				('temp_exeption','Temp Exeption')],
				'Status',required=True),
				
		'fromd' : fields.date('From', ),
		'to' : fields.date('To', ),
		'salary_status' : fields.boolean('Salary status'),
	}
	
	_sql_constraints = [('name_uniq','unique(employee_name)','Employee Status With The Same Data Already Exist!')]


