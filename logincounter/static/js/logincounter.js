ERR_BAD_CREDENTIALS = -1
ERR_BAD_PASSWORD = -4
ERR_BAD_USERNAME = -3
ERR_USER_EXISTS = -2
MAX_PASSWORD_LENGTH = 128
MAX_USERNAME_LENGTH = 128
SUCCESS = 1

function json_request(page, dict, success, failure) {
	$.ajax({
		type: 'POST',
		url: page,
		data: JSON.stringify(dict),
		contentType: "application/json",
		dataType: "json",
		success: success,
		error: failure
	});
}

function show_login_page(user, count){
	$('#login-message').html('Welcome, ' + user + '!');
	$('#content').html('You have logged in ' + count + ' times.').show();
	$('#inputs').hide();
	$('#login-button').hide();
	$('#add-button').hide();
	$('#logout-button').show();
	$('#login-box').attr('class', 'panel panel-success');
}

function update(data) {
	switch(data.errCode) {
		case SUCCESS:
			show_login_page($('#user').val(), data.count);	
			$.cookie("name", user);
			$.cookie("count", data.count);
			break;
		case ERR_BAD_CREDENTIALS:
			$('#login-message').html('Invalid username and password combination. Please try again.');
			$('#login-box').attr('class', 'panel panel-danger');
			break;
		case ERR_BAD_PASSWORD:
			$('#login-message').html('The password should be at most 128 characters long. Please try again.');
			$('#login-box').attr('class', 'panel panel-danger');
			break;
		case ERR_BAD_USERNAME:
			$('#login-message').html('The username should be non-empty and at most 128 characters long. Please try again.');
			$('#login-box').attr('class', 'panel panel-danger');
			break;
		case ERR_USER_EXISTS:
			$('#login-message').html('This username already exists. Please try again.');
			$('#login-box').attr('class', 'panel panel-warning');
			break;
	}
}

function logout() {
	$('#login-message').html('Please enter your credentials below');
	$('#content').html('').hide();
	$('#user').val('');
	$('#password').val('');
	$('#inputs').show();
	$('#login-button').show();
	$('#add-button').show();
	$('#logout-button').hide();
	$('#login-box').attr('class', 'panel panel-default');
	
	$.removeCookie("name");
	$.removeCookie("count");
	return false;
}

function validate_user() {
	user = $('#user').val();
	if(user.length == 0 || user.length > MAX_USERNAME_LENGTH){
		$('#login-message').html('The username should be non-empty and at most 128 characters long. Please try again.');
		$('#login-box').attr('class', 'panel panel-danger');
	}
}

function validate_password() {
	password = $('#password').val();
	if(password.length > MAX_PASSWORD_LENGTH){
		$('#login-message').html('The password should be at most 128 characters long. Please try again.');
		$('#login-box').attr('class', 'panel panel-danger');
	}
}

$(document).ready(function() {
	if($.cookie("name") && $.cookie("count")){
		show_login_page($.cookie("name"), $.cookie("count"));
	}
	$('#login-button').click(function() {
		user = $('#user').val();
		password = $('#password').val();
		json_request("/users/login", {user: user, password: password}, update);
		return false;
	});
	$('#add-button').click(function() {
		user = $('#user').val();
		password = $('#password').val();
		json_request("/users/add", {user: user, password: password}, update);
		return false;
	});
	$('#logout-button').click(logout);
	$('#user').blur(validate_user);
	$('#password').blur(validate_password);
});