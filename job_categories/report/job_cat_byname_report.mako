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

	<% job_info = _get_job_byname(data['form']) %>
<table>
	<tr>
		<th>
			${_("Category Name")}
		</th>
		<th>
			${job_info.job_category}
		</th>
	</tr>
	
	<tr>
		<th>
			${_("Lower Salary Limit")}
		</th>
		<th>
			${job_info.lower_limit}
		</th>
	</tr>

	<tr>
		<th>
			${_("Upper Salary Limit")}
		</th>
		<th>
			${job_info.upper_limit}
		</th>
	</tr>
	
	<tr>
		<th>
			${_("Upper Category")}
		</th>
		<th>
			${job_info.upper_category.job_category}
		</th>
	</tr>
	
</table>

</body>

</html>
