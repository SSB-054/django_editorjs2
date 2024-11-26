from typing import Dict, List, Any, Optional
import nh3

# Convert size to human-readable format
def human_readable_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

class BlockEditorConverter:
    """
    A modular converter for transforming Block Editor JSON to HTML.
    Supports extensibility through custom block type handlers.
    """
    
    def __init__(self):
        # Default block type handlers
        self._block_handlers = {
            'paragraph': self._convert_paragraph,
            'header': self._convert_header,
            'list': self._convert_list,
            'quote': self._convert_quote,
            'code': self._convert_code,
            'image': self._convert_image,
            'embed': self._convert_embed,
             'checklist': self._convert_checklist,
            'table': self._convert_table,
            'delimiter': self._convert_delimiter,
            'attachment': self._convert_attachment
        }
    
    def _convert_checklist(self, block: Dict[str, Any]) -> Optional[str]:
        """
        Convert checklist block to HTML
        
        Example block structure:
        {
            "type": "checklist",
            "data": {
                "items": [
                    {"text": "Task 1", "checked": true},
                    {"text": "Task 2", "checked": false}
                ]
            }
        }
        """
        items = block.get('data', {}).get('items', [])
        
        if not items:
            return None
        
        checklist_items = []
        for item in items:
            text = item.get('text', '')
            checked = item.get('checked', False)
            
            # Use HTML5 checkbox input with disabled attribute
            checkbox = (
                f'<input type="checkbox" {"checked" if checked else ""} disabled>'
                f' <span>{self._sanitize_html(text)}</span>'
            )
            checklist_items.append(f'<li>{checkbox}</li>')
        
        return f'<ul style="list-style: none;">{" ".join(checklist_items)}</ul>'
    
    def _convert_table(self, block: Dict[str, Any]) -> Optional[str]:
        """
        Convert table block to HTML
        
        Example block structure:
        {
            "type": "table",
            "data": {
                "content": [
                    ["Header 1", "Header 2"],
                    ["Row 1, Cell 1", "Row 1, Cell 2"],
                    ["Row 2, Cell 1", "Row 2, Cell 2"]
                ]
            }
        }
        """
        content = block.get('data', {}).get('content', [])
        
        if not content:
            return None
        
        # First row is considered headers
        headers = content[0]
        body_rows = content[1:]
        
        # Generate table headers
        headers_html = ''.join(f'<th>{self._sanitize_html(header)}</th>' for header in headers)
        header_row = f'<thead><tr>{headers_html}</tr></thead>'
        
        # Generate table body rows
        body_rows_html = []
        for row in body_rows:
            row_cells = ''.join(f'<td>{self._sanitize_html(cell)}</td>' for cell in row)
            body_rows_html.append(f'<tr>{row_cells}</tr>')
        
        body_html = f'<tbody>{"".join(body_rows_html)}</tbody>'
        
        return f'<table class="block-editor-table">{header_row}{body_html}</table>'
    
    def _convert_delimiter(self, block: Dict[str, Any]) -> str:
        """
        Convert delimiter block to HTML
        
        Simple horizontal rule to separate content
        """
        return '<hr class="block-editor-delimiter" />'
    
    def _convert_attachment(self, block: Dict[str, Any]) -> Optional[str]:
        """
        Convert attachment block to HTML
        
        Example block structure:
        {
            "type": "attachment",
            "data": {
                "file": {
                    "url": "https://example.com/file.pdf",
                    "name": "Document.pdf",
                    "size": 1024
                },
                "caption": "Optional file description"
            }
        }
        """
        file_data = block.get('data', {}).get('file', {})
        caption = block.get('data', {}).get('caption', '')
        
        url = file_data.get('url', '')
        name = file_data.get('name', 'Attachment')
        size = file_data.get('size', 0)
        
        if not url:
            return None
        
        
        
        readable_size = human_readable_size(size)
        
        attachment_html = (
            f'<div class="block-editor-attachment">'
            f'  <a href="{url}" target="_blank" download>'
            f'    📄 {self._sanitize_html(name)} ({readable_size})'
            f'  </a>'
        )
        
        if caption:
            attachment_html += f'  <p class="attachment-caption">{self._sanitize_html(caption)}</p>'
        
        attachment_html += '</div>'
        
        return attachment_html    
    
    def _convert_blocks(self, block_data: Dict[str, Any]) -> str:
        """
        Convert Block Editor JSON to HTML.
        
        :param block_data: Block Editor JSON data
        :return: Converted HTML string
        """
        if not isinstance(block_data, dict) or 'blocks' not in block_data:
            raise ValueError("Invalid block editor data format")
        
        for block in block_data.get('blocks', []):
            block_type = block.get('type', '')
            if block_type in self._block_handlers:
                handler = self._block_handlers.get(block_type)
                yield handler(block)
    
    def convert(self, block_data: Dict[str, Any]) -> str:
        return "".join(self._convert_blocks(block_data))
    
    def _convert_paragraph(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert paragraph block to HTML"""
        text = block.get('data', {}).get('text', '')
        return f'<p>{self._sanitize_html(text)}</p>' if text else None
    
    def _convert_header(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert header block to HTML"""
        text = block.get('data', {}).get('text', '')
        level = block.get('data', {}).get('level', 2)
        level = max(1, min(level, 6))  # Ensure header is between h1-h6
        return f'<h{level}>{self._sanitize_html(text)}</h{level}>' if text else None
    
    def _convert_list(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert list block to HTML"""
        style = block.get('data', {}).get('style', 'unordered')
        items = block.get('data', {}).get('items', [])
        
        if not items:
            return None
        
        list_tag = 'ul' if style == 'unordered' else 'ol'
        list_items = ''.join(f'<li>{self._sanitize_html(item)}</li>' for item in items)
        return f'<{list_tag}>{list_items}</{list_tag}>'
    
    def _convert_quote(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert quote block to HTML"""
        text = block.get('data', {}).get('text', '')
        caption = block.get('data', {}).get('caption', '')
        
        if not text:
            return None
        
        quote_html = f'<blockquote>{self._sanitize_html(text)}</blockquote>'
        if caption:
            quote_html += f'<cite>{self._sanitize_html(caption)}</cite>'
        
        return quote_html
    
    def _convert_code(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert code block to HTML"""
        code = block.get('data', {}).get('code', '')
        language = block.get('data', {}).get('language', '')
        
        if not code:
            return None
        
        # Optional language class for syntax highlighting
        lang_class = f' class="language-{language}"' if language else ''
        return f'<pre><code{lang_class}>{self._sanitize_html(code)}</code></pre>'
    
    def _convert_image(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert image block to HTML"""
        url = block.get('data', {}).get('file', {}).get('url', '')
        caption = block.get('data', {}).get('caption', '')
        if not url:
            return None
        
        img_html = f'<img src="{url}" alt="{self._sanitize_html(caption)}" style="">'
        if caption:
            img_html = f'<figure>{img_html}<figcaption>{self._sanitize_html(caption)}</figcaption></figure>'
        
        return img_html
    
    def _convert_embed(self, block: Dict[str, Any]) -> Optional[str]:
        """Convert embed block to HTML"""
        service = block.get('data', {}).get('service', '')
        source = block.get('data', {}).get('source', '')
        
        if not source:
            return None
        
        # Basic embed handlers for common services
        if service == 'youtube':
            return f'<iframe src="https://www.youtube.com/embed/{source}" allowfullscreen></iframe>'
        elif service == 'vimeo':
            return f'<iframe src="https://player.vimeo.com/video/{source}" allowfullscreen></iframe>'
        
        return None
    
    def _sanitize_html(self, text: str) -> str:
        """
        Basic HTML sanitization to prevent XSS.
        
        :param text: Input text to sanitize
        :return: Sanitized HTML-safe text
        """
        return nh3.clean(text)

converter = BlockEditorConverter()
    