"""
Custom template tags for documentation with Markdown and Image support
"""
from django import template
from django.utils.safestring import mark_safe
import re
import html
import markdown
from markdown.extensions import fenced_code, tables, toc, nl2br, sane_lists
from markdown.extensions.codehilite import CodeHiliteExtension

register = template.Library()


@register.filter(name='render_content')
def render_content(content):
    """
    Render documentation content with enhanced code blocks
    Converts Summernote code blocks to Nextra-style code blocks with copy button
    """
    if not content:
        return ""

    # Pattern to match code blocks with language class
    pattern = r'<pre[^>]*>\s*<code class="language-(\w+)"[^>]*>(.*?)</code>\s*</pre>'

    def replace_code_block(match):
        language = match.group(1)
        code_content = match.group(2)

        # Decode HTML entities
        code_content = html.unescape(code_content)

        # Re-escape for HTML display
        escaped_code = html.escape(code_content)

        # Generate unique ID for this code block
        import hashlib
        block_id = hashlib.md5(code_content.encode()).hexdigest()[:8]

        # Create Nextra-style code block
        return f'''
<div class="code-block-wrapper" data-language="{language}">
    <div class="code-block-header">
        <span class="code-block-language">{language}</span>
        <button class="code-copy-button" data-code-id="code-{block_id}" title="Copy code">
            <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <svg class="check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        </button>
    </div>
    <pre class="code-block-pre"><code id="code-{block_id}" class="language-{language}">{escaped_code}</code></pre>
</div>
        '''

    # Replace all code blocks
    result = re.sub(pattern, replace_code_block, content, flags=re.DOTALL)

    return mark_safe(result)


@register.simple_tag
def code_block(code, language="python", filename=""):
    """
    Template tag to create a code block with copy functionality
    Usage: {% code_block code_string "python" "example.py" %}
    """
    import hashlib
    import html

    # Escape HTML
    escaped_code = html.escape(code)

    # Generate unique ID
    block_id = hashlib.md5(code.encode()).hexdigest()[:8]

    # Build header
    header_content = f'<span class="code-block-language">{language}</span>'
    if filename:
        header_content = f'<span class="code-block-filename">{filename}</span><span class="code-block-language">{language}</span>'

    html_output = f'''
<div class="code-block-wrapper" data-language="{language}">
    <div class="code-block-header">
        {header_content}
        <button class="code-copy-button" data-code-id="code-{block_id}" title="Copy code">
            <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <svg class="check-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
        </button>
    </div>
    <pre class="code-block-pre"><code id="code-{block_id}" class="language-{language}">{escaped_code}</code></pre>
</div>
    '''

    return mark_safe(html_output)


@register.filter(name='render_markdown')
def render_markdown(content):
    """
    Render Markdown content to HTML with support for:
    - Fenced code blocks with syntax highlighting
    - Tables
    - Table of contents
    - Images with proper styling
    - Links
    - Lists
    """
    if not content:
        return ""

    # Configure markdown extensions
    extensions = [
        'markdown.extensions.fenced_code',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        CodeHiliteExtension(
            css_class='highlight',
            linenums=False,
            guess_lang=True
        ),
    ]

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=extensions)
    html_content = md.convert(content)

    # Enhance images with responsive classes
    html_content = re.sub(
        r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>',
        r'<img class="doc-image" src="\2" loading="lazy" \1\3>',
        html_content
    )

    # Wrap images in figure tags if they have alt text
    html_content = re.sub(
        r'<img class="doc-image" src="([^"]+)" loading="lazy"[^>]*?alt="([^"]+)"[^>]*?>',
        r'<figure class="doc-figure"><img class="doc-image" src="\1" loading="lazy" alt="\2"><figcaption>\2</figcaption></figure>',
        html_content
    )

    # Add target="_blank" to external links
    html_content = re.sub(
        r'<a href="(http[s]?://[^"]+)"',
        r'<a href="\1" target="_blank" rel="noopener noreferrer"',
        html_content
    )

    return mark_safe(html_content)


@register.simple_tag
def doc_image(url, alt="", caption="", width=""):
    """
    Template tag to create a responsive documentation image
    Usage: {% doc_image "https://example.com/image.jpg" "Alt text" "Caption" "800px" %}
    """
    width_style = f'max-width: {width};' if width else ''

    html_output = f'''
    <figure class="doc-figure" style="{width_style}">
        <img class="doc-image" src="{url}" alt="{alt}" loading="lazy">
        {f'<figcaption>{caption or alt}</figcaption>' if (caption or alt) else ''}
    </figure>
    '''

    return mark_safe(html_output)


@register.simple_tag
def youtube_embed(video_id, title="Video"):
    """
    Template tag to embed YouTube video
    Usage: {% youtube_embed "dQw4w9WgXcQ" "Video Title" %}
    """
    html_output = f'''
    <div class="video-container">
        <iframe
            src="https://www.youtube.com/embed/{video_id}"
            title="{title}"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
            loading="lazy"
        ></iframe>
    </div>
    '''

    return mark_safe(html_output)
