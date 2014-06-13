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

	</style>
</head>
<body>
	<% setLang(context["lang"]) %>

	<% sci_inst_recs = _get_inst_byname(data['form']) %>
	${_('Institution Name')} : ${sci_inst_recs[0].inst_name.inst_name}<br/>
	${_('Study Years')} : ${sci_inst_recs[0].study_years}<br/>
	${_('Qualification')} : ${sci_inst_recs[0].qual_degree.qual_degree}<br/>
	<label>Departments</label>
	<br/>
	%for sci_inst in sci_inst_recs:
		
		${_('Department')} : ${sci_inst.department.dep_name}<br/>
		
	%endfor

</body>

</html>