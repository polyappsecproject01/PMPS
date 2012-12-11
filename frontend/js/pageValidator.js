/*
jQuery.validator.addMethod("phoneUS", function(phone_number, element) {
    phone_number = phone_number.replace(/\s+/g, ""); 
	return this.optional(element) || phone_number.length > 9 &&
		phone_number.match(/^(1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
}, "Specify a valid us phone number");


jQuery.validator.addMethod("nameStr", function(nameStr, element) {
    nameStr = nameStr.replace(/\s+/g, ""); 
	return this.optional(element) || nameStr.match(/^([A-Za-z]+)$/);
	
}, "Please enter a valid name");

var searchCacheObj={};

$.validator.setDefaults({
	submitHandler: function(form) { 
		//alert('submit.')
		form.submit();
	}
});
*/
$().ready(function() {


/*

	requiredNameChecker={
				nameStr:true,
				required: true,
				maxlength:25,				
	};
	v_rules= {
		
			patLastName: 	requiredNameChecker,		
			patFirstName : 	requiredNameChecker,
			patICELastName: requiredNameChecker,
			patICEFirstName:requiredNameChecker,
			patPCPLastName:requiredNameChecker,
			patPCPFirstName:requiredNameChecker,
			patAllergies: {required:true},			
			patPCPPhone:{
				//required:true,
				phoneUS:true
			},
			patICEPhone:{
				//required:true,
				phoneUS:true
			}
	};

	var PPINFOValidator= $("#PPINFO").validate({
		rules:v_rules
	});
	$("#PPINFO2").validate({
		rules:v_rules
	});
		$("#PPFind").validate({
		rules:{
			patLastName: 	requiredNameChecker,		
			patFirstName : 	requiredNameChecker
		}			 	
		
		}
	})

*/
//----------search/retrieve pat----------- 
	//default lock #PPINFO

	$('#PPINFO input[type="text"],#PPINFO textarea,#PPINFO select').attr('readonly','readonly');
	initReadonly();

	mBtn= $("#PPEditRegion input[name=modifyPatInfo]");
	rBtn = $("#PPEditRegion input[name=renamePatInfo]");
	if (mBtn!= undefined && rBtn!= undefined ){
	 	mBtn.click(function(){
	 		
	 		mBtn.attr("checked",true);
	 		console.log('mBtn:::'+mBtn.attr("checked") );
	 		rBtn.attr("checked",false);
	 		UpdateRadioBtn() 
	 		//$("#PPINFO").valid( );
	 	});
	 	rBtn.click(function(){
	 		
			rBtn.attr("checked",true);
			console.log('rBtn:::'+rBtn.attr("checked") );
			mBtn.attr("checked",false);
	 		UpdateRadioBtn() ;
	 		//$("#PPINFO").valid( );
	 		//PPINFOValidator.valid( );
	 	});
	}
	dBtn = $("#PPEditRegion input[name=delPatInfo]");
	if (dBtn!= undefined){
		dBtn.click(function(){
			delPatInfo();
		})
	}


	$("#PPFind").submit(function(e){		 	
		e.preventDefault() 
			$.post('retPatInfo2.php',{
				'patLastName': $('#ppfPLN').val(),
		        'patFirstName': $('#ppfPFN').val()
				}, function(respsonse) {
					console.log(respsonse);
					respData = $.parseJSON(respsonse);

					if(respData.result=="succ"){
						//data refresh -- > switch toggle 
						// fill content
						console.log('begin filling');
						fillPPINFO(respData.data);
						searchCacheObj=respData.data; // cachedata
						recoverUsingBtn();
						// pin original user name to hidden field
						// cache user profile content

					}else if(respData.result=="fail"){
						console.log('search failed');
						$('#PPFindError').html(respData.errMsg);
					}else{
						$('#PPFindError').html("Unkonw system exception!");
						console.log('error:recv wrong format data in search')
					}
//{"result":"succ","errMsg":"",
//"data":{"firstname":"Jordan","lastname":"Hill","bloodtype":"A-","allergies":"None.","ICE":{"phone":"12322121","firstname":"Lisa","lastname":"Jones"},"PCP":{"phone":"12322121","firstname":"Norah","lastname":"Joe"},"notes":"He is really crazy."}}

				  console.log(respData.data);
				}
			);
		return false;
	});
	bindValidator();

});
function initReadonly(){
	$('#PPINFO').addClass('readonlyCls');
	mBtn= $("#PPEditRegion input[name=modifyPatInfo]");
	rBtn = $("#PPEditRegion input[name=renamePatInfo]");
	dBtn = $("#PPEditRegion input[name=delPatInfo]");
	sBtn = $("#PPINFO input[type=submit]");
	if (mBtn!= undefined && mBtn)
		console.log('mbtn dis');
	 	mBtn.attr("disabled", "disabled");

	if (rBtn!= undefined && mBtn)
		 rBtn.attr("disabled", "disabled");

	if (dBtn!= undefined && mBtn)
	 	dBtn.attr("disabled", "disabled");

	if (sBtn!= undefined && mBtn)
	 	sBtn.attr("disabled", "disabled");

}
function recoverUsingBtn(){
	$('#PPINFO').removeClass('readonlyCls');
	mBtn= $("#PPEditRegion input[name=modifyPatInfo]");
	rBtn = $("#PPEditRegion input[name=renamePatInfo]");
	dBtn = $("#PPEditRegion input[name=delPatInfo]");
	sBtn = $("#PPINFO input[type=submit]");

	if (mBtn!= undefined && mBtn)
	 	mBtn.removeAttr("disabled");    
	 	mBtn.attr('checked', true); //default
	 	rBtn.attr('checked', false); //default
		UpdateRadioBtn();

	if (rBtn!= undefined && mBtn)
		 rBtn.removeAttr("disabled");  

	if (dBtn!= undefined && mBtn)
	 	dBtn.removeAttr("disabled");  
	if (sBtn!= undefined && mBtn)
	 	sBtn.removeAttr("disabled");  
}
function delPatInfo(){
	var origName = searchCacheObj.lastname +' '+ searchCacheObj.firstname;
	retVal =  confirm("Do you want to del the profile of "+origName+"?")
	if(retVal){
		fillPPINFO_Name(searchCacheObj);
		fillPPINFO_nonName(searchCacheObj);
		$("#PPINFO").attr("action", "remPat2.php");
			console.log('11---del-');
		$("#PPINFO").submit();
		
		
		
	}
	 

}
function UpdateRadioBtn(){

	mBtn= $("#PPEditRegion input[name=modifyPatInfo]");
	rBtn = $("#PPEditRegion input[name=renamePatInfo]");

	if (mBtn== undefined || rBtn== undefined )
	 	return;

	if (mBtn.attr('checked')){
		//mBtn.attr('checked',false);

		console.log('111 in toggle mBtn');
		switch2ModifyPatInfo();
	}else if( rBtn.attr('checked')){

		switch2RenamePatInfo()
		console.log('222 in toggle rBtn');
	}else{
		mBtn.attr('checked',true);
		rBtn.attr('checked',false);
		console.log('in toggle mBtn');
		switch2ModifyPatInfo();
	}

	console.log('m checked:'+mBtn.attr('checked') );

}

