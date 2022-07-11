/**
 * https://www.bootstrapfriendly.com/blog/dynamically-add-or-remove-form-input-fields-using-jquery/
 */


$(document).ready(function(){
	$("#foodname_search-box_1").keyup(function(){
		$.ajax({
		url: "http://127.0.0.1:8000/search/foodname/",
		dataType: "json",
		data:'lang=fr&term='+$(this).val(),
		
			success: function(data){
				console.log(data)
				
				var eleve_str ;
				eleve_str = '<ul class="list-group" id="country-list_new">';
				
				for (let key in data) {
				  let value = data[key];
				  
				  for (food_id in value){
				  	let info=value[food_id];
				  		var food_desc = info.description;
				  		//var data_array = student_name + "_" + student_id;
						//console.log('<li class="list-group-item list-group-flush" onClick="selectSudent_new( \''+ food_id + '\', ' + food_id + ', 1)">' + food_desc +'</li>')
				  		eleve_str +=  '<li class="list-group-item list-group-flush" onClick="selectSudent_new(\''+ food_desc.replaceAll('\'', '') + '\', ' + food_id + ', 1)">'  + food_desc.replaceAll('\'', '') +'</li>';
				  } 
				}	
					
				eleve_str += '</ul>';	
				
				$("#suggesstion-box_no_1").show();
				$("#suggesstion-box_no_1").html(eleve_str);
					
			}
		});	
	});
});


function selectSudent_new(food_desc, food_id) {
	//console.log(typeof val);
	$("#foodname_id_no_1").val(food_id);
	//$('input[class="student_id"]').val(student_id);
	$("#foodname_search-box_1").val(food_desc);
	$("#suggesstion-box_no_1").hide();
}



///======Append method
$(document).ready(function(){ 
	$("body").on("click",".add_new_frm_field_btn", function (){ 
		console.log("clicked"); 
		var index = $(".form_field_outer").find(".form_field_outer_row").length + 1; 
					$(".form_field_outer").append(`
						<div class="row form_field_outer_row">
						
							 <div class="form-group col-sm-1">
				              <input type="text" class="form-control w_90" name="qty[]" id="qty_1" placeholder="Qty." />
				            </div>
				            
				            <div class="form-group col-sm-1">
				              <input type="text" class="form-control w_90" name="unit[]" id="unit_1" placeholder="Unit." />
				            </div>
						
					  		<div class="form-group col">
					    		<input type="text" class="search-box form-control" name="foodname_no[]" id="foodname_search-box_` + index + `" placeholder="Ingredient name" />
								<div class="suggesstion-box" name="suggesstion-box_no" id="suggesstion-box_no_` + index + `"></div>
								<input type="hidden"  name="student_Id_no_` + index + `" class="hidden_student_id" id="student_Id_no_` + index + `" value="N/A">
					  		</div>
						 	
						  	<div class="form-group col-md-2 add_del_btn_outer">
						    	<button class="btn_round remove_node_btn_frm_field" disabled>
						      		<i class="fas fa-trash-alt"></i>
						    	</button>
						  	</div>
					
						</div>`
					); 
		$("#foodname_search-box_" + index).keyup(function(){
		
			$.ajax({
			url: "foodname",
			dataType: "json",
			data:'term='+$(this).val(),
			
			success: function(data){
				console.log(index)
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
	
		$(".form_field_outer").find(".remove_node_btn_frm_field:not(:first)").prop("disabled", false); 
		$(".form_field_outer").find(".remove_node_btn_frm_field").first().prop("disabled", true); 
		
	}); 
});

function selectSudent(food_desc, food_id, index) {
	//console.log(typeof val);
	$("#student_Id_no_" + index).val(food_id);
	//$('input[class="student_id"]').val(student_id);
	$("#foodname_search-box_" + index).val(food_desc);
	$("#suggesstion-box_no_" + index).hide();
}

$(document).ready(function () {
  //===== delete the form fieed row
	$("body").on("click", ".remove_node_btn_frm_field", function () {
    	$(this).closest(".form_field_outer_row").remove();
    	console.log("success");
	});
});



