function sendDataToServer(endPoint, siteId, data, isLastPart, onload) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", API_URL + endPoint, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
  var sendData = { 
    site: siteId,
    data: data,
  };
  if (isLastPart) {
    sendData.isLastPart = true;
  }
  if (!!onload && typeof onload == "function") {
    xhr.onload = function() {
      onload();
    }
  }
  xhr.send(JSON.stringify(sendData));
  
}

// https://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function isUnique(arr) {
  var arrUnique = arr.filter(function(item, pos) {
    return arr.indexOf(item) == pos;
  })
  return arr.length == arrUnique.length;
}

// http://geniuscarrier.com/copy-object-in-javascript/
function shallowCopy(oldObj) {
    var newObj = {};
    for(var i in oldObj) {
        if(oldObj.hasOwnProperty(i)) {
            newObj[i] = oldObj[i];
        }
    }
    return newObj;
}

function isPositiveNumeric(event) {
    return event.keyCode >= 48 && event.keyCode <= 57 || event.code == "Period";
}