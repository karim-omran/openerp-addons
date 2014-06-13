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

	<% recs = _get_inst_byname(data['form']) %>
<table>
	${_("disability type")} ${data['form'][1]}
	%for disability in recs:
		<tr><td>${_("Name")} </td><td>${disability.name}</td></tr>
	%endfor
</table>
</body>



</html>
