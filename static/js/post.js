// page elements
window.onload = () => {
  const inputField = document.querySelector('#searchbox');
  const submit = document.querySelector('#search-button');
  const responseField = document.querySelector('#rate-response');
  
  submit.addEventListener('click', displayRate);
}


/*
window.onload = () => {
	// listen for Return key
	
	// listen for search button
	document.getElementById('search-button').onclick = function(element) {
		let searched = document.getElementById('search-button').value;

		try {
			// raise error if invalid currency
			post(searched);
		} catch (e) {
			// catch invalid currencies
		}
	}
}
*/

const renderResponse = (res) => {
  const responseField = document.querySelector('#rate-response');
	if(!res){
		console.log(res.status);
	}
	if(!res.length){
		responseField.innerHTML = 'nothing returned';
	}
	responseField.innerHTML = res.rate;
	return
}

const getRate = () => {
  const inputField = document.querySelector('#searchbox');
	const currency = inputField.value
	const url = `/api/rate/${currency}`

  const xhr = new XMLHttpRequest();
	xhr.responseType = 'json';
	xhr.onreadystatechange = () => {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			renderResponse(xhr.response);
			//console.log(xhr.response);
		}
	};

	xhr.open('GET', url);
	xhr.send();
}

const displayRate = (event) => {
	event.preventDefault();
	getRate();
}

//submit.addEventListener('click', displayRate);
