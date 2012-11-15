// This JavaScript code is generating warnings to clients regarding bad inputs and clear those inputs from the form
// It is only the initial step of data validation
// Does not block from sending data, just supply warnings and clear non-valid data from field prior to submission

// valid function takes an the input html field (input), and the html placeholder area where an error warning will be issued (errorTdId)
function validFirstName(input, errorTdId) {
	var getInputValue = input.form.patFirstName.value;	
	if (!validate(getInputValue, input)) {
		input.form.patFirstName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (errorTdId == "retPatError") {
		if (AllNamesAreValid(input))
			document.getElementById(errorTdId).innerHTML = "";
	} else if (errorTdId == "modPatInfoError")
		if (AllPatInfoIsValid(input))
			document.getElementById(errorTdId).innerHTML = "";
}

function validLastName(input, errorTdId) {
	var getInputValue = input.form.patLastName.value;
	if (!validate(getInputValue, input)) {
		input.form.patLastName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllNamesAreValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}




function validAllergies(input, errorTdId) {
	var getInputValue = input.form.patAllergies.value;
	if (!validate(getInputValue, input)) {
		input.form.patAllergies.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validICELastName(input, errorTdId) {
	var getInputValue = input.form.patICELastName.value;
	if (!validate(getInputValue, input)) {
		input.form.patICELastName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validICEFirstName(input, errorTdId) {
	var getInputValue = input.form.patICEFirstName.value;
	if (!validate(getInputValue, input)) {
		input.form.patICEFirstName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validICEPhone(input, errorTdId) {
	var getInputValue = input.form.patICEPhone.value;
	if (!validate(getInputValue, input)) {
		input.form.patICEPhone.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validPCPLastName(input, errorTdId) {
	var getInputValue = input.form.patPCPLastName.value;
	if (!validate(getInputValue, input)) {
		input.form.patPCPLastName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validPCPFirstName(input, errorTdId) {
	var getInputValue = input.form.patPCPFirstName.value;
	if (!validate(getInputValue, input)) {
		input.form.patPCPFirstName.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validPCPPhone(input, errorTdId) {
	var getInputValue = input.form.patPCPPhone.value;
	if (!validate(getInputValue, input)) {
		input.form.patPCPPhone.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validNotes(input, errorTdId) {
	var getInputValue = input.form.patNotes.value;
	if (!validate(getInputValue, input)) {
		input.form.patNotes.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllPatInfoIsValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}


function validFirstNameCurrent(input, errorTdId) {
	var getInputValue = input.form.patFirstNameCurrent.value;
	if (!validate(getInputValue, input)) {
		input.form.patFirstNameCurrent.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllModNamesAreValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validLastNameCurrent(input, errorTdId) {
	var getInputValue = input.form.patLastNameCurrent.value;
	if (!validate(getInputValue, input)) {
		input.form.patLastNameCurrent.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllModNamesAreValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validFirstNameNew(input, errorTdId) {
	var getInputValue = input.form.patFirstNameNew.value;
	if (!validate(getInputValue, input)) {
		input.form.patFirstNameNew.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllModNamesAreValid(input))
		document.getElementById(errorTdId).innerHTML = "";
}

function validLastNameNew(input, errorTdId) {
	var getInputValue = input.form.patLastNameNew.value;
	if (!validate(getInputValue, input)) {
		input.form.patLastNameNew.value = "";
		document.getElementById(errorTdId).innerHTML = "Error: Non-valid input was removed."; 
	}
	if (AllModNamesAreValid(input)) 
		document.getElementById(errorTdId).innerHTML = "";
}

// check all required fields in requested form in order to remove an error warning

function AllNamesAreValid(input) {
	return ((validateNoColoring(input.form.patFirstName.value)) && (validateNoColoring(input.form.patLastName.value)))
}

function AllPatInfoIsValid(input) {
	return ( (validateNoColoring(input.form.patFirstName.value)) && (validateNoColoring(input.form.patLastName.value)) && (validateNoColoring(input.form.patAllergies.value)) && (validateNoColoring(input.form.patICELastName.value)) && (validateNoColoring(input.form.patICEFirstName.value)) && (validateNoColoring(input.form.patICEPhone.value)) && (validateNoColoring(input.form.patPCPLastName.value)) && (validateNoColoring(input.form.patPCPFirstName.value)) && (validateNoColoring(input.form.patPCPPhone.value)) && (validateNoColoring(input.form.patNotes.value))  );
}

function AllModNamesAreValid(input) {
	return ( (validateNoColoring(input.form.patFirstNameCurrent.value)) && (validateNoColoring(input.form.patLastNameCurrent.value)) && (validateNoColoring(input.form.patFirstNameNew.value)) && (validateNoColoring(input.form.patLastNameNew.value))   );
}


// Validate function validates data and protects againsts some common SQL injection attacks 
// Only initial validation that generate warnings, more validation will be done both on front-end and back-end.
// Returns false if data is not valid and colors the input border in red
// Returns true if data is valid and colors the input border in green
// 
function validate(stringInput, input) {
	var stringLowerCase = stringInput.toLowerCase();
	if (dataNotValid(stringLowerCase)) {
		input.style.borderColor="#CD2626"; // Change to border to RED
		return false;
	}
	else {
		input.style.borderColor="#66CD00"; // Change to border to GREEN
		return true;
	}
}

// Validate function validates data and protects againsts some common SQL injection attacks 
// Only initial validation that generate warnings, more validation will be done both on front-end and back-end.
// Return false if data is not valid
// Return true if data is valid
function validateNoColoring(stringInput) {
	var stringLowerCase = stringInput.toLowerCase();
	if (dataNotValid(stringLowerCase)) {
		return false;
	}
	else {
		return true;
	}
}

// Definition of non-valid data
function dataNotValid(stringLowerCase) {
	return ((stringLowerCase == "") || (stringLowerCase.indexOf("'") != -1) || (stringLowerCase.indexOf('"') != -1) || (stringLowerCase.indexOf("select") != -1) || (stringLowerCase.indexOf("privileges") != -1) || (stringLowerCase.indexOf("<?php") != -1)|| (stringLowerCase.indexOf("<?") != -1)|| (stringLowerCase.indexOf("?>") != -1) || (stringLowerCase.indexOf("drop") != -1) || (stringLowerCase.indexOf("insert") != -1) || (stringLowerCase.indexOf("create") != -1) || (stringLowerCase.indexOf("truncate") != -1) || (stringLowerCase.indexOf("delete") != -1) || (stringLowerCase.indexOf("*") != -1) || (stringLowerCase.indexOf("insert") != -1) || (stringLowerCase.indexOf("update") != -1) );
}