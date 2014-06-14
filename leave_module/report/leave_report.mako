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
	
<pre>
	<label> Formal Leaves Report ::: </label> 
	<!--%for leave in leave_recs: -->

			<p> ********************** Formal Leaves ******************************** </p>
			<% setLang(context["lang"]) %>

			%for leave in _get_leave_byear(data['form']):
	
			${_('formal vacation ')} : ${leave.occasion_leave.occasion_name} 
			${_('the condition of the vacation ')} : ${leave.leave_condition}
			${_('from day ')} : ${leave.start_date}
			${_('to day ')} :  ${leave.end_date}
			${_('deducted days ')} :  ${leave.deducted_days}
			
			%endfor

		       <p> ************************** Formal Leaves ***************************** </p>
	<!-- %endfor -->


</pre>

</body>

</html>
