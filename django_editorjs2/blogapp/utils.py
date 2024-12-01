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