function switch2ModifyPatInfo(){


	sBtn = $("#PPINFO input[type=submit]");
	//sBtn.val('Submit');
	$("#PPINFO").attr("action", "modPatInfo2.php");

	recoverAndLockPPINFO_Name();// reover2OriginalName and lock it, but allow edit other fileds

}
function switch2RenamePatInfo(){
	

	sBtn = $("#PPINFO input[type=submit]");
	//sBtn.val('Submit');
	$("#PPINFO").attr("action", "modPatName2.php");
	recoverAndLockPPINFO_nonName();// reover2OriginalName and lock it, but allow edit other fileds

}

function fillPPINFO_Name(dataObj){

	$("#PPINFO input[name='patFirstName']").val(dataObj.firstname);
	$("#PPINFO input[name='patLastName']").val(dataObj.lastname);
}
function recoverAndLockPPINFO_Name(){
	console.log('lock name');
	fillPPINFO_Name(searchCacheObj);
	$("#PPINFO_nonName").css("display", "block");


	$('#PPINFO input[type="text"],#PPINFO textarea,#PPINFO select').removeAttr("readonly");

	$("#PPINFO input[name='patFirstName']").attr('readonly','readonly');
	$("#PPINFO input[name='patLastName']").attr('readonly','readonly');

}
//--------

