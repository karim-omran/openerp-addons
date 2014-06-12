<html>
<head>
	<style type="text/css">
	
	${css}

	html,body{

	%if context["lang"] == "ar_SY":
		direction: rtl;
	%endif

	}

	table, td, th{
	
	border: 1px solid black;

	}	

	td{
		padding:5px;
	}

	th{

		padding:10px;

	}

	tr:nth-child(even) { background:#CCC; }
	tr:nth-child(odd) { background:#FFF; }	


	</style>
</head>
<body>
	<% setLang(context["lang"]) %>
	<% actions = get_actions(data['form']) %>
	<H1> ${_('Employee Name')}:${actions[0].employee_id.name}</H1><br/>
	
	<table>
	<tr><th>${_('Infraction')}</th><th>${_('Action')}</th></tr>
	
	%for action in actions:
	<tr>
	 <td>${action.infraction_id.category_id.name}</td>
	 <td>${action.type}</td>
	</tr>
	%endfor
	
	</table>
</body>

</html>