// globals START
// ==================================================================
function Globals () {

    var self = this;
    setDebug = function () {
        $.ajax({
            type: 'GET',
            url: '/ifdebug'
        })
        .done(function (data) {
            data = data.toLowerCase();
            bool = data === 'true' ? true : false;
            self.debug = bool;
        })
        .fail(function (error) {
            console.log(error);  
        })
    }

    setDebug();

    self.getCSRF = function (name) {
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

    return self;
}
var globals = new Globals(); // Instantiating globals
// globals END
// ******************************************************************

// HELPERS START
// ==================================================================
$('.next').click(function(evt) {
    var csrftoken = globals.getCSRF('csrftoken');
    formData = {
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
        if (globals.debug) {
            console.log(data);
        }
    })
    .fail(function(data){
    	console.log(data);
    })
});

$('.pre').click(function(evt) {
    var csrftoken = globals.getCSRF('csrftoken');
    formData = {
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
        if (globals.debug) {
            console.log(data);
        }
    })
    .fail(function(data){
    	console.log(data);
    })
});

$("form.answer-form input[name=answer]").click(function (evt) {
    var ans = $('input[name=answer]:checked').val();
    var csrftoken = globals.getCSRF('csrftoken');
    formData = {
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
        if (globals.debug) {
            console.log(data);
        }
    })
    .fail(function(data){
        console.log(data);
    })
})

function show_alert() {
   alert("Do you really want ro submit the test? You cannot re-take the test again.");
}
// HELPERS END
// ******************************************************************
