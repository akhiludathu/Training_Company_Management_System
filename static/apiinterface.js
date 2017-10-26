$(document).ready(function(){
	$('#btnLogIn').click(function(){
		$.ajax({
			url: '/handle_login',
			data: $('#loginform').serialize(),
			type: 'POST',
			success: function(response){
				//console.log('yay');
				//console.log(response);
				if(response == 'Wrong login credentials')
				{
					alert('Wrong Password!');
				}
				else
				{
					$('#login-modal').modal('toggle');
					var form = document.getElementById("loginform");
					form.reset();
					console.log(response)
					if(response == 'Successful admin login')
					{
						window.location.replace('/adminHome#load-stuff')
						$(function () {
						    if (document.URL.indexOf('#load-stuff') === -1)
								{
						        console.log($('#random').text())
										console.log('hiii')
						    }
						});
					}
					else if(response == 'Successful company login')
					{
						window.location = '/companyHome'
					}
				}
			},
			error: function(error){
				alert('Username doesn\'t exist!');
			}
		});
	});

	$('#btnSignUp').click(function(){
		$.ajax({
			url: '/handle_signup',
			data: $('#signupform').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				if(response == 'Success')
				{
					$('#signup-modal').modal('toggle');
					alert('Account created successfully!');
					var form = document.getElementById("signupform");
					form.reset();
				}
			},
			error: function(error){
				alert('Username already exists!');
			}
		});
	});

	$('#addcoursebtn').click(function(){
		console.log($('#newcourseform').serialize());
		$.ajax({
			url: '/handle_newcourse',
			data: $('#newcourseform').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				if(response == 'Success')
				{
					alert('Program added successfully!');
					var form = document.getElementById("newcourseform");
					form.reset();
				}
			},
			error: function(error){
				alert('Could not add program.');
			}
		});
	});

	$('#btnGrade').click(function(){
		console.log($('#gradeform').serialize());
		var obj = $('#gradeform').serialize();
		console.log(obj);
		$.ajax({
			url: '/gradechange',
			data: $('#gradeform').serializeArray(),
			//data: JSON.stringify(obj),
			type: 'POST',
			success: function(response){
				console.log(response);
				if(response == 'Success')
				{
					var form = document.getElementById("gradeform");
					form.reset();
					$("#grade-modal").modal('toggle');
					alert('Grade updated successfully!');
				}
			},
			error: function(error){
				alert('Could not change grade.');
			}
		});
	});

	$('#addtraineebtn').click(function(){
		$.ajax({
			url: '/handle_newtrainee',
			data: $('#newtraineeform').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
				if(response == 'Success')
				{
					alert('Trainee details added successfully!');
					var form = document.getElementById("newtraineeform");
					form.reset();
				}
			},
			error: function(error){
				alert('Could not add trainee details.');
			}
		});
	});

	$("#startdate").datepicker();
});
