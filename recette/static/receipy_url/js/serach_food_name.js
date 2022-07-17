/**
 * 
 */

$(document).ready(function(){ 
 	$("input[type=text]").focus(function(){
		var lang = $('html')[0].lang
		var input_text_id = $(this).attr('id');
		var first_letter = input_text_id.charAt(0)
		var index = input_text_id.substring(input_text_id.indexOf("_")+1)
		//console.log(first_letter);
		if (first_letter == "I"){
			//console.log("First letter is I");
			//console.log("Input text name is " + input_text_id);
			//console.log("Input index is " + index);
			$('#Ingredient_' + index).keyup(function(){
				//console.log("key up success");
				console.log($(this).val())
				$.ajax({
					url: "http://127.0.0.1:8000/canadiannutrientfile/search/foodname/",
					dataType: "json",
					data:'lang='+lang+'&term='+$(this).val(),
					success: function(data){
						var eleve_str;
						eleve_str = '<ul class="list-group" id="country-list">';
						
						for (let key in data) {
						  let value = data[key];
						  
							for (food_id in value){
						  		let info=value[food_id];
							  		var food_desc = info.description;
							  		//var data_array = student_name + "_" + student_id;
									//console.log('<li class="list-group-item list-group-flush" onClick="selectSudent(\''+ student_name + '\',' + student_id + ',' + index + ')"> ' + info.nom + ' - '+ info.prénom + ' gr2. '+ info.groupe +'</li>')
							  		eleve_str +=  '<li class="list-group-item list-group-flush" onClick="selectSudent(\''+ food_desc.replaceAll('\'', '') + '\', ' + food_id + ', ' + index + ')">'  + food_desc.replaceAll('\'', '') +'</li>';
							} 
						}	
							
						eleve_str += '</ul>';	
						
						$("#suggesstion-box_no_" + index).show();
						$("#suggesstion-box_no_" + index).html(eleve_str);
						}
				});
			});
			
		}
		else {
			console.log("First letter is NOT I");
		}
		
	});
});


function selectSudent(food_desc, food_id, index) {
	var lang = $('html')[0].lang
	console.log("Element selected, the id is: " + food_id);
	$("#Ingredient_id_" + index).val(food_id);
	//$('input[class="student_id"]').val(student_id);
	$('#Ingredient_' + index).val(food_desc);
	$("#suggesstion-box_no_" + index).hide();
	$("#conversion_factor_multiple_choice_box_" + index).hide(); // this is not working
	// get the conversion factors choices from the db associated with that food_name
	$.ajax({
		url:"http://127.0.0.1:8000/canadiannutrientfile/search/conversionfactors/",
		datatype:"json",
		data:'lang=' + lang + '&foodnameid=' + food_id,
		success: function(data){
			var conversion_factor = `<label for="formGroupExampleInput" class="form-label"><b><small>Conversion Factors</small></b></label>` 
			
			
			for (let key in data){
				let value = data[key]
				for (cf_id in value){
					
					//console.log(value[cf_id].description) // this is not good when one food apears more than once in a recipy -- either add same food qty or change the way the id and name are set
					conversion_factor +=`<div class="form-check"> 
  											<input class="form-check-input" type="radio" name="convertion_factor_`+ index +`" id=convertion_factor_"`+ index +`" value="`+ cf_id +`">
  												<label class="form-check-label" for="flexRadioDefault1">`+
    												 value[cf_id].description
  												+`</label>
										</div>`
				}
				
				
			}
			$("#conversion_factor_multiple_choice_box_" + index).show();
			$("#conversion_factor_multiple_choice_box_" + index).html(conversion_factor);
			
			//index_2 +=1
		}
	});
	// show box with select choice when  
	
	
}
