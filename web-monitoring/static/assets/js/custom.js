$('#SSLEnable').on('change', function() {
    if ($('#SSLEnable').is(":checked"))
        $("#ssl_content").show();
    else
        $("#ssl_content").hide();
});

$('#isperfomance').on('change', function() {
    if ($('#isperfomance').is(":checked"))
        $("#performance_content").show();
    else
        $("#performance_content").hide();
});