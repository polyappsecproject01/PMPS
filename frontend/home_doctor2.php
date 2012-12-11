
<?php
require_once('./validation2.php');

session_start();
sessionAuthenticateDoctor();

?>



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>Patient Medical Profile System - EMT View</title> 
<script type="text/javascript" src="initialValidation.js"></script>


<script type="text/javascript" src="js/jq18min.js"></script>
<!-- script type="text/javascript" src="js/jquery.validate.js"></script-->
<script type="text/javascript" src="js/pageValidator.js"></script>

<link href='https://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>

<link rel="stylesheet" href="css/reset.css" />
<link rel="stylesheet" href="style.css" />
<link rel="stylesheet" href="css/style2.css" />

</head> 
<body> 
<div id="container">
	<header>
    	<img id="logoPic" src="logo_pmpsc.png" onmouseover="this.src='logo_pmpsc_on.png';" onmouseout="this.src='logo_pmpsc.png'"/><br /><br />
	</header>
	<div id="userView">
        
   		<form method="POST" action="logout2.php">
        <h3>Status:</h3>
  
        <h4><?php  if (isset($_SESSION["username"])) echo "Logged in as <b>".$_SESSION["username"]."</b>";  ?></h4>

        <input type="submit" value="Logout">

        </form>
        <hr>
