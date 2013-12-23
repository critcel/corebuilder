$(document).ready(function () { // load json file using jquery ajax
    $.getJSON('javascripts/timestamp.json', function (data) {
        var output = '<ul>';
        $.each(data, function (key, val) {
            output += '<li>' + val.name + ':' + '</li>';
        });
        output += '</ul>';
        $('#update').html(output);  // replace all existing content
    });
});
$(document).ready(function () {       // load text file using jquery ajax
    $('#coresource').load('corebuild.inp');    // load text data
});
