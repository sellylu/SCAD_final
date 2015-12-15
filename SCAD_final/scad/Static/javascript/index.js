function saveUserInfo() {

	FB.api('/me',{"fields": "name, email"}, function(response) {
		   if(response && !response.error) {
		   $.ajaxSetup({
					   data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
					   });
		   $.post("/index/",{user_id : response.id, user_name: response.name, user_email: response.email}).then(function(){$('#about-us').hide();console.log('Successful login for: ' + response.name + ' with ' + response.id + ' and ' + response.email);});


      }
		});

}

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "https://connect.facebook.net/en_US/sdk.js";
 fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

function checkLoginState() {
    FB.getLoginStatus(function(response) {
                      statusChangeCallback(response);
                      });
}

function statusChangeCallback(response) {
    if (response.status === 'connected') {
        saveUserInfo();
    } else if (response.status === 'not_authorized') {
        if(confirm('Please log ' + 'into this app.'))
            FB.login(function(response) {
                     // TODO
                     }, {scope: 'email'});
    } else {
        alert('Please log ' + 'into Facebook.')
    }
}

window.fbAsyncInit = function() {
    FB.init({
            appId      : '879242695464021',
			cookie     : true,
            xfbml      : true,
            version    : 'v2.5'
            });
};
