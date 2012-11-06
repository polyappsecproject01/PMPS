// This JavaScript code is generating warnings to clients regarding bad inputs
// It is only the initial step of data validation
// Does not block from sending data, just supply warnings


function validFirstName(input) {
	var getInputValue = input.form.patFirstName.value;
	validate(getInputValue, input);
}

function validLastName(input) {
	var getInputValue = input.form.patLastName.value;
	validate(getInputValue, input);
}

function validAllergies(input) {
	var getInputValue = input.form.patAllergies.value;
	validate(getInputValue, input);
}

function validICELastName(input) {
	var getInputValue = input.form.patICELastName.value;
	validate(getInputValue, input);
}

function validICEFirstName(input) {
	var getInputValue = input.form.patICEFirstName.value;
	validate(getInputValue, input);
}

function validICEPhone(input) {
	var getInputValue = input.form.patICEPhone.value;
	validate(getInputValue, input);
}

function validPCPLastName(input) {
	var getInputValue = input.form.patPCPLastName.value;
	validate(getInputValue, input);
}

function validPCPFirstName(input) {
	var getInputValue = input.form.patPCPFirstName.value;
	validate(getInputValue, input);
}

function validPCPPhone(input) {
	var getInputValue = input.form.patPCPPhone.value;
	validate(getInputValue, input);
}

function validNotes(input) {
	var getInputValue = input.form.patNotes.value;
	validate(getInputValue, input);
}

function validFirstNameCurrent(input) {
	var getInputValue = input.form.patFirstNameCurrent.value;
	validate(getInputValue, input);
}

function validLastNameCurrent(input) {
	var getInputValue = input.form.patLastNameCurrent.value;
	validate(getInputValue, input);
}

function validFirstNameNew(input) {
	var getInputValue = input.form.patFirstNameNew.value;
	validate(getInputValue, input);
}

function validLastNameNew(input) {
	var getInputValue = input.form.patLastNameNew.value;
	validate(getInputValue, input);
}


// Validate function validates data and protects againsts some common SQL injection attacks 
// Only initial validation that generate warnings, more validation will be done both on front-end and back-end.
function validate(stringInput, input) {
	var stringLowerCase = stringInput.toLowerCase();
	if ((stringLowerCase == "") || (stringLowerCase.indexOf("drop table") != -1) || (stringLowerCase.indexOf("insert into") != -1) || (stringLowerCase.indexOf("create table") != -1) || (stringLowerCase.indexOf("truncate table") != -1) || (stringLowerCase.indexOf("delete from") != -1) || (stringLowerCase.indexOf("delete * from") != -1) || (stringLowerCase.indexOf("insert into") != -1)  || (stringLowerCase.indexOf("select * from") != -1) || (stringLowerCase.indexOf("update") != -1) ) {
		input.style.borderColor="#CD2626";
	}
	else {
		input.style.borderColor="#66CD00";
	}
}