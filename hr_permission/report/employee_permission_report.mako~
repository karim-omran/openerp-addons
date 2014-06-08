<html>
<head>

	<style type='text/css'>

	html,body{

		%if context["lang"] == "ar_SY":
			direction: rtl;
		%endif
	}

	label{

		width:140px;
		display:inline-block;
		clear:both;
		float:right;

	}
	.var{
		
		display:inline-block;


	}

	</style>
</head>
<body>
	<% setLang(context["lang"]) %>

	<% recs = _get_permissions_of_month(data['form']) %>
  %for record in recs:
		${_('Employee Name')} : ${record.employee_name.name}<br/>
		${_('Reason')} : ${record.type_of_permission.type_of_permission}<br/>
		${_('Date')} : ${record.date_of_permission}<br/>
		${_('Permissions')} : ${record.available_permission}<br/>
		
	%endfor

</body>

</html>
