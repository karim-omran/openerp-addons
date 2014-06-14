from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
import time

class formal_vacations(osv.osv):
	_name = 'formal.vacations'

	#_inherit = 'hr.employee'

	_columns = {

			

			'occasion_leave' : fields.many2one(
					'new.occasion',
					'Occasion',
					ondelete='set null',
					onupdate='cascade',
					required=True, # this means not null how i say  ondelete='set null and here say not null
				),

			
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

			'leave_condition' : fields.selection(
				[('fully granted', 'fully granted'), ('leaves days will decrease', 'leaves days will decrease')],
				'Leave Condition : ',
				required=True,
				),

			'deducted_days' : fields.integer(
				'Deducted Days From Employee : ',
				size=50,
				#required=True,
				),

			}

	_sql_constraints = [('rec_uniq','unique(occasion_leave,start_date,end_date,leave_condition)', 'Occasion With The Same Data Already Exist!')]



	def onchange_condition(self, cr, uid, ids, leave_condition, context=None):
        
		if leave_condition== 'whole':
			readonly='True'
	
		if leave_condition== 'part':
			readonly='False'

			return True
            
formal_vacations()

#======================================================================================


class new_occasion(osv.osv):

	_name = 'new.occasion'


	_order = 'occasion_name asc'

	_rec_name = 'occasion_name' # because it read from field called name so i told him the name of field that must read from it  , it's 		name is  occasion_name i put it in _rec_name  attribute

	_columns = {
			
			'occasion_name' : fields.char(
					'Occasion',
					size=60,
					required=True,
				),

		}

	_defaults = {
			'occasion_name' : '',
		}

	_sql_constraints = [('occa_uniq','unique(occasion_name)', 'Occasion With The Same Name Already Exist!')]


#======================================================================================

