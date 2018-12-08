function replaceSelection(cm, active, startEnd) {
  var text;
  var start = startEnd[0];
  var end = startEnd[1];
  var startPoint = cm.getCursor("start");
  var endPoint = cm.getCursor("end");
  if(active) {
    text = cm.getLine(startPoint.line);
    start = text.slice(0, startPoint.ch);
    end = text.slice(startPoint.ch);
    cm.replaceRange(start + end, {
      line: startPoint.line,
      ch: 0
    });
  } else {
    text = cm.getSelection();
    cm.replaceSelection(start + text + end);

    startPoint.ch += start.length;
    if(startPoint !== endPoint) {
      endPoint.ch += start.length;
    }
  }
  cm.setSelection(startPoint, endPoint);
  cm.focus();
}

function drawWikiLink(editor) {
  var cm = editor.codemirror;
  var stat = simplemde.getState(cm);
  replaceSelection(cm, stat.link, ['[[',']]'], '');
}

var simplemde = new SimpleMDE({
  autoDownloadFontAwesome: false,
  toolbar: [
    'heading', 'bold', 'italic', 'strikethrough', '|',
    'quote', 'unordered-list', 'ordered-list', 'table', 'horizontal-rule', '|',
    { name: 'wikilink', className: 'fa fa-link', action: drawWikiLink, title: 'Wiki Link' },
    { name: 'link', className: 'fa fa-external-link', action: SimpleMDE.drawLink, title: 'Link' },
    'image', '|',
    'preview', 'side-by-side', 'fullscreen', 'guide',
  ],
  previewRender: function(plainText, preview) {
		preview.classList.add('content');
		return simplemde.markdown(plainText);
	},
  spellChecker: false,
});
