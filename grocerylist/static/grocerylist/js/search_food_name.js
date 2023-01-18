$(document).ready(function(){
	$("#food_name").keyup(function(){
		// console.log("keyup")
		$.ajax({
		
		url: "http://127.0.0.1:8000/canadiannutrientfile/search/foodname/",
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
				  		eleve_str +=  '<li class="list-group-item list-group-flush" onClick="selectFoodName(\''+ food_desc.replaceAll('\'', '') + '\', ' + food_id + ', 1)">'  + food_desc.replaceAll('\'', '') +'</li>';
				  } 
				}	
					
				eleve_str += '</ul>';	
				
				$("#food_name_suggestion_box").show();
				$("#food_name_suggestion_box").html(eleve_str);
					
			}
		});	
	});
});

function selectFoodName(food_desc, food_id) {
	console.log("clicked");
	$("#id_food_name").val(food_id);
	//$('input[class="student_id"]').val(student_id);
	$("#food_name").val(food_desc);
	$("#food_name_suggestion_box").hide();
}