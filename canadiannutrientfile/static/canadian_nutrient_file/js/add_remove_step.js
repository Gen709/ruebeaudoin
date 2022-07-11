/**
 * https://www.bootstrapfriendly.com/blog/dynamically-add-or-remove-form-input-fields-using-jquery/
 */



///======Append method
$(document).ready(function(){ 
	$("body").on("click",".add_new_step_field_btn", function (){ 
		console.log("clicked"); 
		var index = $(".form_field_outer_step").find(".form_field_outer_row_step").length + 1; 
					$(".form_field_outer_step").append(`
						<div class="row form_field_outer_row_step">
					  		<div class="form-group col">
					    		<textarea class="text-box form-control" name="step_no[]" id="step_search-box_` + index + `" placeholder="Enter step"></textarea>
					  		</div>
						 	
						  	<div class="form-group col-md-2 add_del_btn_outer">
						    	<button class="btn_round remove_node_btn_frm_field_step" disabled>
						      		<i class="fas fa-trash-alt"></i>
						    	</button>
						  	</div>
					
						</div>`
					); 
	
		$(".form_field_outer_step").find(".remove_node_btn_frm_field_step:not(:first)").prop("disabled", false); 
		$(".form_field_outer_step").find(".remove_node_btn_frm_field_step").first().prop("disabled", true); 
		
	}); 
});


$(document).ready(function () {
  //===== delete the form fieed row
	$("body").on("click", ".remove_node_btn_frm_field_step", function () {
    	$(this).closest(".form_field_outer_row_step").remove();
    	console.log("success");
	});
});



