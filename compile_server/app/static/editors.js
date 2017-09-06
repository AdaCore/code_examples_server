// Process the result of a check
//  editors: the editors to decorate
//  output_area: the div where the messages should go
//  status: the exit status
//  message: any message coming back from the application
//   TODO: make use of message
function process_check_output(editors, output_area, output, status, message){

   // Clear the output area
   output_area.empty()

   // Process the lines
   output.forEach(function (l){
      // Look for lines that contain an error message
      var match_found = l.match(/^([a-zA-Z._-]+):(\d+):(\d+):(.+)$/)
      var klass = match_found?"output_msg":"output_line"

      // Print the line in the output area
      var div = $('<div class="' + klass + '">')
      div.text(l)
      div.appendTo(output_area)

      if (match_found != null){
         // Lines that contain a sloc are clickable:
         div.on('click', function(x){
            // find the corresponding editor
            var basename = match_found[1]
            editors.forEach(function (e){
               if (e.basename == basename){
                  // Switch to the tab that contains the editor
                  $("#" + e.unique_id + "-tab").tab('show')

                  // Jump to the corresponding line
                  e.gotoLine(parseInt(match_found[2]),
                             parseInt(match_found[3]), true)
               }
            })
         })
       }
    })

    // Congratulations!
    if (status == 0){
      var div = $('<div class="output_success">')
      div.text("Success!")
      div.appendTo(output_area)
    }
}

// Launch a check on the given example editor
function query_check_result(example_name, editors, output_area) {

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
      process_check_output(editors, output_area,
         json.output_lines, json.status, json.message)
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
          editor.unique_id = the_id

          // TODO: place the cursor at 1,1

          // Append the editor to the list of editors
          editors.push(editor)
      })

      var row = $('<div class="row">')
      row.appendTo(container)

      // create the buttons

      var buttons_div = $('<div class="col-md-2">')
      buttons_div.appendTo(row)

      reset_button = $('<button type="button" class="btn btn-secondary">'
         ).text("Reset").appendTo(buttons_div)
      reset_button.editors = editors

      check_button = $('<button type="button" class="btn btn-primary">'
         ).text("Check").appendTo(buttons_div)
      check_button.editors = editors
      // Create the output area

      var output_div = $('<div class="col-md-8">')
      output_div.appendTo(row)

      var output_area = $('<div class="output_area">')
      output_area.appendTo(output_div)

      // Connect the buttons
      reset_button.on('click', function (x){
          output_area.empty()

          reset_button.editors.forEach(function (x){
             x.setValue(x.initial_contents)
             x.gotoLine(1)
          })
      })

      check_button.on('click', function (x){
         output_area.empty()

         // TODO: animate this
         $('<span>').text("Checking...").appendTo(output_area)
         query_check_result(example_name, check_button.editors, output_area)
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
