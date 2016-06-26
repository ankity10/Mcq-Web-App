// global variables;

var cur_que = window.location.pathname.split('/')[2];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('.next').click(function(evt) {

// console.log("inside submition");

var csrftoken = getCookie('csrftoken');
// console.log(csrftoken);

formData = {
	'cq' : cur_que,
	'type' : 'next',

}

$.ajax({
       type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/q_submit/', // the url where we want to POST
            data: formData, // our data object
            dataType: 'json', // what type of data do we expect back from the server
            encode: true,
            headers: {"X-CSRFToken":csrftoken}

})

.done(function(data){
console.log(data);

}).fail(function(data){
	console.log(data);
})
console.log("submition finished");

// alert("it");
// evt.preventDefault();


	// body...
});

$('.pre').click(function(evt) {

console.log("inside submition");

var csrftoken = getCookie('csrftoken');
console.log(csrftoken);
var cur_que = window.location.pathname.split('/')[2];
formData = {
	'cq' : cur_que,
	'type' : 'pre',
}

$.ajax({
       type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/q_submit/', // the url where we want to POST
            data: formData, // our data object
            dataType: 'json', // what type of data do we expect back from the server
            encode: true,
            headers: {"X-CSRFToken":csrftoken}

})

.done(function(data){
console.log(data);

}).fail(function(data){
	console.log(data);
})
console.log("submition finished");

// alert("it");
// evt.preventDefault();


	// body...
});

$("form.answer-form input[name=answer]").click(function (evt) {
    console.log("it works");
    ans = $('input[name=answer]:checked').val();
    var csrftoken = getCookie('csrftoken');

    console.log(ans);
    console.log(csrftoken);



    formData = {
        'cq' : cur_que,
        'ans' : ans,
    }

    $.ajax({
       type: 'POST', // define the type of HTTP verb we want to use (POST for our form)
            url: '/ans_submit/', // the url where we want to POST
            data: formData, // our data object
            dataType: 'json', // what type of data do we expect back from the server
            encode: true,
            headers: {"X-CSRFToken":csrftoken}

})

.done(function(data){
console.log(data);

}).fail(function(data){
    console.log(data);
})
console.log("submition finished");


    // body...
})