/**
 * 
 */




//console.log(a);

var i=0
var allValues = []
for (let food_name in a) {
	i +=1
	var title = food_name
	//console.log(food_name)
	let nutrient_list = a[food_name];
	//console.log(typeof nutrient_list)
	const label_list = [];
	const data_list = [];
	
	for (let nutrient in nutrient_list){
		label_list.push(nutrient)
		data_list.push(nutrient_list[nutrient])	
	}
	
	
	allValues.push(data_list)
	
	var data = [
		{
			x:label_list,
			y:data_list,
			type: 'bar'
	}];
	
	var data_pie = [
		{
			labels: label_list,
			values: data_list,
			type: 'pie'
	}];
	
	var elem = document.createElement('div');
	var div_id = "plot_" + i
	elem.setAttribute("id", div_id);
	document.body.appendChild(elem);
	
	var layout = {
		title: {
	    	text:title,
	    	font: {
	      		family: 'Courier New, monospace',
	      		size: 14
	    	},
	    xref: 'paper',
	    x: 0.05,
	  }
	}
	
	var layout_pie = {
		height: 400,
  		width: 500,
		title: {
	    	text:title,
	    	font: {
	      		family: 'Courier New, monospace',
	      		size: 14
	    	},
	    xref: 'paper',
	    x: 0.05,
	  }
	}
	
	Plotly.newPlot(elem, data_pie, layout_pie);
}
