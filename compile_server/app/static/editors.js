// Log an error message in the output area
function output_error(output_area, message) {
    var div = $('<div class="output_error">')
    div.text(message)
    div.appendTo(output_area)
}

// Process the result of a check
//  editors: the editors to decorate
//  output_area: the div where the messages should go
//  status: the exit status
//  message: any message coming back from the application
//   TODO: make use of message
function process_check_output(editors, output_area, output, status, completed, message) {
    // Process the lines

    read_lines = 0

    output.forEach(function (l) {
        read_lines++

        // Look for lines that contain an error message
        var match_found = l.match(/^([a-zA-Z._0-9-]+):(\d+):(\d+):(.+)$/)
        var klass = match_found ? "output_msg" : "output_line"

        // Print the line in the output area
        var div = $('<div class="' + klass + '">')
        div.text(l)
        div.appendTo(output_area)

        if (match_found != null) {
            output_area.error_count++

                // Lines that contain a sloc are clickable:
                div.on('click', function (x) {
                    // find the corresponding editor
                    var basename = match_found[1]
                    editors.forEach(function (e) {
                        if (e.basename == basename) {
                            // Switch to the tab that contains the editor

                            // TODO: this is in the case of bootstrap only
                            // $("#" + e.unique_id + "-tab").tab('show')

                            // Jump to the corresponding line
                            e.gotoLine(parseInt(match_found[2]),
                                // looks like column numbers are indexed from 0
                                parseInt(match_found[3] - 1),
                                true)
                            e.focus()
                        }
                    })
                })
        }
    })

    // Congratulations!
    if (completed) {
        if (status != 0) {
            output_error(output_area, "exit status: " + status)
        } else if (output_area.error_count == 0) {
            var div = $('<div class="output_success">')
            div.text("Success!")
            div.appendTo(output_area)
        } else if (output_area.error_count == 1) {
            var div = $('<div class="output_info">')
            div.text("One error.")
            div.appendTo(output_area)
        } else {
            var div = $('<div class="output_info">')
            div.text(output_area.error_count + " errors.")
            div.appendTo(output_area)
        }
    }

    return read_lines
}

