// Contact us Error Controller
$("#alert-div-input-username").hide();
$("#alert-div-input-mobile").hide();
$("#alert-div-input-email").hide();
$("#alert-div-input-message").hide();
$("#alert-div-input-empty-email-or-mobile").hide();
$("#alert-div-send-succfull").hide();
// This User Name
$("#alert-div-input-username").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
	'<div class="alert" role="alert">' +
	'<i class="far fa-exclamation-circle"></i>' +
	'<p>نام و نام خانوادگی نمی تواند خالی باشد.</p>' +
    '</div></div>'
);
// This User Mobile
$("#alert-div-input-mobile").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
	'<div class="alert" role="alert">' +
	'<i class="far fa-exclamation-circle"></i>' +
	'<p>شماره موبایل شما درست وارد نشده است.</p>' +
    '</div></div>'
);
// This User Email
$("#alert-div-input-email").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
	'<div class="alert" role="alert">' +
	'<i class="far fa-exclamation-circle"></i>' +
	'<p>ایمیل شما درست وارد نشده است.</p>' +
    '</div></div>'
);
// This User Message
$("#alert-div-input-message").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
    '<div class="alert" role="alert">' +
    '<i class="far fa-exclamation-circle"></i>' +
    '<p>پیام شما نمی تواند خالی باشد.</p>' +
    '</div></div>'
);
// Mobile Or Email Is Empty
$("#alert-div-input-empty-email-or-mobile").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
    '<div class="alert" role="alert">' +
    '<i class="far fa-exclamation-circle"></i>' +
    '<p>برای ثبت پیام شماره موبایل یا ایمیل اجباریست.</p>' +
    '</div></div>'
);
// Send From Is Succful
$("#alert-div-send-succfull").html('<div class="col-xl-12 xol-lg-12 col-md-12 col-sm-12 col-12">' +
    '<div class="alert" role="alert">' +
    '<i class="far fa-exclamation-circle"></i>' +
    '<p>پیام شما با موفقیت ثبت شد.</p>' +
    '</div></div>'
);
// check validate email
function validateEmail(thisemail) {
    const pattern = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(pattern.test(thisemail));
    return pattern.test(thisemail);
}
// check contact fields
check_fields = function (thisuser_name) {
    var status = false;
    if(thisuser_name.length == 0) {
        $("#alert-div-input-username").show();
        $("#input_fullname").addClass("inputshopempty");
        status = false;
    }
    if(($('#input_mobile').val().length != 11) & ($('#input_useremail').val().length > 0) & (validateEmail($('#input_useremail').val()) {
        $("#alert-div-input-mobile").show();
        $("#input_mobile").addClass("inputshopempty");
        status = false;
    }
    if($('#input_useremail').val().length == 0) {
        $("#alert-div-input-email").show();
        $("#input_useremail").addClass("inputshopempty");
        status = false;
    }
    if($('#input_message').val().length < 2) {
        $("#alert-div-input-message").show();
        $("#input_message").addClass("inputshopempty");
        status = false;
    }
    if(($('#input_useremail').val().length == 0) & ($('#input_mobile').val().length != 11)) {
        $("#alert-div-input-empty-email-or-mobile").show();
        $("#input_useremail").addClass("inputshopempty");
        $("#input_mobile").addClass("inputshopempty");
        status = false;
    }
    // if ((thisuser_name.length != 0) & ((thisuser_mobile.length != 0 && thisuser_mobile.length == 11) | (thisuser_email.length != 0)) & (thisuser_message.length != 0)){
    //     return true;
    // }else{
    //     return false;
    // }
    return status;
}

$("#input_fullname").on("input", function () {
    if ($(this).val() !== '') {
        $(this).removeClass("inputshopempty");
        $("#alert-div-input-username").hide();
    }
})

$("#input_mobile").on("input", function () {
    if ($(this).val().length == 11) {
        $(this).removeClass("inputshopempty");
        $("#alert-div-input-mobile").hide();
    }
})

$("#input_useremail").on("input", function () {
    if ($(this).val() !== '') {
        $(this).removeClass("inputshopempty");
        $("#alert-div-input-email").hide();
    }
})

$("#input_message").on("input", function () {
    if ($(this).val().length > 2) {
        $(this).removeClass("inputshopempty");
        $("#alert-div-input-message").hide();
    }
})