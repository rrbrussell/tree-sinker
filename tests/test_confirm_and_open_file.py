from tree_sinker.support import confirm_and_open_file

def test_confirm_and_open_file():
    result = confirm_and_open_file('.non_existent', False)
    assert result is None
    result = confirm_and_open_file('./etc/tree-sinker.ini', False)
    assert result is not None
    result.close()

#End of buffer
