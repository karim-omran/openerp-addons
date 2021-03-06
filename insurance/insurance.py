from osv import osv, fields
import openerp
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from openerp import netsvc, tools, pooler


class insurance(osv.osv):
		
	_name = 'hr.insurance'
	_rec_name = 'company_name'
	_columns = {
		'company_name' : fields.char('Company name',size = 60, required = True,), 
		'employee_share' : fields.float('Employee share',digits = (2,2), required =True,), 
		'owner_share' : fields.float('owner_share',digits = (2,2), required = True,),
		'injury' : fields.float('injury',digits = (2,2), required = True,),
		'aging' : fields.float('aging',digits = (2,2), required = True,),

	}

	_sql_constraints = [('name_uniq','unique(company_name)','company name With The Same Name Already Exist!')]


class hr_contract(osv.osv):
	_name = "hr.contract"
	_inherit = "hr.contract"
	_columns = {
		'company_name_insurance': fields.many2one('hr.insurance', 'company name'),
	}

hr_contract()
