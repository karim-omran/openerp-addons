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
<table>
##${context.keys()}
<body>
<h2><label>${_("military_status Report")}</label></h2>
%for military_status in objects:
<tr><td>${_("Name")}</td><td>${ military_status.employee_name.name }</td></tr>
<tr><td>${_("Status")}</td><td>${ military_status.status }</td></tr>
<tr><td>${_("From")}</td><td>${ military_status.fromd }</td></tr>
<tr><td>${_("To")}</td><td>${ military_status.to }</td></tr>
<tr><td>${_("Salary")}</td><td>${ military_status.salary_status }</td></tr>

%endfor
</table>
</body>

</html>
