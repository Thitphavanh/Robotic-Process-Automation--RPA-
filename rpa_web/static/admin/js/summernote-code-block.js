/**
 * Summernote Code Block Plugin
 * Adds a custom button to insert code blocks with syntax highlighting
 */

(function(factory) {
    if (typeof define === 'function' && define.amd) {
        define(['jquery'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('jquery'));
    } else {
        factory(window.jQuery);
    }
}(function($) {
    $.extend(true, $.summernote.lang, {
        'en-US': {
            codeBlock: {
                insert: 'Insert Code Block',
                edit: 'Edit Code',
                remove: 'Remove Code',
                codeLanguage: 'Code Language',
                enterCode: 'Enter your code:',
            }
        }
    });

    $.extend($.summernote.options, {
        codeBlock: {
            languages: [
                { value: 'python', label: 'Python' },
                { value: 'javascript', label: 'JavaScript' },
                { value: 'bash', label: 'Bash/Shell' },
                { value: 'json', label: 'JSON' },
                { value: 'sql', label: 'SQL' },
                { value: 'yaml', label: 'YAML' },
                { value: 'html', label: 'HTML' },
                { value: 'css', label: 'CSS' },
                { value: 'php', label: 'PHP' },
                { value: 'java', label: 'Java' },
                { value: 'cpp', label: 'C++' },
                { value: 'csharp', label: 'C#' },
                { value: 'go', label: 'Go' },
                { value: 'rust', label: 'Rust' },
                { value: 'ruby', label: 'Ruby' },
            ]
        }
    });

    $.extend($.summernote.plugins, {
        'codeBlock': function(context) {
            var self = this;
            var ui = $.summernote.ui;
            var $editor = context.layoutInfo.editor;
            var options = context.options;
            var lang = options.langInfo;

            context.memo('button.codeBlock', function() {
                var button = ui.button({
                    contents: '<i class="fa fa-code"/> Code Block',
                    tooltip: lang.codeBlock.insert,
                    click: function() {
                        self.show();
                    }
                });

                return button.render();
            });

            this.show = function() {
                var $modal = $('<div class="modal fade" tabindex="-1" role="dialog">')
                    .html([
                        '<div class="modal-dialog" role="document">',
                        '  <div class="modal-content">',
                        '    <div class="modal-header">',
                        '      <h5 class="modal-title">Insert Code Block</h5>',
                        '      <button type="button" class="close" data-dismiss="modal" aria-label="Close">',
                        '        <span aria-hidden="true">&times;</span>',
                        '      </button>',
                        '    </div>',
                        '    <div class="modal-body">',
                        '      <div class="form-group">',
                        '        <label for="code-language">Programming Language:</label>',
                        '        <select class="form-control" id="code-language">',
                        '          <option value="python">Python</option>',
                        '          <option value="javascript">JavaScript</option>',
                        '          <option value="bash">Bash/Shell</option>',
                        '          <option value="json">JSON</option>',
                        '          <option value="sql">SQL</option>',
                        '          <option value="yaml">YAML</option>',
                        '          <option value="html">HTML</option>',
                        '          <option value="css">CSS</option>',
                        '          <option value="php">PHP</option>',
                        '          <option value="java">Java</option>',
                        '          <option value="cpp">C++</option>',
                        '          <option value="csharp">C#</option>',
                        '          <option value="go">Go</option>',
                        '          <option value="rust">Rust</option>',
                        '          <option value="ruby">Ruby</option>',
                        '        </select>',
                        '      </div>',
                        '      <div class="form-group">',
                        '        <label for="code-content">Code:</label>',
                        '        <textarea class="form-control" id="code-content" rows="10" ',
                        '                  style="font-family: monospace; font-size: 14px;" ',
                        '                  placeholder="Paste your code here..."></textarea>',
                        '      </div>',
                        '    </div>',
                        '    <div class="modal-footer">',
                        '      <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>',
                        '      <button type="button" class="btn btn-primary" id="insert-code-btn">Insert Code</button>',
                        '    </div>',
                        '  </div>',
                        '</div>',
                    ].join(''));

                $modal.appendTo('body');
                $modal.modal('show');

                $modal.find('#insert-code-btn').on('click', function() {
                    var language = $modal.find('#code-language').val();
                    var code = $modal.find('#code-content').val();

                    if (code.trim()) {
                        // Escape HTML entities
                        var escapedCode = code
                            .replace(/&/g, '&amp;')
                            .replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;')
                            .replace(/"/g, '&quot;')
                            .replace(/'/g, '&#039;');

                        // Create code block with language class for syntax highlighting
                        var codeBlock = [
                            '<pre class="code-block" data-language="' + language + '" style="background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 15px 0;">',
                            '<code class="language-' + language + '" style="font-family: Monaco, Menlo, \'Ubuntu Mono\', monospace; font-size: 14px; line-height: 1.5;">',
                            escapedCode,
                            '</code>',
                            '</pre>',
                            '<p><br></p>'
                        ].join('');

                        context.invoke('editor.pasteHTML', codeBlock);
                    }

                    $modal.modal('hide');
                });

                $modal.on('hidden.bs.modal', function() {
                    $modal.remove();
                });
            };
        }
    });
}));