function fillPPINFO_nonName(dataObj){
	$("#PPINFO select[name='patBloodType']").val(dataObj.bloodtype);
	$("#PPINFO textarea[name='patAllergies']").val(dataObj.allergies);

	$("#PPINFO input[name='patICELastName']").val(dataObj.ICE.lastname);
	$("#PPINFO input[name='patICEFirstName']").val(dataObj.ICE.firstname);
	$("#PPINFO input[name='patICEPhone']").val(dataObj.ICE.phone);

	$("#PPINFO input[name='patPCPLastName']").val(dataObj.PCP.lastname);
	$("#PPINFO input[name='patPCPFirstName']").val(dataObj.PCP.firstname);
	$("#PPINFO input[name='patPCPPhone']").val(dataObj.PCP.phone);

	$("#PPINFO textarea[name='patNotes']").val(dataObj.notes);
}
function recoverAndLockPPINFO_nonName(){
	console.log('lock non-name');
	fillPPINFO_nonName(searchCacheObj);
	$('#PPINFO input[type="text"],#PPINFO textarea,#PPINFO select').removeAttr("readonly");


	$("#PPINFO select[name='patBloodType']").attr('readonly','readonly');
	$("#PPINFO textarea[name='patAllergies']").attr('readonly','readonly');

	$("#PPINFO input[name='patICELastName']").attr('readonly','readonly');
	$("#PPINFO input[name='patICEFirstName']").attr('readonly','readonly');
	$("#PPINFO input[name='patICEPhone']").attr('readonly','readonly');

	$("#PPINFO input[name='patPCPLastName']").attr('readonly','readonly');
	$("#PPINFO input[name='patPCPFirstName']").attr('readonly','readonly');
	$("#PPINFO input[name='patPCPPhone']").attr('readonly','readonly');
	$("#PPINFO textarea[name='patNotes']").attr('readonly','readonly');
	$("#PPINFO_nonName").css("display", "none");

}


function fillPPINFO(dataObj){
	//$("#PPINFO input[name='patFirstName']").val('testFirstName');
	//1 
	fillPPINFO_Name(dataObj);
	fillPPINFO_nonName(dataObj);

	//for hidden elements, only fill it when user search a new pat info
	$("#PPINFO input[name='patOrigFirstName']").val(dataObj.firstname);
	$("#PPINFO input[name='patOrigLastName']").val(dataObj.lastname);
}

function bindValidator(){
	//need includeing initialVaildation.js

	//--PPFind
	$("#PPFind input[name='patFirstName']").change(function(){
		validFirstName(this,"PPFindError")
	});
	$("#PPFind input[name='patLastName']").change(function(){
		validLastName(this,"PPFindError")
	})
	
	//--PPINFO--
	$("#PPINFO input[name='patFirstName']").change(function(){
		validFirstName(this,"PPINFOError")
	});
	$("#PPINFO input[name='patLastName']").change(function(){
		validLastName(this,"PPINFOError")
	})


	$("#PPINFO input[name='patAllergies']").change(function(){
		validAllergies(this,"PPINFOError")
	})


	$("#PPINFO input[name='patICELastName']").change(function(){
		validICELastName(this,"PPINFOError")
	})
	$("#PPINFO input[name='patICEFirstName']").change(function(){	
		validICEFirstName(this,"PPINFOError")
	})
	$("#PPINFO input[name='patICEPhone']").change(function(){
		validICEPhone(this,"PPINFOError")
	})


	$("#PPINFO input[name='patPCPLastName']").change(function(){
		validPCPLastName(this,"PPINFOError")
	})
	$("#PPINFO input[name='patPCPFirstName']").change(function(){
		validPCPFirstName(this,"PPINFOError")
	})
	$("#PPINFO input[name='patPCPPhone']").change(function(){
		validPCPPhone(this,"PPINFOError")
	})

	$("#PPINFO input[name='patNotes']").change(function(){
		validNotes(this,"PPINFOError")
	})

	//---PPINFO2 
	$("#PPINFO2 input[name='patFirstName']").change(function(){
		validFirstName(this,"PPINFO2Error")
	});
	$("#PPINFO2 input[name='patLastName']").change(function(){
		validLastName(this,"PPINFO2Error")
	})


	$("#PPINFO2 input[name='patAllergies']").change(function(){
		validAllergies(this,"PPINFO2Error")
	})


	$("#PPINFO2 input[name='patICELastName']").change(function(){
		validICELastName(this,"PPINFO2Error")
	})
	$("#PPINFO2 input[name='patICEFirstName']").change(function(){	
		validICEFirstName(this,"PPINFO2Error")
	})
	$("#PPINFO2 input[name='patICEPhone']").change(function(){
		validICEPhone(this,"PPINFO2Error")
	})


	$("#PPINFO2 input[name='patPCPLastName']").change(function(){
		validPCPLastName(this,"PPINFO2Error")
	})
	$("#PPINFO2 input[name='patPCPFirstName']").change(function(){
		validPCPFirstName(this,"PPINFO2Error")
	})
	$("#PPINFO2 input[name='patPCPPhone']").change(function(){
		validPCPPhone(this,"PPINFO2Error")
	})

	$("#PPINFO2 input[name='patNotes']").change(function(){
		validNotes(this,"PPINFO2Error")
	})

	//---UINFO
	$("#UINFO input[name='userAccountName']").change(function(){
		validUserAccountName(this,"UINFOError")
		console.log('run uacc name checker1 ');
	})
	$("#UINFO2 input[name='userAccountName']").change(function(){
		validUserAccountName(this,"UINFO2Error")
	})

}
