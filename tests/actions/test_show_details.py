from pro_filer.actions.main_actions import show_details  # NOQA
import pytest


@pytest.fixture
def existing_file_context():
    return {"base_path": "images/pro-filer-preview.gif"}


@pytest.fixture
def non_existing_file_context():
    return {"base_path": "images/trybe/???"}


def test_show_details_existing_file(capsys, existing_file_context):
    show_details(existing_file_context)
    captured = capsys.readouterr()
    assert "File name: pro-filer-preview.gif" in captured.out
    assert "File size in bytes:" in captured.out
    assert "File type: file" in captured.out
    assert "File extension: .gif" in captured.out
    assert "Last modified date:" in captured.out in captured.out


def test_show_details_non_existing_file(capsys, non_existing_file_context):
    show_details(non_existing_file_context)
    captured = capsys.readouterr()
    assert "File '???' does not exist\n" == captured.out


# teste
