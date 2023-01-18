/**
 * 
 */

$(document).ready(function(){
	$("body").on("click", ".remove-grocery-item-section", function(){
		$('.add_new_frm_field_btn').prop('disabled', false);
		$(".grocery-item-section").empty();
	});
});



$(document).ready(function(){

	$("body").on("click", ".add_new_frm_field_btn", function(){
		// get the grocery store id
		let goccery_store_id = $(this).attr("id")
		// button id
		$('.add_new_frm_field_btn').prop('disabled', true);
		
		$(".test-class").append(`<div class="grocery-item-section">
									<input type="hidden" name="store" id="id_store" value="` + goccery_store_id + `">
									
									<div class="mb-3">
										<label class="form-label" for="id_food_name">Food name</label>
										<input name="food_name_id" class="form-control" required="" id="food_name">
										<input type="hidden" name="food_name" id="id_food_name" value="N/A">
										<div name="food_name_suggestion_box" class="suggestion_box" id="food_name_suggestion_box"></div>
									</div>
									
									<div class="mb-3">
										<label class="form-label" for="id_price">Price</label>
										<input type="number" name="price" step="0.01" class="form-control" placeholder="Price" required="" id="id_price">
									</div>
									
									<div class="mb-3">
										<label class="form-label" for="id_unit">Unit</label>
										<input type="text" name="unit" maxlength="25" class="form-control" placeholder="Unit" id="id_unit">
									</div>

									<div class="mb-3">
										<label class="form-label" for="id_qty">Qty</label>
										<input type="number" name="qty" step="0.01" class="form-control" placeholder="Qty" required="" id="id_qty">
									</div>
									
									<input type="hidden" name="status" id="id_status" value="1">

									<div class="col">
										<button type="submit" class="btn btn-success">Ajouter</button>
										<button type="button" class="btn btn-secondary remove-grocery-item-section">Annuler</button>
									</div>
								</div>
								`);
								
		$("#food_name").keyup(function(){
			// console.log("keyup")
			$.ajax({
			url:  "http://127.0.0.1:8000/canadiannutrientfile/search/foodname/",
			dataType: "json",
			data:'lang=fr&term='+$(this).val(),
			
				success: function(data){
					// console.log(data)
					
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
	
		function selectFoodName(food_desc, food_id) {
			console.log("clicked");
			$("#id_food_name").val(food_id);
			//$('input[class="student_id"]').val(student_id);
			$("#food_name").val(food_desc);
			$("#food_name_suggestion_box").hide();
		};
															
	});

	$("input").on("input", function(){
		var fieldName_itemId = $( this ).attr("id");
		var value1 = $( this ).val();
		var myContent = {fieldName_itemId: fieldName_itemId,
						 value: value1
						};
		
		if (fieldName_itemId.split("_")[0] != "isSold"){
			$.ajax({
				method: "POST",
				url: "http://127.0.0.1:8000/grocerylist/wishlist/update/",
				dataType: "json",
				data:myContent,
					success: function(data){
						console.log("sucess")		
					}
			});	
		};
		
		
		

	});
	// $( "input" ).focus(function() {
	// 	console.log($( this ).attr("id"));
		
	// }).focusout(function() {
	// 	// console.log($( this ).attr("value"));
	// 	var fieldName_itemId = $( this ).attr("id");
	// 	var value1 = $( this ).attr("value");
	// 	var myContent = {fieldName_itemId: fieldName_itemId,
	// 					 value: value1
	// 					};
	// 	console.log( myContent );
		
	// });
});