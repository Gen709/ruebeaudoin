/**
 * 
 */

$(document).ready(function(){
	$("body").on("click", ".remove-grocery-item-section", function(){
		$('.add_new_frm_field_btn').prop('disabled', false);
		console.log("remove shit"); 
		$(".grocery-item-section").empty();
	});
});



$(document).ready(function(){
	$("body").on("click", ".add_new_frm_field_btn", function(){
		
		console.log($(this).attr("id")); 
		
		// get the grocery store id
		let goccery_store_id = $(this).attr("id")
		// dissable the buttons
		
		console.log("Disable Buttons");
		// button id
		$('.add_new_frm_field_btn').prop('disabled', true);
		
		
		$(".test-class").append(`<div class="row grocery-item-section">
									<div class="col">
										<input type="hidden" class="form-control" value="`+ goccery_store_id +`" name="grocerystore_id">
										
										<div class="col-md">
											<!-- food name -->
											<label for="foodname" class="form-label">Item</label>
											<input type="text" class="form-control" placeholder="" name="food_name" id="food_name">
											<input type="hidden"  name="food_name_id" id="food_name_id" value="N/A">
											<div name="food_name_suggestion_box" class="suggestion_box" id="food_name_suggestion_box"></div>
										</div>
										
										<div class="col-md">
											<!-- price -->
											<label for="price" class="form-label">Prix</label>
											<input type="text" class="form-control" placeholder="" name="price">
										</div>
										
										<div class="col-md">
											<!-- qty -->
											<label for="qty" class="form-label">Qty.</label>
											<input type="text" class="form-control" placeholder="" name="qty">
										</div>
										
										<div class="col">
											<button type="submit" class="btn btn-success">Ajouter</button>
											<button type="button" class="btn btn-danger remove-grocery-item-section">Annuler</button>
										</div>
										
									</div>
								</div>
								`);
								
	$("#food_name").keyup(function(){
		console.log("keyup")
		$.ajax({
		url:  "http://127.0.0.1:8000/canadiannutrientfile/search/foodname/",
		dataType: "json",
		data:'lang=fr&term='+$(this).val(),
		
			success: function(data){
				console.log(data)
				
				var eleve_str;
				eleve_str = '<ul class="list-group" id="country-list_new">';
				
				for (let key in data) {
				  let value = data[key];
				  
				  for (food_id in value){
				  	let info=value[food_id];
				  		var food_desc = info.description;
				  		//var data_array = student_name + "_" + student_id;
						//console.log('<li class="list-group-item list-group-flush" onClick="selectSudent_new( \''+ food_id + '\', ' + food_id + ', 1)">' + food_desc +'</li>')
				  		eleve_str +=  '<li class="list-group-item list-group-flush" onClick="selectFoodName(\''+ food_desc.replaceAll('\'', '').replaceAll('"', '') + '\', ' + food_id + ', 1)">'  + food_desc.replaceAll('\'', '') +'</li>';
				  } 
				}	
					
				eleve_str += '</ul>';	
				
				$("#food_name_suggestion_box").show();
				$("#food_name_suggestion_box").html(eleve_str);
					
			}
		});	
	});
	
	//$("#food_name").focusout(function() {
    ///	$("#food_name_suggestion_box").hide();
  	//});

	function selectFoodName(food_desc, food_id) {
		//console.log(typeof val);
		$("#food_name_id").val(food_id);
		//$('input[class="student_id"]').val(student_id);
		$("#food_name").val(food_desc);
		$("#food_name_suggestion_box").hide();
	};
								
								
	});
	
});


