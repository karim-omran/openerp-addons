from osv import osv, fields

class insurance(osv.osv):
		
	_name = 'hr.insurance'
	_rec_name = 'company_name'
	_columns = {
		'company_name' : fields.char('Company Name',size = 60, required = True,), 
		'employee_share' : fields.float('Employee Share',digits = (2,2), required =True,), 
		'owner_share' : fields.float('Owner Share',digits = (2,2), required = True,),
		'injury_share' : fields.float('Injury Share',digits = (2,2), required = True,),
		'aging_share' : fields.float('Aging Share',digits = (2,2), required = True,),

	}

	_sql_constraints = [('name_uniq','unique(company_name)','insurance company name With The Same Name Already Exist!')]

	def _check_shares(self, cr, uid, ids, context=None):
		record = self.browse(cr, uid, ids, context=context)
		for data in record:
			if data.employee_share < 0 or data.employee_share > 100 or data.owner_share < 0 or data.owner_share > 100 or data.injury_share < 0 or data.injury_share > 100 or data.aging_share < 0 or data.aging_share > 100:
				return False
			else :
				return True

	_constraints = [(_check_shares, 'Error : Shares Must Be Positive Number And Less Than 100!', ['employee_share', 'owner_share', 'injury_share', 'aging_share']),]

class hr_contract(osv.osv):
	_name = "hr.contract"
	_inherit = "hr.contract"
	_columns = {
		'company_name_insurance': fields.many2one('hr.insurance', 'Company Name'),
	}

hr_contract()
