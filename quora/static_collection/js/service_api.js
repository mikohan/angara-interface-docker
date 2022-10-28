

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var CSRF_TOKEN = getCookie('csrftoken');
//import { CSRF_TOKEN } from './api.token';


async function getJSON(response) {
    if (response.status === 400) {
        return false
    }
    if (response.status === 204) return '';
    return response.json();
}

function apiService(endpoint, method, data, type = 'json') {
    let headers = {};
    if (type == 'file') {

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFTOKEN': CSRF_TOKEN,
        },
            body = data;

    }
    else {
        headers = {
            'content-type': 'application/json',
            'X-CSRFTOKEN': CSRF_TOKEN
        },
            body = data !== undefined ? JSON.stringify(data) : null;
    }

    const config = {
        method: method || 'GET',
        body: body,
        headers: headers
    }
    return fetch(endpoint, config)
        .then(getJSON)
        .catch(error =>  {
            console.log(error);
            
        });
}


function fetchUploadImageApi(endpoint, form_data) {
    headers = {
        'X-CSRFTOKEN': CSRF_TOKEN
    }
    const config = {
        method: 'POST',
        body: form_data,
        headers: headers
    }

    fetch(endpoint, config)
        .then(response => response.json())
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.error(error)
        })
}

function axiosUploadImageApi(endpoint, form_data) {
    return axios.post(endpoint, form_data, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFTOKEN': CSRF_TOKEN
        }
    }).catch(err => {
        console.log(err);
        return false;
    })
}