function get_output_from_identifier(container, editors, output_area, identifier, already_read) {
    data = {
        "identifier": identifier,
        "already_read": already_read
    }
    $.ajax({
            url: container.example_server + "/check_output/",
            data: JSON.stringify(data),
            type: "POST",
            dataType: "json",
            contentType: 'application/json; charset=UTF-8',
        })
        .done(function (json) {
            read_lines = process_check_output(
                editors, output_area,
                json.output_lines, json.status, json.completed, json.message
            )
            if (!json.completed) {
                // We have not finished processing the output: call this again
                setTimeout(function () {
                    get_output_from_identifier(container, editors, output_area, identifier, already_read + read_lines)
                }, 250)
            }
        })
        .fail(function (xhr, status, errorThrown) {
            output_error(output_area, "could not download output")
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
        .fail(function (json) {
            output_error(output_area, json.message)
        })
}


// Launch a run on the given example editor
function query_operation_result(container, example_name, editors, output_area, operation_url) {

    files = []

    // Grab the contents from actual editors
    editors.forEach(function (e) {
        files.push({
            'basename': e.basename,
            'contents': e.getValue()
        })
    })

    // Grab the contents from shadow files
    if (container.shadow_files){
      container.shadow_files.forEach(function (e){
        files.push({
            'basename': e.basename,
            'contents': e.contents
            });
      });
    }

    data = {
        "example_name": example_name,
        "files": files,
        "main": container.attr("main"),
        "extra_args": container.attr("extra_args"),
    }


    // request the examples
    $.ajax({
            url: container.example_server + operation_url,
            data: JSON.stringify(data),
            type: "POST",
            dataType: "json",
            contentType: 'application/json; charset=UTF-8',
        })
        .done(function (json) {
            if (json.identifier == "") {
                output_error(output_area, json.message)
            } else {
                get_output_from_identifier(container, editors, output_area, json.identifier, 0)
            }
        })
        .fail(function (xhr, status, errorThrown) {
            //
            alert("could not run the example");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        })
}


function create_editor(resource, container, content, editors, counter) {
   var the_id = "tab_" + container.attr("the_id") + "-" + counter
   var div = $('<div role="tabpanel" class="tab-pane' +
       (counter == 1 ? ' active' : '') +
       '" id="' + the_id + '">');
   var editordiv = $('<div class="editor_container' + (is_inline?' inline':'') + '"'
                     + ' id="' + resource.basename + the_id + '_editor">');
   editordiv.appendTo(div);
   div.appendTo(content);

   // ACE editors...
   var editor = ace.edit(resource.basename + the_id + '_editor');
   editor.session.setMode("ace/mode/ada");

   // ... and their contents
   editor.setValue(resource.contents);
   editor.setShowPrintMargin(false);
   editor.gotoLine(1);
   editor.initial_contents = resource.contents;
   editor.basename = resource.basename;
   editor.unique_id = the_id;

   editor.setOptions({
       "highlightActiveLine": false,
   });

   // check if we are overriding db content with inline content
   if (container.attr("inline")) {
       $(container).children(".resource").each(function () {
           if ($(this).attr("region")) {
               region = $(this).attr("region");

               // search editor content for region "region"
               beginregion = editor.find("--  #region " + region);
               endregion = editor.find("--  #endregion " + region);

               newRange = beginregion.clone();
               newRange.end.row = endregion.end.row;
               newRange.end.column = endregion.end.column;

               textReplace = $(this).text().replace(/^\s|\s+$/g, '');

               editor.getSession().getDocument().replace(newRange, textReplace);
               $(this).text('');
           }
          else {
             // No region: replace the whole editor
             editor.initial_contents = $(this).text();
             editor.setValue($(this).text());
             $(this).text('');
          }
       })
   }

   // search for remaining region marks and remove
   editor.replaceAll("", {
       needle: "--  #region (.*)\n",
       regExp: true
   });
   editor.replaceAll("", {
       needle: "--  #endregion (.*)\n",
       regExp: true
   });

   // check if container is readonly
   if (container.attr("readonly")) {
       // remove all read only tags in the editor
       editor.replaceAll("", {
           needle: "--  (begin|end) readonly",
           regExp: true
       });

       editor.setOption("readOnly", true);
   } else {
       // look for readonly sections
       roStack = [];
       roList = [];
       editor.setOption("readOnly", false);
       selection = editor.getSession().getSelection();
       selection.clearSelection();
       selection.moveCursorFileStart();

       while (tag = editor.find("--  (begin|end) readonly", {
               regExp: true,
               wrap: false
           })) {
           var str = editor.getSession().getDocument().getTextRange(tag);
           var re = new RegExp('--  (begin|end) readonly');
           var type = re.exec(str)[1];

           if (type == "begin") {
               roStack.push(tag);
           } else {
               if (roStack.length == 0) {
                   tag.start.row = 0;
                   tag.start.column = 0;

               } else {
                   var beginRange = roStack.pop();
                   tag.start = beginRange.start;
               }
               roList.push(tag);
           }
       }

       while (roStack.length > 0) {
           var beginRange = roStack.pop();
           var numRows = editor.getSession().getLength() - 1;
           var numCols = editor.getSession().getLine(numRows).length;

           beginRange.end.row = numRows;
           beginRange.end.column = numCols;

           roList.push(beginRange);
       }

       selection.clearSelection();
       for (var i = 0; i < roList.length; i++) {
           selection.addRange(roList[i]);
       }

       selection.mergeOverlappingRanges();
       editor.readOnlyRanges = selection.getAllRanges();

       // hijack keyboard commands on editor
       editor.keyBinding.addKeyboardHandler({
           handleKeyboard: function (data, hash, keyString, keyCode, event) {
               if (Math.abs(keyCode) == 13 && onEnd(editor.getCursorPosition())) {
                   return false;
               }
               if (hash === -1 || (keyCode <= 40 && keyCode >= 37)) return false;
               for (i = 0; i < editor.readOnlyRanges.length; i++) {
                   if (intersects(editor.readOnlyRanges[i])) {
                       return {
                           command: "null",
                           passEvent: false
                       };
                   }
               }
           }
       });

       before(editor, 'onPaste', preventReadonly);
       before(editor, 'onCut', preventReadonly);

       function before(obj, method, wrapper) {
           var orig = obj[method];
           obj[method] = function () {
               var args = Array.prototype.slice.call(arguments);
               return wrapper.call(this, function () {
                   return orig.apply(obj, args);
               }, args);
           }

           return obj[method];
       }

       function intersects(range) {
           return editor.getSelectionRange().intersects(range);
       }

       function intersectsRange(newRange) {
           for (var i = 0; i < editor.readOnlyRanges.length; i++) {
               if (newRange.intersects(editor.readOnlyRanges[i])) {
                   return true;
               }
           }
           return false;
       }

       function preventReadonly(next, args) {
           for (var i = 0; i < editor.readOnlyRanges.length; i++) {
               if (intersects(editor.readOnlyRanges[i]))
                   return;
           }
           next();
       }

       function onEnd(position) {
           var row = position["row"];
           var column = position["column"];

           for (var i = 0; i < editor.readOnlyRanges.length; i++) {
               if (editor.readOnlyRanges[i].end["row"] == row && editor.readOnlyRanges[i].end["column"] == column) {
                   return true;
               }
           }
           return false;
       }

       function outSideRange(position) {
           var row = position["row"];
           var column = position["column"];

           for (var i = 0; i < editor.readOnlyRanges.length; i++) {
               if (editor.readOnlyRanges[i].start["row"] < row && editor.readOnlyRanges[i].end["row"] > row) {
                   return false;
               }

               if (editor.readOnlyRanges[i].start["row"] == row && editor.readOnlyRanges[i].start["column"] < column) {
                   if (editor.readOnlyRanges[i].end["row"] != row || editor.readOnlyRanges[i].end["column"] > column) {
                       return false;
                   }
               } else if (editor.readOnlyRanges[i].end["row"] == row && editor.readOnlyRanges[i].end["column"] > column) {
                   return false;
               }
           }
           return true;
       }

       for (var i = 0; i < editor.readOnlyRanges.length; i++) {
           // add readonly class to lines
           editor.getSession().addMarker(editor.readOnlyRanges[i], "read-only");

           // add anchors around ro sections
           editor.readOnlyRanges[i].start = editor.getSession().getDocument().createAnchor(editor.readOnlyRanges[i].start);
           editor.readOnlyRanges[i].end = editor.getSession().getDocument().createAnchor(editor.readOnlyRanges[i].end);
           editor.readOnlyRanges[i].end.$insertRight = true;

           // TODO: add folding mode to ada definition then uncomment the following
           //editor.getSession().addFold("read only", editor.readOnlyRanges[i]);
       }

       // remove all read only tags in the editor
       editor.replaceAll("", {
           needle: "--  (begin|end) readonly",
           regExp: true
       });

       var old$tryReplace = editor.$tryReplace;
       editor.$tryReplace = function (range, replacement) {
           return intersectsRange(range) ? null : old$tryReplace.apply(this, arguments);
       }
       var session = editor.getSession();
       var oldInsert = session.insert;
       session.insert = function (position, text) {
           return oldInsert.apply(this, [position, outSideRange(position) ? text : ""]);
       }
       var oldRemove = session.remove;
       session.remove = function (range) {
           return intersectsRange(range) ? false : oldRemove.apply(this, arguments);
       }
       var oldMoveText = session.moveText;
       session.moveText = function (fromRange, toPosition, copy) {
           if (intersectsRange(fromRange) || !outSideRange(toPosition)) return fromRange;
           return oldMoveText.apply(this, arguments);
       }
   }

   // Inline? set the editor to use exactly the vertical space it needs
   if (is_inline){
       editor.setOptions({
            maxLines: editor.session.getLength()
       })
   }

   // place the cursor at 1,1
   editor.selection.moveTo(0, 0);

   // clear undo stack to avoid undoing everything we just did
   editor.getSession().getUndoManager().reset();

   return editor;
}

// Fills a <div> with an editable representation of an example.
//    container: the <div> in question
//    example_name: the name of the example to load

var unique_id = 0

function fill_editor_from_contents(container, example_name, example_server,
                                   resources, main) {

   is_inline = container.attr("inline")

   // First create the tabs

   if (!is_inline){
      var ul = $('<ul class="nav nav-tabs" role="tablist">')
      ul.appendTo(container);

      var counter = 0;

      resources.forEach(function (resource) {
          counter++;
          var the_id = "tab_" + container.attr("the_id") + "-" + counter

          var li = $('<li role="presentation" class="' +
              (counter == 1 ? 'active' : '') +
              '">').appendTo(ul);
          $('<a href="#' + the_id + '" aria-controls="' +
              the_id + '" ' +
              'id="' + the_id + '-tab"' +
              'role="tab" data-toggle="tab">' +
              resource.basename + '</a>').appendTo(li)
      })
   }

   // Then fill the contents of the tabs

   var content = $('<div class="tab-content">')
   content.appendTo(container);

   counter = 0;

   var editors = []

   resources.forEach(function (resource) {
       counter++;
       editor = create_editor(resource, container, content, editors, counter)
       // Append the editor to the list of editors
       editors.push(editor)
   })

   var row = $('<div class="row output_row">')
   row.appendTo(container)

   // create the buttons

   var buttons_div = $('<div class="col-md-3">')
   buttons_div.appendTo(row)

   var output_div = $('<div class="col-md-9">')
   output_div.appendTo(row)

   var output_area = $('<div class="output_area">')
   output_area.appendTo(output_div)

   if (container.attr("prove_button") || container.attr("run_button")){
      var reset_button = $('<button type="button" class="btn btn-secondary">').text("Reset").appendTo(buttons_div)
      reset_button.editors = editors;
      reset_button.on('click', function (x) {
          output_area.empty();
          output_area.error_count = 0;

          reset_button.editors.forEach(function (x) {
              x.setValue(x.initial_contents);
              x.gotoLine(1);
          })
      })
   }

   if (container.attr("prove_button")){
      var check_button = $('<button type="button" class="btn btn-primary">').text("Prove").appendTo(buttons_div)
      check_button.editors = editors;
      check_button.on('click', function (x) {
          output_area.empty();
          output_area.error_count = 0;

          var div = $('<div class="output_info">');
          div.text("Proving...");
          div.appendTo(output_area);
          query_operation_result(container, example_name, check_button.editors, output_area, "/check_program/");
       })
   }

   if (container.attr("run_button")){
       var run_button = $('<button type="button" class="btn btn-primary">').text("Run").appendTo(buttons_div);
       run_button.editors = editors;
       run_button.on('click', function (x) {
           output_area.empty();
           output_area.error_count = 0;

           var div = $('<div class="output_info">');
           div.text("Running...");
           div.appendTo(output_area);
           query_operation_result(container, example_name, run_button.editors, output_area, "/run_program/");
       })
   }
}

function fill_editor(container, example_name, example_server) {
    unique_id++;
    container.attr("the_id", unique_id);
    container.example_server = example_server;

    is_inline = container.attr("inline");

    if (is_inline){
       // In inline mode, just assume all the sources are here, do not
       // request them in AJAX

       // List the "file" divs, add these as resources
       var resources = []
       $(container).children(".file").each(function () {
          // Create a fake resource for each 'file' div
          a = Object();
          a.basename = $(this).attr("basename");
          a.contents = $(this).text();
          $(this).text('');
          resources.push(a);
       })

       // List the contents of the ".shadow_file" divs
       container.shadow_files = []
       $(container).children(".shadow_file").each(function () {
          // Create a fake resource for each 'file' div
          a = Object();
          a.basename = $(this).attr("basename");
          a.contents = $(this).text();
          $(this).text('');
          container.shadow_files.push(a);
       })

       fill_editor_from_contents(container, example_name, example_server,
                                 resources, container.attr("main"));
    } else {

       // request the examples
       $.ajax({
               url: container.example_server + "/example/" + example_name,
               data: {},
               type: "GET",
               // dataType : "json",
               contentType: 'text/plain',
               crossDomain: true,
               //      headers: { "Origin": "http://www.adacore.com" }

           })
           .done(function (json) {
               // On success, create editors for each of the resources

               fill_editor_from_contents(container, example_name, example_server,
                                         json.resources, json.main);

               })
           .fail(function (xhr, status, errorThrown) {
               alert("could not download the example");
               console.log("Error: " + errorThrown);
               console.log("Status: " + status);
               console.dir(xhr);
           });
        }
}


// Called when the document is ready
$(document).ready(function () {

    // Iterate on all divs, finding those that have the "example_editor"
    // attribute
    $("div").each(function (index, element) {
        example_name = $(this).attr("example_editor");
        example_server = $(this).attr("example_server");
        if (!example_server) {
            example_server = '';
        }
        if (example_name) {
            fill_editor($(this), example_name, example_server);
        }
    })
});
