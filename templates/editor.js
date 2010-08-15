goog.require('goog.dom');
goog.require('goog.events');
goog.require('goog.events.KeyCodes');
goog.require('goog.net.XhrIo');
goog.require('goog.Uri');

    goog.require('goog.editor.Command');
    goog.require('goog.editor.Field');
    goog.require('goog.editor.plugins.BasicTextFormatter');
    goog.require('goog.editor.plugins.EnterHandler');
    goog.require('goog.editor.plugins.HeaderFormatter');
    goog.require('goog.editor.plugins.ListTabHandler');
    goog.require('goog.editor.plugins.LinkBubble');
    goog.require('goog.editor.plugins.LinkDialogPlugin');
    goog.require('goog.editor.plugins.LoremIpsum');
    goog.require('goog.editor.plugins.RemoveFormatting');
    goog.require('goog.editor.plugins.SpacesTabHandler');
    goog.require('goog.editor.plugins.UndoRedo');
    goog.require('goog.ui.editor.DefaultToolbar');
    goog.require('goog.ui.editor.ToolbarController');


function setupEditors() {

  goog.array.map(goog.dom.$$("div", "node"), 
    function(element) {
      var nodepath = element.id;
      goog.events.listen(element, 
        goog.events.EventType.DBLCLICK, function(event) { 
          if (element.editable) {
            return;
          };
          event.preventDefault();
          goog.net.XhrIo.send(nodepath + ".json",
              function(e) { 
                var node = e.target.getResponseJson()[0].fields;
                element.editable = true;
                makeEditable(node, element, node.title.trim(), node.content.trim());
              });
       }
      );
    }
  );
}

function saveEdit(node, element, titleElement, contentElement) {
  node.title = titleElement.getCleanContents();
  node.content = contentElement.getCleanContents();
  var data = goog.Uri.QueryData.createFromMap(node);
  function onsave(e) {
    var node = e.target.getResponseJson()[0].fields;
    element.editable = false;
    //var title = element.prev.title;
    //var content = element.prev.content;
    //goog.dom.removeChildren(title);
    //goog.dom.appendChild(title, goog.dom.createTextNode(node.title));
    //goog.dom.removeChildren(content);
    //goog.dom.appendChild(content, goog.dom.htmlToDocumentFragment(node.content));
    contentElement.makeUneditable();
    titleElement.makeUneditable();
  };
  goog.net.XhrIo.send('/node' + node.path + ".json", onsave, 'POST', data.toString(0));
}

function makeEditable(node, element, inputText, contentText) {
  var title = goog.dom.getElementsByTagNameAndClass('h1', 'title', element)[0];
  var content = goog.dom.getElementsByTagNameAndClass('div', 'content', element)[0];
  var textarea = new goog.editor.Field('/node' + node.path + '/content');
  var input = new goog.editor.Field('/node' + node.path + '/title');
  //textarea.value = contentText;
  textarea.registerPlugin(new goog.editor.plugins.BasicTextFormatter());
  textarea.registerPlugin(new goog.editor.plugins.RemoveFormatting());
  textarea.registerPlugin(new goog.editor.plugins.UndoRedo());
  textarea.registerPlugin(new goog.editor.plugins.ListTabHandler());
  textarea.registerPlugin(new goog.editor.plugins.SpacesTabHandler());
  textarea.registerPlugin(new goog.editor.plugins.EnterHandler());
  textarea.registerPlugin(new goog.editor.plugins.HeaderFormatter());
  //textarea.registerPlugin(
  //    new goog.editor.plugins.LoremIpsum('Click here to edit'));
  textarea.registerPlugin(
   new goog.editor.plugins.LinkDialogPlugin());
  textarea.registerPlugin(new goog.editor.plugins.LinkBubble());
 


 var buttons = [
    goog.editor.Command.BOLD,
    goog.editor.Command.ITALIC,
    goog.editor.Command.UNDERLINE,
    goog.editor.Command.LINK,
    /*goog.editor.Command.UNORDERED_LIST,
    goog.editor.Command.ORDERED_LIST,
    goog.editor.Command.JUSTIFY_LEFT,
    goog.editor.Command.JUSTIFY_CENTER,
    goog.editor.Command.JUSTIFY_RIGHT,
    goog.editor.Command.SUBSCRIPT,
    goog.editor.Command.SUPERSCRIPT,
    goog.editor.Command.STRIKE_THROUGH,
    goog.editor.Command.REMOVE_FORMAT
    */
  ];

  var myToolbar = goog.ui.editor.DefaultToolbar.makeToolbar(buttons,
      goog.dom.$('/node' + node.path + '/toolbar'));
  var myToolbarController =
      new goog.ui.editor.ToolbarController(textarea, myToolbar);
  function updateFieldContents() {
    console.log(textarea.getCleanContents());
  }

  goog.events.listen(textarea, goog.editor.Field.EventType.DELAYEDCHANGE,
      updateFieldContents);
  textarea.makeEditable();
  input.makeEditable();
  //var save = goog.dom.createDom('div', null, "save");
  //goog.dom.removeChildren(title);
  //goog.dom.appendChild(title, input);
  //goog.dom.removeChildren(content);
  //goog.dom.appendChild(content, textarea);
  //goog.dom.appendChild(title, save);
  goog.events.listen(textarea, goog.events.EventType.BLUR, function(event) {
    //saveEdit(node, element, input, textarea);
  }); 
  goog.events.listen(input, goog.events.EventType.BLUR, function(event) {
    //saveEdit(node, element, input, textarea);
  }); 
  goog.events.listen(element, 'keypress', function(e) {
      if (e.keyCode == goog.events.KeyCodes.ENTER) {
        saveEdit(node, element, input, textarea);
      }
  }); 
  input.focus();
  element.prev = {};
  element.prev.title = title;
  element.prev.content = content;
}
