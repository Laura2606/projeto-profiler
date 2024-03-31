from pro_filer.actions.main_actions import show_disk_usage  # NOQA
import pytest
import os
from faker import Faker

fake = Faker()


@pytest.fixture
def files_list(tmp_path):
    file1 = "file1.txt"
    file_path1 = tmp_path / file1
    file_path1.write_text("This is a test file 1.")

    file2 = "file2.txt"
    file_path2 = tmp_path / file2
    file_path2.write_text("This is a test file 2.")

    file3 = "file3.txt"
    file_path3 = tmp_path / file3
    file_path3.write_text("This is a test file 3." * 10)

    return [file_path1, file_path2, file_path3]


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
    ), "O espaço total ocupado pelos arquivos não está sendo calculado"
    "corretamente."


def test_show_disk_usage_detects_empty_files(tmp_path, files_list, capsys):
    context = {
        "all_files": [os.path.join(str(tmp_path), file) for file in files_list]
    }
    show_disk_usage(context)
    captured = capsys.readouterr().out

    assert (
        "Algum dos arquivos está vazio." not in captured
    ), "A função show_disk_usage considera incorretamente todos os arquivos"
    "como vazios."


@pytest.fixture
def files_size(files_list):
    return [file.stat().st_size for file in files_list]


def test_show_disk_usage_order_by_size(files_list, files_size, capsys):
    context = {"all_files": [str(file) for file in files_list]}
    show_disk_usage(context)
    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")
    assert len(lines) == len(files_size) + 1
    sizes_from_output = [
        int(line.split("(")[0].strip().split()[-1]) for line in lines[:-1]
    ]
    sorted_file_sizes = sorted(files_size, reverse=True)
    assert sorted_file_sizes == sizes_from_output
