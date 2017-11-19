function handleInputChange(inputName, day, elemId) {
			var value = document.getElementById(elemId).value;
			if (!data[day]) {
				data[day] = {}
			}
			switch (inputName) {
				case "Tmax":
					data[day].Tmax = value == "" ? undefined : value;
					break;
				case "Tmin":
					data[day].Tmin = value == "" ? undefined : value;
					break;
				case "prec":
					data[day].prec = value == "" ? undefined : value;
					break;
			}
			if (data[day].Tmin == undefined && data[day].Tmax == undefined && data[day].prec == undefined) {
				data[day] = null;
			}
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

	function renderLabels(day, elemId) {
			var elem = document.getElementById(elemId);
			elem.innerHTML = '';
			if (!!data && !!data[day] && !!data[day].obs) {
				for (var i = 0; i < data[day].obs.length; i++) {
					var span = document.createElement("span");
	    			span.className = "label label-info inline-block";
	    			span.appendChild(document.createTextNode(obsCodes[data[day].obs[i]]));
	    			elem.appendChild(span);
	    			//console.log(obsCodes);
				}
			}
			
	}