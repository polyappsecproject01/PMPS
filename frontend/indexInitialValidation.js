function initialUserValidation(form) {
	var inputUser = form.username.value;
	var userLowerCase = inputUser.toLowerCase();
	
	if ( dataNotValid(userLowerCase)) {
		form.errUser.value = "true";
	}
	else {
		form.errUser.value = "false";
	}
}

function initialPassValidation(form) {
	var inputPass = form.password.value;
	var passLowerCase = inputPass.toLowerCase();
	
	if ( dataNotValid(passLowerCase)) {
		form.errPass.value = "true";
	}
	else {
		form.errPass.value = "false";
	}
}

function dataNotValid(stringLowerCase) {
	return ((stringLowerCase == "") || (stringLowerCase.indexOf("&") != -1) || (stringLowerCase.indexOf("'") != -1) || (stringLowerCase.indexOf('"') != -1) || (stringLowerCase.indexOf('<') != -1) || (stringLowerCase.indexOf('>') != -1) || (stringLowerCase.indexOf('script') != -1) || (stringLowerCase.indexOf('/') != -1) || (stringLowerCase.indexOf("select") != -1) || (stringLowerCase.indexOf("privileges") != -1) || (stringLowerCase.indexOf("?") != -1) || (stringLowerCase.indexOf("<?") != -1) || (stringLowerCase.indexOf("?>") != -1) || (stringLowerCase.indexOf("drop") != -1) || (stringLowerCase.indexOf("insert") != -1) || (stringLowerCase.indexOf("create") != -1) || (stringLowerCase.indexOf("truncate") != -1) || (stringLowerCase.indexOf("delete") != -1) || (stringLowerCase.indexOf("insert") != -1) || (stringLowerCase.indexOf("update") != -1) );
}
