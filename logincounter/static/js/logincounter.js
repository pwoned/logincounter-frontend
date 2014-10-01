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

function update(data) {
	switch(data.errCode) {
		case SUCCESS:
			$('#login-message').html('Welcome, ' + $('#user').val() + '!');
			$('#content').html('You have logged in ' + data.count + ' times.').show();
			$('#inputs').hide();
			$('#login-button').hide();
			$('#add-button').hide();
			$('#logout-button').show();
			$('#login-box').attr('class', 'panel panel-success');
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
	return false;
}

$(document).ready(function() {
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
});