<!-- Patient Info section begin -->
        <div id="containerView" >
            <div id="PatientSection" class="container ">
                <div id="PatientSectionLeft" class="left">
                    <div class='subTitle'><h3>#1> Manage Patient Profile:</h3></div>
                    <div class='subTitle'><h3>Retrieve Patient Profile:</h3></div>
                    <form id="PPFind" method="POST" action="retPatInfo2.php">
                        <table>
                    
                            <tr>
                                <td class='txtlabel'>
                                    <div> First Name:</div>
                                </td>
                                <td>
                                    <div><input type="text" maxlength="25" id="ppfPFN" name="patFirstName" /></div>
                                </td>           
                            </tr> 
                             <tr>
                                <td class='txtlabel'>
                                    <div> Last Name:</div>
                                </td>
                                <td>
                                     <div><input type="text" maxlength="25" id="ppfPLN" name="patLastName"  /></div>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <input type="submit" value="Retrieve" >
                                </td>
                                <td>
                                    <span id="PPFindError"></span>
                                </td>
                            </tr>
                        </table>
                    </form>

                    <br />
                    <div id="PPEditRegion">
                        
                        <div ><div class="preopList"><h3>Medical Profile<h3></div><div class="opList"></div>
                        </div>
                        <hr>
                        <form id="PPINFO" Method="POST">
                            <table >
                                <tr>        
                                    <td id='patFirstNameLabel' class='txtlabel'>First Name:</td>
                                    <td> <input type="text" maxlength="25" name="patFirstName" />
                                         <input type="hidden" maxlength="25" name="patOrigFirstName"  />
                                    </td>
                                </tr>
                                <tr>
                                    <td id='patLastNameLabel' class='txtlabel'>Last Name:</td>
                                    <td><input type="text" maxlength="25" name="patLastName"  />
                                        <input type="hidden" maxlength="25" name="patOrigLastName"  />
                                    </td>
                                </tr>
                            </table >
                            <table id="PPINFO-nonName">
                                
                                <tr>
                                    <td class='txtlabel'> Blood Type:</td>                
                                    <td> <select name="patBloodType">
                                            <option value="O+">O+</option>
                                            <option value="O-">O-</option>
                                            <option value="A+">A+</option>
                                            <option value="A-">A-</option>
                                            <option value="B+">B+</option>
                                            <option value="B-">B-</option>
                                            <option value="AB+">AB+</option>
                                            <option value="AB-">AB-</option>
                                     </select>
                                     </td>
                                </tr>

                                <tr>  
                                    <td class='txtlabel'>Allergies:</td>   
                                    <td>
                                        <textarea type="text" name="patAllergies" maxlength="500" cols="16" rows="3"  /></textarea>
                                    </td>
                                </tr>
                                
                                 <tr>  
                                    <td class='txtlabel'>ICELastName:</td>  
                                    <td><input type="text" maxlength="25" name="patICELastName"  />
                                    </td>
                                </tr>

                                <tr>  
                                    <td class='txtlabel'>ICEFirstName:</td>  
                                    <td><input  type="text" maxlength="25" name="patICEFirstName"  />  
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td class='txtlabel'>ICEPhone:</td>  
                                    <td><input  type="text" name="patICEPhone" />
                                    </td>
                                </tr>

                               <tr>
                                    <td class='txtlabel'>PCPLastName:</td>  
                                    <td><input  type="text" maxlength="25" name="patPCPLastName"  />
                                    </td>
                                <tr>

                                <tr>
                                     <td class='txtlabel'>PCPFirstName:</td>  
                                     <td><input type="text" maxlength="25" name="patPCPFirstName" />
                                    </td>
                                </tr>

                                <tr>
                                     <td class='txtlabel'>PCPPhone:</td>  
                                     <td><input type="text" maxlength="16" name="patPCPPhone" />
                                    </td>
                                </tr>
                                <tr>
                                    <td class='txtlabel'>
                                    <h5>Notes:</h5>
                                    <td>
                                        <textarea name="patNotes" maxlength="500" cols="40" rows="3" ></textarea>
                                    </td>
                                 
                                </tr>     
                            </table>
                      
                            <table>
                                <tr>
                                    <td >
                                        <input type='submit' value="Submit">
                                    </td>
                                    <td>
                                        <span id="PPINFOError"></span>
                                    </td>
                                    
                                </tr>   
                            </table>
                            
                        
                        </form>              
                    </div>                
                </div>

                <div id="PatientSectionRight" class="right">

                    <div id="PPEmpty"> </div>
                    <div class='subTitle'><h3>Add Patient Profile:</h3></div>
                    <br />
                    <div id="PPNewRegion">
                        <h3>Medical Profile</h3>
                        <hr>
                        <form id="PPINFO2" action="addPat2.php" method="POST">
                            <table >
                                <tr>        
                                    <td class='txtlabel'>First Name:</td>
                                    <td> <input type="text" maxlength="25" name="patFirstName" />
                                         <input type="hidden" maxlength="25" name="patOrigFirstName"  />
                                    </td>
                                </tr>

                                <tr>
                                    <td class='txtlabel'>Last Name:</td>
                                    <td><input type="text" maxlength="25" name="patLastName"  />
                                        <input type="hidden" maxlength="25" name="patOrigLastName"  />
                                    </td>
                                </tr>


                                
                                <tr>
                                    <td class='txtlabel'> Blood Type:</td>                
                                    <td> <select name="patBloodType">
                                            <option value="O+">O+</option>
                                            <option value="O-">O-</option>
                                            <option value="A+">A+</option>
                                            <option value="A-">A-</option>
                                            <option value="B+">B+</option>
                                            <option value="B-">B-</option>
                                            <option value="AB+">AB+</option>
                                            <option value="AB-">AB-</option>
                                     </select>
                                     </td>
                                </tr>

                                <tr>  
                                    <td class='txtlabel'>Allergies:</td>   
                                    <td>
                                        <textarea type="text" name="patAllergies" maxlength="500" cols="16" rows="3"  /></textarea>
                                    </td>
                                </tr>
                                
                                 <tr>  
                                    <td class='txtlabel'>ICELastName:</td>  
                                    <td><input type="text" maxlength="25" name="patICELastName"  />
                                    </td>
                                </tr>

                                <tr>  
                                    <td class='txtlabel'>ICEFirstName:</td>  
                                    <td><input  type="text" maxlength="25" name="patICEFirstName"  />  
                                    </td>
                                </tr>
                                
                                <tr>
                                    <td class='txtlabel'>ICEPhone:</td>  
                                    <td><input  type="text" name="patICEPhone" />
                                    </td>
                                </tr>

                               <tr>
                                    <td class='txtlabel'>PCPLastName:</td>  
                                    <td><input  type="text" maxlength="25" name="patPCPLastName"  />
                                    </td>
                                <tr>

                                <tr>
                                     <td class='txtlabel'>PCPFirstName:</td>  
                                     <td><input type="text" maxlength="25" name="patPCPFirstName" />
                                    </td>
                                </tr>

                                <tr>
                                     <td class='txtlabel'>PCPPhone:</td>  
                                     <td><input type="text" maxlength="16" name="patPCPPhone" />
                                    </td>
                                </tr>
                                <tr>
                                    <td class='txtlabel'>
                                    <h5>Notes:</h5>
                                    <td>
                                        <textarea name="patNotes" maxlength="500" cols="40" rows="3" ></textarea>
                                    </td>
                                    </td>
                                </tr>   
                            </table>
                             
                            <table>
                                <tr>
                                    <td >
                                        <input type='submit' value="Add">
                                    </td>
                                    <td>
                                        <span id="PPINFO2Error"></span>
                                    </td>
                                    
                                </tr>   
                            </table>

                            
                        </form>

                     
                    </div>

                </div>

            </div >
      

        <!-- PatientSection end -->

      

        </div>
       <!-- containerview end-->
    </div>
     <!-- userView end-->
</div>
<!-- container end-->
<hr>
    <footer>
    <p>Copyright © Team PMPS</p>
    </footer>

</body> 
</html> 