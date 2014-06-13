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
##${context.keys()}
<body>
<h2>${_("insurance Report")}</h2>
<table>
%for insurance in objects:

<tr><td>${_("Name")}</td><td>${ insurance.company_name }</td></tr>
<tr><td>${_("Employee Share")}</td><td>${ insurance.employee_share }</td></tr>
<tr><td>${_("Owner Share")}</td><td>${ insurance.owner_share }</td></tr>
<tr><td>${_("Aging Share")}</td><td>${ insurance.aging }</td></tr>

%endfor
</table>
</body>

</html>
