$(function () {

    $("#contactForm input,#contactForm textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function ($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function ($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var name = $("input#name").val();
            var email = $("input#email").val();
            var phone = $("input#phone").val();
            var message = $("textarea#message").val();
            var firstName = name; // For Success/Failure Message
            // Check for white space in name for Success/Fail message
            if (firstName.indexOf(' ') >= 0) {
                firstName = name.split(' ').slice(0, -1).join(' ');
            }
            $this = $("#sendMessageButton");
            $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
            $.ajax({
                url: "submit",
                type: "POST",
                data: {
                    name: name,
                    phone: phone,
                    email: email,
                    message: message
                },
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                cache: false,
                success: function () {
                    // Success message
                    $('#success').html("<div class='alert alert-success'>");
                    $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-success')
                        .append("<strong>Your message has been sent. </strong>");
                    $('#success > .alert-success')
                        .append('</div>');
                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
                error: function () {
                    // Fail message
                    $('#success').html("<div class='alert alert-danger'>");
                    $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
                    $('#success > .alert-danger').append('</div>');
                    //clear all fields
                    $('#contactForm').trigger("reset");
                },
                complete: function () {
                    setTimeout(function () {
                        $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
                    }, 1000);
                }
            });
        },
        filter: function () {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

/*When clicking on Full hide fail/success boxes */
$('#name').focus(function () {
    $('#success').html('');
});

$(function () {

    $("#adoptionForm input,#adoptionForm textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function ($form, event, errors) {
            // additional error messages or events
        },
        submitSuccess: function ($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var name = $("input#adopt-name").val();
            var email = $("input#adopt-email").val();
            var phone = $("input#adopt-phone").val();
            var message = $("textarea#adopt-message").val();
            var pet_id = $("input#adopt-pet-id").val();
            var pet_name = $("input#adopt-pet-name").val();
            var location = $("input#adopt-location").val();
            var firstName = name; // For Success/Failure Message
            // Check for white space in name for Success/Fail message
            if (firstName.indexOf(' ') >= 0) {
                firstName = name.split(' ').slice(0, -1).join(' ');
            }
            $this = $("#sendAdoptionFormButton");
            $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
            $.ajax({
                url: "submit/adopt/",
                type: "POST",
                data: {
                    name: name,
                    phone: phone,
                    email: email,
                    message: message,
                    pet_id: pet_id,
                    pet_name: pet_name,
                    location: location
                },
                headers: {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                cache: false,
                success: function () {
                    // Success message
                    $('#adopt-success').html("<div class='alert alert-success'>");
                    $('#adopt-success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#adopt-success > .alert-success')
                        .append("<strong>Your message has been sent. </strong>");
                    $('#adopt-success > .alert-success')
                        .append('</div>');
                    //clear all fields
                    $('#adoptionForm').trigger("reset");
                },
                error: function () {
                    // Fail message
                    $('#adopt-success').html("<div class='alert alert-danger'>");
                    $('#adopt-success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                        .append("</button>");
                    $('#adopt-success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
                    $('#adopt-success > .alert-danger').append('</div>');
                    //clear all fields
                    $('#adoptionForm').trigger("reset");
                },
                complete: function () {
                    setTimeout(function () {
                        $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
                    }, 1000);
                }
            });
        },
        filter: function () {
            return $(this).is(":visible");
        },
    });

    $("a[data-toggle=\"tab\"]").click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

/*When clicking on Full hide fail/success boxes */
$('#adopt-name').focus(function () {
    $('#adopt-success').html('');
});

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

/* Upload button */
function uploadajax(ttl, cl) {
    var fileList = $('#multiupload').prop("files");
    $('#prog' + cl).removeClass('loading-prep').addClass('upload-image');

    var form_data = "";

    form_data = new FormData();
    form_data.append("upload_image", fileList[cl]);
    form_data.append("pet_id", $("#register-pet-id").val());

    var request = $.ajax({
        url: "register/upload/",
        cache: false,
        contentType: false,
        processData: false,
        async: true,
        data: form_data,
        type: 'POST',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        xhr: function () {
            var xhr = $.ajaxSettings.xhr();
            if (xhr.upload) {
                xhr.upload.addEventListener('progress', function (event) {
                    var percent = 0;
                    if (event.lengthComputable) {
                        percent = Math.ceil(event.loaded / event.total * 100);
                    }
                    $('#prog' + cl).text(' ' + percent + '%')

                }, false);
            }
            return xhr;
        },
        success: function (res, status) {
            if (status == 'success') {
                percent = 0;
                $('#prog' + cl).text('');
                $('#prog' + cl).text(' Success');
                if (cl < ttl) {
                    uploadajax(ttl, cl + 1);
                }
            }
        },
        fail: function (res) {
            alert('Failed');
        }
    })
}

$('#upload-btn').click(function () {

    var fileList = $('#multiupload').prop("files");
    $('#upload-stats').html('');
    var i;
    for (i = 0; i < fileList.length; i++) {
        $('#upload-stats').append('<p class="upload-page">' + fileList[i].name + '<span class="loading-prep" id="prog' + i + '"></span></p>');
        if (i == fileList.length - 1) {
            uploadajax(fileList.length - 1, 0);
        }
    }

});


/* Registration Form */
$('#sendRegistrationFormButton').click(function () {
    $('#registrationForm').validator('validate');
    registrationAjax();
    $('html, body').animate({
        scrollTop: $("#sendRegistrationFormButton").offset().top
    }, 400);
});

function registrationAjax() {
    var pet_name = $("input#register-pet-name").val();
    var breed = $("select#register-breed").val();
    var country = $("select#register-country").val();
    var city = $("input#register-city").val();
    var age_month = $("select#register-age-month").val();
    var age_year = $("select#register-age-year").val();
    var gender = $("select#register-gender").val();
    var sterilized = $("input#register-sterilized").is(":checked");
    var house_trained = $("input#register-house-trained").is(":checked");
    var is_adopted = $("input#register-adopted").is(":checked");
    var show_badge = $("input#register-show-badge").is(":checked");
    var characteristics = $("textarea#register-characteristics").val();
    var story = $("textarea#register-story").val();
    var added_by = $("input#register-user-id").val();
    var email = $("input#register-email").val();
    var mobile = $("input#register-mobile").val();

    var firstName = $("input#register-added-by").val(); // For Success/Failure Message
    // Check for white space in name for Success/Fail message
    if (firstName.indexOf(' ') >= 0) {
        firstName = name.split(' ').slice(0, -1).join(' ');
    }
    $this = $("#sendRegistrationFormButton");
    $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
    $.ajax({
        url: "register/submit",
        type: "POST",
        data: {
            pet_name: pet_name,
            breed: breed,
            country: country,
            city: city,
            age_month: age_month,
            age_year: age_year,
            gender: gender,
            sterilized: sterilized,
            house_trained: house_trained,
            is_adopted: is_adopted,
            show_badge: show_badge,
            characteristics: characteristics,
            story: story,
            added_by: added_by,
            email: email,
            mobile: mobile
        },
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        },
        cache: false,
        success: function (data) {
            // Success message
            $('#register-success').html("<div class='alert alert-success'>");
            $('#register-success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                .append("</button>");
            $('#register-success > .alert-success')
                .append("<strong>Your message has been sent. Now Please upload some images. </strong>");
            $('#register-success > .alert-success')
                .append('</div>');
            //clear all fields
            $('#registrationForm').trigger("reset");

            // show uload block
            $('#upload-block').show();

            // set  pet-id
            $("#register-pet-id").val(data.pet_id);

            // // prevent submit success scroll
            // event.preventDefault();
            // $('html, body').animate({
            //     scrollTop: $("#upload-block").offset().top
            // }, 400);
        },
        error: function () {
            // Fail message
            $('#register-success').html("<div class='alert alert-danger'>");
            $('#register-success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                .append("</button>");
            $('#register-success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that server is not responding. Please try again later!"));
            $('#register-success > .alert-danger').append('</div>');
            //clear all fields
            // $('#registrationForm').trigger("reset");
        },
        complete: function () {
            setTimeout(function () {
                $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
            }, 1000);
        }
    });
}


/* Filter button */
$(document).ready(function () {
    if (window.location.pathname == '/pets/all') {
        populate_filters()
    }
});

function populate_filters() {
    if (getUrlParameter('pa') == 'true') {
        $('#filter-peepalfarm-approved').prop("checked", true);
    }
    if (getUrlParameter('ht') == 'true') {
        $('#filter-house-trained').prop("checked", true);
    }
    if (getUrlParameter('s') == 'true') {
        $('#filter-sterilized').prop("checked", true);
    }
    if (getUrlParameter('ab')) {
        $('#filter-added-by').prop("value", getUrlParameter('ab'));
    }
    if (getUrlParameter('g')) {
        $('#filter-gender').prop("value", getUrlParameter('g'));
    }
    if (getUrlParameter('a')) {
        $('#filter-age').prop("value", getUrlParameter('a'));
    }
    if (getUrlParameter('b')) {
        $('#filter-breed').prop("value", getUrlParameter('b'));
    }
    if (getUrlParameter('c')) {
        $('#filter-country').prop("value", getUrlParameter('c'));
    }
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
}

$('#filterButton').click(function () {
    url = compute_filter_url()
    window.location.assign(url);
});

function compute_filter_url() {
    var url = "all?"
    var pa = $("#filter-peepalfarm-approved").prop("checked");
    url = url + "pa=" + pa + "&"
    var ht = $("#filter-house-trained").prop("checked");
    url = url + "ht=" + ht + "&"
    var s = $("#filter-sterilized").prop("checked");
    url = url + "s=" + s + "&"
    var ab = $("#filter-added-by").val();
    url = url + "ab=" + ab + "&"
    var g = $("#filter-gender").val();
    url = url + "g=" + g + "&"
    var a = $("#filter-age").val();
    url = url + "a=" + a + "&"
    var b = $("#filter-breed").val();
    url = url + "b=" + b + "&"
    var c = $("#filter-country").val();
    url = url + "c=" + c
    return url
}

// function filterAjax() {
//     var pa = $("#filter-peepalfarm-approved").val();
//     var ht = $("#filter-house-trained").val();
//     var s = $("#filter-sterilized").val();
//     var ab = $("#filter-added-by").val();
//     var g = $("#filter-gender").val();
//     var a = $("#filter-age").val();
//     var b = $("#filter-breed").val();
//     var c = $("#filter-country").val();
//
//     $this = $("#filterButton");
//     $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
//     $.ajax({
//         url: "pets/all",
//         type: "GET",
//         data: {
//             pa: pa,
//             ht: ht,
//             s: s,
//             ab: ab,
//             g: g,
//             a: a,
//             b: b,
//             c: c
//         },
//         cache: false,
//         success: function () {
//             // Success message
//         },
//         error: function () {
//             // Fail message
//         },
//         complete: function () {
//             setTimeout(function () {
//                 $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
//             }, 1000);
//         }
//     });
//
// }

// $(function () {
//
//     $("#registrationForm input,#registrationForm textarea,#registrationForm select").jqBootstrapValidation({
//         preventSubmit: true,
//         submitError: function ($form, event, errors) {
//             // additional error messages or events
//         },
//         submitSuccess: function ($form, event) {
//             event.preventDefault(); // prevent default submit behaviour
//             // get values from FORM
//
//             var fileList = $('#multiupload').prop("files");
//             var images_list = [];
//             var i = 0;
//             for (i = 0; i < fileList.length; i++) {
//                 images_list.push[fileList[i].name]
//             }
//             var pet_name = $("input#register-pet-name").val();
//             var breed = $("input#register-breed").val();
//             var age_month = $("input#register-age-month").val();
//             var age_year = $("input#register-age-year").val();
//             var location = $("input#register-location").val();
//             var gender = $("input#register-gender").val();
//             var sterilized = $("input#register-sterilized").val();
//             var house_trained = $("input#register-house-trained").val();
//             var is_adopted = $("input#register-adopted").val();
//             var show_badge = $("input#register-show-badge").val();
//             var characteristics = $("input#register-characteristics").val();
//             var story = $("input#register-story").val();
//             var images = images_list;
//             var added_by = $("input#register-added-by").val();
//             var email = $("input#register-email").val();
//             var mobile = $("input#register-mobile").val();
//
//             var firstName = pet_name; // For Success/Failure Message
//             // Check for white space in name for Success/Fail message
//             if (firstName.indexOf(' ') >= 0) {
//                 firstName = name.split(' ').slice(0, -1).join(' ');
//             }
//             $this = $("#sendRegistrationFormButton");
//             $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
//             $.ajax({
//                 url: "submit",
//                 type: "POST",
//                 data: {
//                     pet_name: pet_name,
//                     breed: breed,
//                     age_month: age_month,
//                     age_year: age_year,
//                     location: location,
//                     gender: gender,
//                     sterilized: sterilized,
//                     house_trained: house_trained,
//                     is_adopted: is_adopted,
//                     show_badge: show_badge,
//                     characteristics: characteristics,
//                     story: story,
//                     images: images,
//                     added_by: added_by,
//                     email: email,
//                     mobile: mobile
//                 },
//                 headers: {
//                     "X-CSRFToken": getCookie('csrftoken')
//                 },
//                 cache: false,
//                 success: function () {
//                     // Success message
//                     $('#register-success').html("<div class='alert alert-success'>");
//                     $('#register-success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
//                         .append("</button>");
//                     $('#register-success > .alert-success')
//                         .append("<strong>Your message has been sent. </strong>");
//                     $('#register-success > .alert-success')
//                         .append('</div>');
//                     //clear all fields
//                     $('#registrationForm').trigger("reset");
//                 },
//                 error: function () {
//                     // Fail message
//                     $('#register-success').html("<div class='alert alert-danger'>");
//                     $('#register-success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
//                         .append("</button>");
//                     $('#register-success > .alert-danger').append($("<strong>").text("Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!"));
//                     $('#register-success > .alert-danger').append('</div>');
//                     //clear all fields
//                     $('#registrationForm').trigger("reset");
//                 },
//                 complete: function () {
//                     setTimeout(function () {
//                         $this.prop("disabled", false); // Re-enable submit button when AJAX call is complete
//                     }, 1000);
//                 }
//             });
//         },
//         filter: function () {
//             return $(this).is(":visible");
//         },
//     });
//
//     $("a[data-toggle=\"tab\"]").click(function (e) {
//         e.preventDefault();
//         $(this).tab("show");
//     });
// });
//
// /*When clicking on Full hide fail/success boxes */
// $('#register-pet-name').focus(function () {
//     $('#register-success').html('');
// });