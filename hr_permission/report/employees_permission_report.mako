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
<% import logging %>
<%_logger = logging.getLogger(__name__)%>
<% 	_logger.info("mako 38")%>
<% setLang(context["lang"]) %>
<% 	_logger.info("mako 39")%>
</br>	
	<table>
		<tr>
			<th>${_("Employee Name")}</th>
			<th>${_("Reason")}</th>
			<th>${_("Date")}</th>
			<th>${_("Permissions")}</th>
		</tr>
		<% recs=_get_employee_permissions(data['form']) %>
		%for record in recs:
			<tr>
				<td>${record.employee_name.name}</td>
				<td>${record.type_of_permission.type_of_permission}</td>
				<td>${record.date_of_permission}</td>
				<td>${record.available_permission}/2</td>
			</tr>
		%endfor
</table>

</body>
</html>
