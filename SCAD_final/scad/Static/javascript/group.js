$.ajaxSetup({
    data: {csrfmiddlewaretoken: '{{ csrf_token }}' },
});

$(document).ready(function() {
// page is now ready, initialize the calendar...




});

function setuser_no(){
    id = Cookies.get('user_id');
    if(id != undefined){
        str = '/userno/'+id;
        $.get(str,function(data){
            Cookies.set('user_no',data);
        });
    }
}

function checkShowAddButton(member){

	id = Cookies.get('user_id');
    if(id != undefined){
    	
    	user_no = Cookies.get('user_no');
    	showbutton = 0;
		if(user_no != undefined){
			var tmp = member.split(',');
			showbutton = 1;
			for(i=0;i<tmp.length;i++){
				if(user_no == tmp[i]){
					showbutton = 0;
				}
			}
		}

	
	
		if(showbutton == 1){
			document.getElementById('join_group_btn').style.visibility = 'visible';
		}else{
			document.getElementById('join_group_btn').style.visibility = 'hidden';
		}


    }else{
    	document.getElementById('join_group_btn').style.visibility = 'hidden';
	
    }
	
	
}
function checkShowLoginDiv() {
    user_id = Cookies.get('user_id');
	if(user_id != undefined)
		adjustCSS();
}

function adjustCSS() {
	$('#navbar-button').show();
	$('#create_group_button').show();
	$('#navbar-login').hide();
}

function creategroup_submit() {
	check_group_name = $('#group_name').val();
	check_group_intro = $('#intro').val();
	check_time = $('#finished_time_date').val();
	nosubmit = 0;
	if(check_time == '') {
		$('#finished_time_date').attr('style','border: 1px solid red');
		nosubmit =1;
	} else {
		$('#finished_time_date').removeAttr('style');
	}
	if(check_group_intro =='') {
		$('#introdiv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#introdiv').attr('class','form-group');
	}
	if(check_group_name=='') {
		$('#namediv').attr('class','form-group has-error');
		nosubmit =1;
	} else {
		$('#namediv').attr('class','form-group');
	}
	if(nosubmit==1)return false;

	creator_id = Cookies.get('user_id');
	group_name = document.getElementById("group_name").value;
	intro = document.getElementById("intro").value;
	finished_time = document.getElementById("finished_time_date").value;
	if(document.getElementById("private_op1").checked) {
		private = 0;
	} else {
		private = 1;
	}
	date = Date.now();
	group_id = creator_id + date;
	member_limit = parseInt(document.getElementsByName("member_limit")[0].value);

	$.post( "/index/", { group_id : group_id, group_name : group_name,  member_limit :member_limit,intro:intro,private:private,creator_id:creator_id ,finished_time:finished_time})
		.then(function () {
			window.location = '/group/'+group_id;
	});
	// TODO: display link of the group
}

function getMyInfoURL(){
	user_id = Cookies.get('user_id');
	window.location = '/user/'+user_id+'/';
}

function logout() {
	Cookies.remove('user_id');
	window.location = '/index/';
}

function showSchedule(group_id) {
	$('#myContent').empty();

	
	var div = $('<div/>', {id: 'calendar'});

	$('#myContent').append(div);
	$('#calendar').fullCalendar({
		// put your options and callbacks here
		events: function( start, end, callback ) {
			$.get(calendarurl, function(data){
		
		
			tmp = data.split(';');
			console.log('tmp = ' + tmp);
			for(var i=0;i<tmp.length-1;i++){
				tmp2 = tmp[i].split(',');
				console.log('tmp2 = ' + tmp2);
				event_title = tmp2[0];
				event_start = tmp2[1];
				myevent = {title: event_title,start: event_start,allDay:true};
				$('#calendar').fullCalendar( 'renderEvent', myevent);
			}
			});

       },

		eventClick: function(calEvent, jsEvent, view) {
			alert('Event: ' + calEvent.title);
			// change the border color just for fun
			$(this).css('border-color', 'red');
		},
		
		dayClick: function(date, allDay, jsEvent, view) {
		    var title = prompt('Add new event');
		   
		    var d = new Date(date);
		    var year = d.getFullYear();
		    var month = (d.getMonth()+1);
		    var date = d.getDate();
		    if(month<10) month='0'+month;
		    if(date<10)date='0'+date;
		    var datetime = year + '-' + month + '-' + date;
		   
		    url = '/postcalendarevent/' + group_id +'/';
		    $.post(url, { title:title,start: datetime}).
				then(function(){
					showSchedule(group_id);
				});
		}	    
	});

	var calendarurl = '/group/' + group_id + '/calendar';
	$.get(calendarurl, function(data){
		
		
		tmp = data.split(';');
		console.log('tmp = ' + tmp);
		for(var i=0;i<tmp.length-1;i++){
			tmp2 = tmp[i].split(',');
			console.log('tmp2 = ' + tmp2);
			event_title = tmp2[0];
			event_start = tmp2[1];
			myevent = {title: event_title,start: event_start,end:event_start,allDay:true};
			$('#calendar').fullCalendar( 'renderEvent', myevent);
		}
	});



}

function Group_Member_inf(id){
	$('#myContent').empty();
	var str = '/group/' + id + '/member_inf';
	$.get(str, function(data){
		var tmp = data.split(",");
		var member = '';
		for(var i = 0; i < tmp.length; i+=2) {
			member += '<tr><td>' + tmp[i] + '</td><td>' + tmp[i+1] + '</td></tr>';
		}
		$('#myContent').append('<table class="table table-striped table-hover"><thead><tr><td>NAME</td><td>EMAIL</td></tr></thead><tbody>' + member + '</tbody></table>');
		console.log(data);
	});
}

function joinGroup(group_id) {
	// TODO: implement the action for user to join the displayed group
	var str = '/group/' + group_id +'/';
	join_id = Cookies.get('user_id');
	$.post( str, { group_id : group_id, join_id:join_id })
		.then(function () {
			$('#join_group_btn').hide();
			alert("Join group success!");
		});
}

function saveUserInfo() {
	FB.api('/me',{"fields": "name, email"}, function(response) {
		if(response && !response.error) {
			$.post("/index/",{
				user_id : response.id, user_name: response.name, user_email: response.email})
				.then(function(){
					adjustCSS();
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
