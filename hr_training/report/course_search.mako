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

	<h2>${_("Courses")}</h2>
	<table>
		
	<tr>	<th>${_("Course")}</th><th>${_("From")}</th><th>${_("To")}</th> </tr>
	
	%for course in get_Course(data["form"]):
	
	<tr>	<td>${course.name}</td><td>${course.from_date}</td><td>${course.to_date}</td>
				</tr>
	%endfor


	</table>

</body>


</html>
