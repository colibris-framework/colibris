
def assert_is_envelope(value, count=None, pages=None, page=None, page_size=None):
    assert isinstance(value, dict)

    assert 'count' in value
    assert 'pages' in value
    assert 'page' in value
    assert 'page_size' in value

    if count is not None:
        assert value['count'] == count
    if pages is not None:
        assert value['pages'] == pages
    if page is not None:
        assert value['page'] == page
    if page_size is not None:
        assert value['page_size'] == page_size
