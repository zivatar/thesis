	function handleInputChange(inputName, day, elemId) {
		handleInputChangeBefore(inputName, day, elemId);
		var value = document.getElementById(elemId).value;
		if (inputName == "snowDepth" && value == 0) {
			value = undefined;
		}
		data[day][inputName] = value == "" ? undefined : value;
		handleInputChangeAfter(inputName, day, elemId);
	}

	function handleInputChangeCheckbox(inputName, day, elemId) {
		handleInputChangeBefore(inputName, day, elemId);
		var elem = document.getElementById(elemId);
		data[day][inputName] = !!elem.checked;
		handleInputChangeAfter(inputName, day, elemId);
	}

	function handleInputChangeBefore(inputName, day, elemId) {
		if (!data[day]) {
			data[day] = {}
		}
	}

	function handleInputChangeAfter(inputName, day, elemId) {
		var empty = true;
			for (var i in data[day]) {
				if (data[day][i] != undefined) {
					empty = false;
					break;
				}
			}
			if (!!empty) {
				delete data[day];
			}
			console.log(data[day]);
	}

	function handleAddObservation(day, elemId) {
			var value = document.getElementById(elemId).value;
			if (value != -1) {
				if (!data[day]) {
					data[day] = { obs: [] }
				} else if (!data[day].obs) {
					data[day].obs = [];
				}
				if (data[day].obs.indexOf(value) == -1) {
					data[day].obs.push(value);
				}
				
				document.getElementById(elemId).value = -1;
			}
			renderLabels(day, "obsLabels"+(day+1));
	}

	function deleteLabel(day, i, button) {
	    data[day].obs.splice(i, 1);
	    button.remove();
	}

	function renderLabels(day, elemId) {
			var elem = document.getElementById(elemId);
			elem.innerHTML = '';
			if (!!data && !!data[day] && !!data[day].obs) {
				for (var i = 0; i < data[day].obs.length; i++) {
					var span = document.createElement("button");
					span.onclick = function(day, i, span) {
					    return function() {
					        deleteLabel(day, i, span);
					    }
					}(day, i, span);
	    			span.className = "inline-block btn btn-warning";
	    			span.appendChild(document.createTextNode(obsCodes[data[day].obs[i]]));
	    			elem.appendChild(span);
	    			//console.log(obsCodes);
				}
			}
			
	}