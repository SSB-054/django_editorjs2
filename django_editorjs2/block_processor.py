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
            'attaches': self._convert_attachment
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
                stretched: false,
                withHeadings: true,
                "content": [
                    ["Header 1", "Header 2"],
                    ["Row 1, Cell 1", "Row 1, Cell 2"],
                    ["Row 2, Cell 1", "Row 2, Cell 2"]
                ]
            }
        }
        """
        # Extract data with default values
        data = block.get('data', {})
        content = data.get('content', [])
        
        # Handle new variables with explicit checks
        stretched = data.get('stretched', False)
        with_headings = data.get('withHeadings', True)
        
        if not content:
            return None
    
        # Determine table classes based on new variables
        table_classes = ["block-editor-table"]
        if stretched:
            table_classes.append("block-editor-table-stretched")
        
        # Generate table headers (only if with_headings is True)
        if with_headings and content:
            headers = content[0]
            headers_html = ''.join(f'<th>{self._sanitize_html(header)}</th>' for header in headers)
            header_row = f'<thead><tr>{headers_html}</tr></thead>'
            body_rows = content[1:]
        else:
            header_row = ''
            body_rows = content
        
        # Generate table body rows
        body_rows_html = []
        for row in body_rows:
            row_cells = ''.join(f'<td>{self._sanitize_html(cell)}</td>' for cell in row)
            body_rows_html.append(f'<tr>{row_cells}</tr>')
        
        body_html = f'<tbody>{"".join(body_rows_html)}</tbody>'
        
        # Construct the final table HTML with dynamic classes
        return f'<table class="{" ".join(table_classes)}">{header_row}{body_html}</table>'
    
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
        title = block.get('data', {}).get('title', '')
        
        url = file_data.get('url', '')
        name = file_data.get('name', 'Attachment')
        size = file_data.get('size', 0)
        
        if not url:
            return None
        
        
        
        readable_size = human_readable_size(size)
        
        attachment_html = (
            f'<div class="block-editor-attachment">'
            f'  <a href="{url}" target="_blank" download>'
            f'    📄 {self._sanitize_html(title)} ({readable_size})'
            f'  </a>'
        )
                
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
        # Extract data with default values
        data = block.get('data', {})
        
        # Extract file information
        file_info = data.get('file', {})
        url = file_info.get('url', '')
        
        # Extract other block properties
        caption = data.get('caption', '')
        stretched = data.get('stretched', False)
        with_background = data.get('withBackground', False)
        with_border = data.get('withBorder', False)
        
        # Early return if no URL
        if not url:
            return None
        
        # Prepare inline styles
        img_styles = ['max-width: min(600px, 100%);']
        figure_styles = []
        
        if stretched:
            img_styles.append('max-width: 100%; width: 100%; height: auto;')
        
        if with_background:
            figure_styles.append('background-color: rgba(0, 0, 0, 0.1); padding: 10px;')
        
        if with_border:
            figure_styles.append('border: 1px solid #000; padding: 10px;')
        
        # Construct style attributes
        img_style_attr = f' style="{" ".join(img_styles)}"' if img_styles else ''
        figure_style_attr = f' style="{" ".join(figure_styles)}"' if figure_styles else ''
        
        # Create image HTML
        img_html = f'<img src="{url}" alt="{self._sanitize_html(caption)}"{img_style_attr}>'
        
        # Wrap with figure if there's a caption or additional styles
        if caption or figure_styles:
            img_html = f'<figure{figure_style_attr}>{img_html}'
            
            if caption:
                img_html += f'<figcaption>{self._sanitize_html(caption)}</figcaption>'
            
            img_html += '</figure>'
        
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
    