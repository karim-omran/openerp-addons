<html>
<head>

	<style type='text/css'>
	${css}

	html,body{

		text-align:right;

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
<% setLang(context["lang"]) %>
##${context.keys()}
<body>
%for reward in objects:
<h2>${_("Reward Report")}</h2>

<label>${_("Reward Name :")}</label><div class="var">${ reward.reward_name }</div><br>
<label>${_("Reward Type :")}</label><div class="var">${ reward.reward_type } </div><br>
<label>${_("Notes :")}</label><div class="var">${ reward.reward_notes }</div><br>

%endfor

</body>

</html>
