// Launch a check on the given example editor
function query_check_result(example_name, editors, container) {

   files = []

   editors.forEach(function(e){
       files.push({'basename': e.basename,
                   'contents': e.getValue()})
   })

   data = {"example_name": example_name,
           "files": files}

   // request the examples
   $.ajax({
      url: "/check_program/",
      data: JSON.stringify(data),
      type: "POST",
      dataType : "json",
      contentType: 'application/json; charset=UTF-8',
   })
   .done(function( json ) {
      alert(json)
   })
   .fail(function( xhr, status, errorThrown ) {
     //
     alert( "could not run the example" );
     console.log( "Error: " + errorThrown );
     console.log( "Status: " + status );
     console.dir( xhr );
   })
}


// Fills a <div> with an editable representation of an example.
//    container: the <div> in question
//    example_name: the name of the example to load

var unique_id = 0

function fill_editor(container, example_name) {

   unique_id++;
   container.attr("the_id", unique_id);

   // request the examples
   $.ajax({
      url: "/example/" + example_name,
      data: {},
      type: "GET",
      dataType : "json",
   })
   .done(function( json ) {
      // On success, create editors for each of the resources

      // First create the tabs

      var ul = $( '<ul class="nav nav-tabs" role="tablist">' )
      ul.appendTo(container);

      var counter = 0;

      json.resources.forEach(function(resource){
          counter++;
          var the_id = "tab_" + container.attr("the_id") + "-" + counter

          var li = $( '<li role="presentation" class="'
           + (counter == 1 ? 'active' : '')
           + '">' ).appendTo(ul);
          $('<a href="#' + the_id + '" aria-controls="'
            + the_id + '" '
            + 'id="' + the_id + '-tab"'
            + 'role="tab" data-toggle="tab">'
            + resource.basename + '</a>').appendTo(li)
      })

      // Then fill the contents of the tabs

      var content = $( '<div class="tab-content">' )
      content.appendTo(container);

      counter = 0;

      var editors = []

      json.resources.forEach(function(resource){
          counter++;

          var the_id = "tab_" + container.attr("the_id") + "-" + counter
          var div = $('<div role="tabpanel" class="tab-pane'
                      + (counter == 1 ? ' active' : '')
                      + '" id="' + the_id + '">');
          var editordiv = $('<div class="editor_container" id="' + resource.basename + the_id + '_editor">');
          editordiv.appendTo(div)
          div.appendTo(content);


          // ACE editors...
          var editor = ace.edit(resource.basename + the_id + '_editor')
          editor.session.setMode("ace/mode/ada");

          // ... and their contents
          editor.setValue(resource.contents)
          editor.gotoLine(1)
          editor.initial_contents = resource.contents
          editor.basename = resource.basename

          // TODO: place the cursor at 1,1

          // Append the editor to the list of editors
          editors.push(editor)
      })

      var toolbar = $('<div class="btn-toolbar">')
      toolbar.appendTo(container)

      reset_button = $('<button type="button" class="btn btn-secondary">').text("Reset").appendTo(toolbar)
      reset_button.editors = editors
      reset_button.on('click', function (x){
          reset_button.editors.forEach(function (x){
             x.setValue(x.initial_contents)
             x.gotoLine(1)
          })
      })

      check_button = $('<button type="button" class="btn btn-primary">').text("Check").appendTo(toolbar)
      check_button.editors = editors
      check_button.on('click', function (x){
         query_check_result(example_name, check_button.editors, container)
      })
   })
   .fail(function( xhr, status, errorThrown ) {
     //
     alert( "could not download the example" );
     console.log( "Error: " + errorThrown );
     console.log( "Status: " + status );
     console.dir( xhr );
   })
   // Code to run regardless of success or failure;
   // commented for now - just so I remember how it's done
   // .always(function( xhr, status ) {});
}


// Called when the document is ready
$( document ).ready(function() {

   // Iterate on all divs, finding those that have the "example_editor"
   // attribute
   $( "div" ).each(function(index, element) {
       example_name = $( this ).attr("example_editor");
       if (example_name) {
           fill_editor($( this ), example_name);
           }
       })

});
