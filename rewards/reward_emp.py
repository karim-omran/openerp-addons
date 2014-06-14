from openerp.osv import osv
from openerp.osv import fields




class reward_emp(osv.osv):

    # name to erp
    _name = 'reward.emp'

    _order = 'reward_name asc'

    _description = 'reward types model'

    # to show in inheritance
    #_rec_name = 'field name'
    _rec_name = 'reward_name'

    _columns = {

                'reward_name' : fields.char(
                'Reward Name',
                size= 50,
                required=True,
                ),

                'reward_type' : fields.char(
                'Reward Type',
                size= 50,
                required=True,
                ),

                'reward_notes' : fields.text(
                'Notes',

                ),

    }

    _defaults = {

                'reward_name':'',
                'reward_type':'',
                'reward_notes':'',
    }

    _sql_constraints = [
        ('uniq_name','unique(reward_name,reward_type)',"A Reward with this name and type already exists")
    ]

###################################################### reward_reg ################################################################



class reward_reg(osv.osv):

    # name to erp
    _name = 'reward.reg'
    _description = "Give Employees Reward"
    _columns = {

        'employee': fields.many2one('hr.employee',
            'Employee',
            required=True,
            select=True),

        'reward_name': fields.many2one('reward.emp',
            'Reward Name',
            required=True,
            select=True),

        'date': fields.date('Date', required=True),

        'value' : fields.float('Value',
            digits = (2,2),
            required = True,),

        'status':fields.selection([('Per Month','Per Month'),('Once','Once')],
            'Status',
            required=True,
            translated=True),

        'notes' : fields.text(
            'Notes',),

        }




######################################################################################################


class hr_employee(osv.osv):

    _name = "hr.employee"
    _inherit = "hr.employee"
    _columns = {

        'employee_name_reward': fields.one2many('reward.reg',
            'employee'),

        }

hr_employee()

####################################################

class reward_employee(osv.osv):

    _name = "reward.employee"
    _inherit = "reward.emp"
    _columns = {

        'reward_for_employee': fields.one2many('reward.reg',
            'reward_name'),

        }

reward_employee()
