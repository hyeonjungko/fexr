// page elements
window.onload = () => {
  const inputField = document.querySelector('#searchbox');
  const submit = document.querySelector('#search-button');
  const responseField = document.querySelector('#rate-response');
  
  submit.addEventListener('click', displayRate);
}

const renderResponse = (res) => {
  const inputField = document.querySelector('#searchbox');
	inputField.style.cssText += "position: fixed; width: 10%; left: 4rem;";
  const submit = document.querySelector('#search-button');
	submit.style.cssText += "position: fixed; width: 10%; left: 4rem;";

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
