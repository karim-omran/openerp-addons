from osv import osv, fields
class res_company(osv.osv):
	_name = 'res.company'
	_inherit = 'res.company'
	_columns = {
							'day_late' : fields.float('Day_late'),
							'max_late' : fields.float('Max_late'),
							'month_late' : fields.float('Month_late'),
							'number_of_permissions' : fields.integer('Number of permissions'),
}


