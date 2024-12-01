def image_link_preprocessor(link):
    """
    Preprocess image link.
    """
    print(link)
    return link

def download_link_preprocessor(link):
    """
    Preprocess download link.
    """
    print(link)
    return link

def callback_before_file_save(file):
    """
    Callback modifies the file before saving it.
    """
    print(file)
    return file

def callback_before_return_response(response):
    """
    Callback fixes the response before returning it.
    """
    print(response)
    return response

def editorjs_field_preview_callback(value):
    """
    Preprocess value for widget preview.
    """
    print(value)
    return value

def editorjs_field_save_callback(value):
    """
    Preprocess value before saving it.
    """
    print(value)
    return value