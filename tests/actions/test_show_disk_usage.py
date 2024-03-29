from pro_filer.actions.main_actions import show_disk_usage  # NOQA
import pytest
import os


@pytest.fixture
def files_list(tmp_path):
    file1 = "file1.txt"
    (tmp_path / file1).write_text("This is a test file 1.")

    file2 = "file2.txt"
    (tmp_path / file2).write_text("This is a test file 2.")

    file3 = "file3.txt"
    (tmp_path / file3).write_text("This is a test file 3." * 10)

    return [file1, file2, file3]


def test_show_disk_usage_calculates_correct_total_size(
    tmp_path, files_list, capsys
):
    context = {
        "all_files": [os.path.join(str(tmp_path), file) for file in files_list]
    }
    show_disk_usage(context)
    captured = capsys.readouterr().out

    file_sizes = [
        os.path.getsize(os.path.join(str(tmp_path), file))
        for file in files_list
    ]

    total_size = sum(file_sizes)

    assert (
        f"Total size: {total_size}" in captured
    ), "O espaço total ocupado pelos arquivos não está sendo calculado corretamente."


def test_show_disk_usage_detects_empty_files(tmp_path, files_list, capsys):
    context = {
        "all_files": [os.path.join(str(tmp_path), file) for file in files_list]
    }
    show_disk_usage(context)
    captured = capsys.readouterr().out

    assert (
        "Algum dos arquivos está vazio." not in captured
    ), "A função show_disk_usage considera incorretamente todos os arquivos como vazios."


def test_show_disk_usage_sorts_files_by_size(tmp_path, files_list, capsys):
    context = {
        "all_files": [os.path.join(str(tmp_path), file) for file in files_list]
    }
    show_disk_usage(context)

    captured = capsys.readouterr().out

    file_sizes = [
        os.path.getsize(os.path.join(str(tmp_path), file))
        for file in files_list
    ]

    sorted_files = sorted(
        zip(files_list, file_sizes), key=lambda x: x[1], reverse=True
    )

    total_size = sum(file_sizes)

    expected_output = ""
    for file_name, size in sorted_files:
        percentage = int((size / total_size) * 100)
        file_name = os.path.basename(file_name)
        expected_output += f"- '{file_name}': {size} ({percentage}%)\n"
    expected_output += f"Total size: {total_size}\n"

    assert (
        captured == expected_output
    ), "A listagem de arquivos não está ordenada corretamente por tamanho."
