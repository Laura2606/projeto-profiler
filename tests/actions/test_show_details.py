from pro_filer.actions.main_actions import show_details  # NOQA
import pytest
from datetime import datetime


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
    assert "File '???' does not exist\n" in captured.out


def test_show_details_without_extension(capsys):
    context = {"base_path": "/home/trybe/Downloads/some_file"}
    show_details(context)
    captured = capsys.readouterr()
    assert "File 'some_file' does not exist\n" in captured.out


@pytest.fixture
def file_without_extension(tmp_path):
    file_path = tmp_path / "file_without_extension"
    file_path.write_text("This is a test file without extension.")
    return str(file_path)


def test_show_details_file_without_extension(file_without_extension, capsys):
    context = {"base_path": file_without_extension}
    show_details(context)
    captured = capsys.readouterr()
    expected_output = (
        "File name: file_without_extension\n"
        "File size in bytes: 38\n"
        "File type: file\n"
        "File extension: [no extension]\n"
        "Last modified date: 2024-03-28\n"
    )
    assert expected_output in captured.out


def test_show_details_correct_date_format(capsys):
    context = {"base_path": "pro_filer/actions/__init__.py"}
    show_details(context)
    captured = capsys.readouterr()
    _, mod_date_str = captured.out.split("Last modified date: ")
    try:
        _ = datetime.strptime(mod_date_str.strip(), "%Y-%m-%d")
    except ValueError:
        pytest.fail("Formato de data incorreto")


def test_show_details_incorrect_date_format(capsys):
    context = {"base_path": "pro_filer/actions/__init__.py"}
    show_details(context)
    captured = capsys.readouterr()
    _, mod_date_str = captured.out.split("Last modified date: ")
    with pytest.raises(ValueError):
        datetime.strptime(mod_date_str.strip(), "%d-%m-%Y")
