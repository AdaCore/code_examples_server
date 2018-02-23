$(document).ready( function() {
    $( document ).on( "scroll", onScroll);

    $( ".toc-link" ).click( function() {

        var hid = lid2hid( $( this ).attr( 'id' ) );

        $( 'html, body' ).animate( {
            scrollTop: $( hid ).offset().top
        }, 800);
    });

    onScroll();

});

function lid2hid(lid) {
    return "#header" + lid.substr(5);
}

function onScroll() {
    var active = "pure-menu-selected"
    
    $( '#toc a' ).each( function () {
        var refElement = $( lid2hid( $( this ).attr( 'id' ) ) );
        var currLink = $( this );

        if ( inView( refElement) ) {
            $( '#toc ul li a' ).removeClass( active );
            currLink.addClass( active );
        }
    });
}

function inView(elem) {
    var viewport = {};
    viewport.top = $( window ).scrollTop();
    viewport.bottom = viewport.top + $( window ).height();

    var bounds = {};
    bounds.top = $( elem ).offset().top;
    bounds.bottom = bounds.top + $( elem ).outerHeight();

    return ((bounds.top <= viewport.bottom) && (bounds.bottom >= viewport.top));
}