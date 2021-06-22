from validate_email import validate_email


def test_valid_email():
    is_valid = validate_email("fakeoff22@gmail.com")
    assert is_valid is True


def test_invalid_email():
    is_valid = validate_email("meuemailnaoexiste@naoexiste.com.br")
    assert is_valid is False
