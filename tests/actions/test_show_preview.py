from pro_filer.actions.main_actions import show_preview  # NOQA
import pytest


@pytest.fixture
def context_with_files_and_dirs():
    return {
        "all_files": [
            "/path/to/file1.txt",
            "/path/to/file2.txt",
            "/path/to/file3.txt",
            "/path/to/file4.txt",
            "/path/to/file5.txt",
            "/path/to/file6.txt",
        ],
        "all_dirs": [
            "/path/to/directory1",
            "/path/to/directory2",
            "/path/to/directory3",
            "/path/to/directory4",
            "/path/to/directory5",
            "/path/to/directory6",
        ],
    }


@pytest.fixture
def context_with_empty_files_and_dirs():
    return {"all_files": [], "all_dirs": []}


def test_show_preview_with_files_and_dirs(capsys, context_with_files_and_dirs):
    show_preview(context_with_files_and_dirs)
    captured = capsys.readouterr()
    assert "Found 6 files and 6 directories" in captured.out
    assert (
        "First 5 files: ['/path/to/file1.txt', '/path/to/file2.txt', "
        "'/path/to/file3.txt', '/path/to/file4.txt', '/path/to/file5.txt']"
        in captured.out
    )
    assert (
        "First 5 directories: ['/path/to/directory1', '/path/to/directory2', "
        "'/path/to/directory3', '/path/to/directory4', '/path/to/directory5']"
        in captured.out
    )


def test_show_preview_with_empty_files_and_dirs(
    capsys, context_with_empty_files_and_dirs
):
    show_preview(context_with_empty_files_and_dirs)
    captured = capsys.readouterr()
    assert "Found 0 files and 0 directories" in captured.out
