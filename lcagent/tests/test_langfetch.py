from lcagent.langfetch import langfetcher


lf = langfetcher

def test_right_examples() -> None:
    assert lf('test0', 'en-us') == 'This is a test.'
    assert lf('test0', 'english') == 'This is a test.'
    assert lf('test0', 'zh-cn') == "这是一个测试。"
    assert lf('test0', 'simplified_chinese') == "这是一个测试。"
    lf.set_lang('en-us')
    assert lf('test0') == 'This is a test.'
    lf.set_lang('english')
    assert lf('test0') == 'This is a test.'
    lf.set_lang('zh-cn')
    assert lf('test0') == "这是一个测试。"
    lf.set_lang('simplified_chinese')
    assert lf('test0') == "这是一个测试。"
    supported = lf.get_supported()
    assert supported['english'] == 'en-us'
    assert supported['simplified_chinese'] == 'zh-cn'

def test_wrong_examples() -> None:
    assert lf('test_wrong0', 'en-us') == lf.DEFAULT_ERROR_MESSAGE
    assert lf('test_wrong0', 'english') == lf.DEFAULT_ERROR_MESSAGE
    assert lf('test_wrong0', 'zh-cn') == lf.DEFAULT_ERROR_MESSAGE
    assert lf('test_wrong0', 'simplified_chinese') == lf.DEFAULT_ERROR_MESSAGE
    original = lf('test0')
    lf.set_lang('language_not_exist')
    assert lf('test0') == original
