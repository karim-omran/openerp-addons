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
	
	table, th, th{
	
	border: 1px solid black;

	}	

	th{
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

	<% outside_work_recs = _get_outside_work_by_name(data['form']) %>
	
	</br>
	<table>
		<tr>
			<th>${_("Employee")}</th>
			<th>${_("Outside Work Type")}</th>
		</tr>
		%for outside_work in outside_work_recs:
		<tr>
			<th>${outside_work.employee.name}</th>
			<th>${outside_work.outside_work_type.type}</th>
		</tr>
	</table>
	%endfor
</body>


</html>
