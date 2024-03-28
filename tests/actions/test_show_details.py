from pro_filer.actions.main_actions import show_details  # NOQA
import pytest
from datetime import date


@pytest.fixture
def existing_file_context():
    return {"base_path": "/path/to/existing_file.txt"}


@pytest.fixture
def non_existing_file_context():
    return {"base_path": "/path/to/non_existing_file.txt"}


def test_show_details_existing_file(capsys, existing_file_context):
    show_details(existing_file_context)
    captured = capsys.readouterr()
    assert "File name: existing_file.txt" in captured.out
    assert "File size in bytes:" in captured.out
    assert "File type: file" in captured.out
    assert "File extension: .txt" in captured.out
