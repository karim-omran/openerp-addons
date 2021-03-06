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
	table,th,td
	{
		border:1px solid black;
		border-collapse:collapse
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
	</br>	
	<table>
		<tr>
			<th>${_("Employee Name")}</th>
			<th>${_("Reason")}</th>
			<th>${_("Date")}</th>
			<th>${_("Permissions")}</th>
		</tr>
		<tr>
			<td>${record.employee_name.name}</td>
			<td>${record.type_of_permission.type_of_permission}</td>
			<td>${record.date_of_permission}</td>
			<td>${record.available_permission}/2</td>
		</tr>
	</table>
	%endfor
</body>
</html>
