def remove_url_parameters(url):
    if '?' in url:
        return url[:url.find('?')]
    return url
