$(document).ready( function() {

    $( ".toc_link" ).click( function() {

        var lid = $( this ).attr( 'id' );
        var hid = "#header" + lid.substr(5);

        $( 'html, body' ).animate( {
            scrollTop: $( hid ).offset().top
        }, 800);
    });

});