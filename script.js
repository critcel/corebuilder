$(document).ready(function () { // load json file using jquery ajax
    $.getJSON('data.json', function (data) {
        var output = '<ul>';
        $.each(data, function (key, val) {
            output += '<li>' + val.name + ' &ndash; ' + val.age '</li>';
        });
        output += '</ul>';
        $('#update').html(output);  // replace all existing content
    });
});
