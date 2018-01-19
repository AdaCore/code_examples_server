$( document ).ready(function() {
    $( '.sidebar-link' ).click(function(event) {
        var linkid = event.target.id;
        var page_number = linkid.substr(12)
        var divsearch = "#page_anchor_" + page_number;

        if($( divsearch ).length) {
            $( 'html, body' ).animate({
                scrollTop: $( divsearch ).offset().top
            }, 500);
        }
        else {
            infinite_scroll(divsearch);
        }
    });

    function infinite_scroll(search_elem) {
        $('html, body').animate({
            scrollTop: $( document ).height()
        }, 500, function() {
            if(!$( search_elem ).length) {
                infinite_scroll(search_elem);
            }
        });

    }


    var infinite = new Waypoint.Infinite({
        element: $( '.infinite-container' )[0],
        onBeforePageLoad: function () {
            $( '.loading' ).show();
        },
        onAfterPageLoad: function ($items) {
            $( '.loading' ).hide();
        }
    });
});


