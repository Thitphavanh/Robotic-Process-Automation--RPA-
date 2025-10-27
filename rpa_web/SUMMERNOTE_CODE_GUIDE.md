# Summernote Code Block Guide

## Overview
The RPA Bot documentation system now supports rich text editing with **syntax-highlighted code blocks** using Summernote WYSIWYG editor.

## Features

### 1. **Code Block Button**
- Custom "Code Block" button in the Summernote toolbar
- Easy-to-use modal dialog for inserting code
- Support for 15+ programming languages

### 2. **Supported Languages**
- Python
- JavaScript
- Bash/Shell
- JSON
- SQL
- YAML
- HTML
- CSS
- PHP
- Java
- C++
- C#
- Go
- Rust
- Ruby

### 3. **Syntax Highlighting**
- Powered by Prism.js
- Dark theme (Prism Tomorrow theme)
- Automatic code formatting
- Line numbers support

## How to Use

### Adding Code Examples in Admin Panel

1. **Navigate to Documentation Section**
   - Go to Django Admin: `/admin/`
   - Click on "เอกสาร Documentation" (Doc Sections)
   - Click on any section to edit (e.g., "Overview", "API Reference")

2. **Insert Code Block**
   - In the "เนื้อหา" (Content) field, you'll see the Summernote editor
   - Click the **"Code Block"** button in the toolbar (icon with `</>`)
   - A modal dialog will appear

3. **Fill in Code Details**
   - **Programming Language**: Select from dropdown (Python, JavaScript, etc.)
   - **Code**: Paste or type your code in the textarea
   - Click **"Insert Code"** button

4. **Save Document**
   - Click "Save" or "Save and continue editing"
   - Your code will be displayed with syntax highlighting

### Example: Inserting Python Code

1. Click "Code Block" button
2. Select "Python" from language dropdown
3. Paste code:
```python
from rpa_bot.models import DocSection

# Get all active documentation sections
sections = DocSection.objects.filter(is_active=True)

for section in sections:
    print(f"{section.title} - {section.description}")
```
4. Click "Insert Code"

### Example: Inserting Bash Commands

1. Click "Code Block" button
2. Select "Bash/Shell" from language dropdown
3. Paste code:
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```
4. Click "Insert Code"

### Example: Inserting JSON Data

1. Click "Code Block" button
2. Select "JSON" from language dropdown
3. Paste code:
```json
{
  "title": "API Reference",
  "slug": "api-reference",
  "group": "advanced",
  "order": 1,
  "is_active": true
}
```
4. Click "Insert Code"

## Advanced Features

### Using Content Blocks (Alternative Method)

For more complex documentation with multiple content types:

1. **Navigate to Doc Section**
2. **Scroll to "Content Blocks" inline section**
3. **Add new block**:
   - Block Type: Select "โค้ด" (Code)
   - Content: Paste your code
   - Code Language: Enter language (python, javascript, etc.)
   - Order: Set display order
   - Is Active: Check to enable

### HTML Code View

Summernote also includes a raw HTML editor:

1. Click **"Code View"** button (icon with `</>` in toolbar)
2. Edit raw HTML directly
3. You can manually add code blocks:
```html
<pre class="code-block" data-language="python" style="background-color: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px;">
<code class="language-python">
def hello_world():
    print("Hello, World!")
</code>
</pre>
```
4. Click "Code View" again to return to visual mode

## Tips & Best Practices

### 1. **Code Formatting**
- Use proper indentation before pasting
- Remove unnecessary blank lines
- Keep code examples concise and focused

### 2. **Language Selection**
- Always select the correct language for accurate highlighting
- For generic text/pseudocode, use "bash" or "python"

### 3. **Code Length**
- For long code examples (100+ lines), consider:
  - Breaking into smaller sections
  - Using Content Blocks for better organization
  - Adding comments to explain complex parts

### 4. **Security**
- Never include sensitive information (API keys, passwords, etc.)
- Use placeholder values like `YOUR_API_KEY` or `example.com`

### 5. **Testing**
- Always preview your documentation after adding code
- Check that syntax highlighting works correctly
- Verify code blocks are readable on both light and dark themes

## Styling Reference

### Default Code Block Styles

```css
.code-block {
    background-color: #2d2d2d;
    color: #f8f8f2;
    padding: 15px;
    border-radius: 5px;
    overflow-x: auto;
    margin: 15px 0;
    font-family: Monaco, Menlo, 'Ubuntu Mono', monospace;
    font-size: 14px;
    line-height: 1.5;
}
```

## Troubleshooting

### Code Block Button Not Showing

1. Clear browser cache
2. Run `python manage.py collectstatic --noinput`
3. Refresh admin page (Ctrl+F5 or Cmd+Shift+R)

### Syntax Highlighting Not Working

1. Check that Prism.js CSS is loading:
   - Open browser dev tools (F12)
   - Check Network tab for `prism-tomorrow.min.css`
2. Verify code block has correct language class:
   - Inspect element and look for `class="language-python"`

### Code Not Saving

1. Ensure Content Security Policy allows inline styles
2. Check for JavaScript errors in browser console
3. Verify `SUMMERNOTE_CONFIG` in `settings/base.py`

## Configuration Files

### Settings: `config/settings/base.py`
```python
SUMMERNOTE_CONFIG = {
    'summernote': {
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'strikethrough', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']],
            ['mybutton', ['codeBlock']],
        ],
        'width': '100%',
        'height': '480',
    },
}
```

### Admin: `rpa_bot/admin.py`
```python
@admin.register(DocSection)
class DocSectionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

    class Media:
        js = ('admin/js/summernote-code-block.js',)
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css',)
        }
```

## Next Steps

After adding code examples to your documentation:

1. **Preview Documentation**: Visit `/docs/overview/` to see your changes
2. **Create Examples**: Add practical code examples to each section
3. **Test Code**: Ensure code examples actually work
4. **Add Context**: Explain what each code example does
5. **Cross-Reference**: Link related documentation sections

## Support

For issues or questions:
- Check Django Admin logs
- Review browser console for JavaScript errors
- Consult Summernote documentation: https://summernote.org/
- Check Prism.js documentation: https://prismjs.com/

---

**Last Updated**: 2025-10-27
**Version**: 1.0
