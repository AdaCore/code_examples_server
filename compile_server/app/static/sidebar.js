$( document ).ready( function() {
    $( document ).on( "scroll", onScroll);

    $( ".toc-link" ).click( function(e) {

        var hid = lid2hid( $( this ).attr( 'id' ) );
        var div_position = $( hid ).offset().top;
        var padding = 12;
        var header_offset = $( "#title_header" ).outerHeight();

        $( 'html, body' ).animate( {
            scrollTop: (div_position - header_offset - padding)
        }, 800);
        
        if ( $( "#sidebar" ).hasClass( 'active' ) )
            toggleAll(e);
    });
    
    $( "#sidebarLink" ).click( toggleAll );
    $( "#main" ).click( function(e) {
        if ( $( "#sidebar" ).hasClass( 'active' ) )
            toggleAll(e);
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

function toggleAll(e) {
    var active = 'active';

    e.preventDefault();
    
    $( "#wrapper" ).toggleClass( active );
    $( "#sidebar" ).toggleClass( active );
    $( "#sidebarLink" ).toggleClass( active );
}
