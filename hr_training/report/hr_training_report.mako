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

	<h2>${get_Course_Name()}</h2>
	<table>
		
	<tr>	<th>${_("Employee Name")}</th><th>${_("Department")}</th><th>${_("Work Phone")}</th> </tr>
	
	%for emp in getEmps():
	
	<tr>	<td>${emp.name}</td><td>${emp.department_id.name}</td><td>${emp.work_phone}</td>
				</tr>
	%endfor


	</table>

</body>


</html>
