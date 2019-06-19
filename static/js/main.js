
window.onload = () => {
  const inputField = document.querySelector('#searchbox');
  const submit = document.querySelector('#search-button');
  const responseField = document.querySelector('#rate-response');
  
  submit.addEventListener('click', displayRate);
}

const renderResponse = (res) => {
	const sSearch = document.querySelector('#section-search');
  const responseField = document.querySelector('#rate-response');
  const sResponse = document.querySelector('.section-results');
	const diver = document.querySelector('#divider');

	//sResponse.insertBefore(sSearch, divider); 
	//sSearch.classList.remove("nav");

	if(!res){
		console.log(res.status);
	}
	if(!res.length){
		responseField.innerHTML = 'no rate returned';
	}
	responseField.innerHTML = res.rate;
	return
}

const getRate = () => {
  const inputField = document.querySelector('#searchbox');
	const currency = inputField.value.toUpperCase();
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

