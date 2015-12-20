$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

function creategroup_submit() {

    creator_id = Cookies.get('user_id');

    group_name = document.getElementById("group_name").value;

    intro = document.getElementById("intro").value;
    private = parseInt(document.getElementsByName("private")[0].value);
    console.log(typeof(private));
    member_limit = parseInt(document.getElementsByName("member_limit")[0].value);
    console.log(creator_id,group_name,intro,private,member_limit);
    $.post( "/index/", { group_name : group_name,  member_limit :member_limit,intro:intro,private:private,creator_id:creator_id });

    $("#create_group_Modal").modal('hide');
}

function saveUserInfo() {

	FB.api('/me',{"fields": "name, email"}, function(response) {
		   if(response && !response.error) {

               $.post("/index/",{
                   user_id : response.id, user_name: response.name, user_email: response.email})
                   .then(function(){
                       $('#about-us').hide();
                       Cookies.set('user_id',response.id);
                       console.log('Successful login for: ' + response.name + ' with ' + response.id + ' and ' + response.email);
                   });


            }
		});

}

(function(d, s, id){
 var js, fjs = d.getElementsByTagName(s)[0];
 if (d.getElementById(id)) {return;}
 js = d.createElement(s); js.id = id;
 js.src = "http://connect.facebook.net/en_US/sdk.js";
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
            FB.login(function(response) {
                    if (response.authResponse) {
                        FB.api('/me', function (response) {
                            saveUserInfo();
                        });
                    }
            }, {scope: 'email'});
    } else {
        alert('Please log ' + 'into Facebook.')
        FB.login(function(response) {
                    if (response.authResponse) {
                        FB.api('/me', function(response) {
                            saveUserInfo();
                         });
                    }
        }, {scope: 'email'});
    }
}

window.fbAsyncInit = function() {
    FB.init({
            appId      : '444916912380076',
			cookie     : true,
            xfbml      : true,
            version    : 'v2.5'
            });
};
