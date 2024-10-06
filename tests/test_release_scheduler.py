import random

import pytest
from unittest.mock import mock_open, MagicMock
from src.file_utils import read_releases, write_solution
from src.release_scheduler import select_releases


@pytest.mark.parametrize(
    "file_content, expected_output", [
        ("1 1\n2 1\n3 1\n9 1\n10 4\n10 2\n9 5\n10 3\n4 5\n", "5\n1 1\n2 2\n3 3\n4 8\n9 9\n"),
        ("1 1\n1 1\n1 1\n", "1\n1 1\n"),
        ("1 10\n", "1\n1 10\n"),
        ("10 1\n", "1\n10 10\n"),
        ("1 2\n3 2\n5 5\n10 1\n", "4\n1 2\n3 4\n5 9\n10 10\n"),
        ("9 3\n5 7\n", "0\n"),
        ("9 2\n3 8\n 1 3\n", "2\n1 3\n9 10\n"),
        ("9 2\n3 8\n", "1\n3 10\n"),
        ("1 1\n1 3\n1 2\n", "1\n1 3\n"),
        ("", "0\n"),
    ],
    ids=[
        "provided regular case",
        "multiple releases in the same day, only one fits",
        "single long release fits entire sprint",
        "release on the last day",
        "releases are just fitting the sprint",
        "releases are not fitting in the sprint",
        "prioritize a number of releases over a release with the most days to verify",
        "prioritize a release with the most days to verify if number of releases remains the same",
        "same day different durations",
        "empty file",
    ]
)
def test_release_scheduler(mocker, file_content, expected_output):
    m_open = mocker.patch('builtins.open', new_callable=mock_open, read_data=file_content)
    args = MagicMock(
        input_filename='releases.txt',
        output_filename='solution.txt',
        allow_postponement=False,
        sprint_duration_days=10,
    )
    mocker.patch('src.cli_parser.parse_cli_arguments', return_value=args)

    releases = read_releases(file_path='releases.txt')
    selected_releases = select_releases(
        releases=releases,
        sprint_duration_days=args.sprint_duration_days,
        allow_postponement=args.allow_postponement,
    )
    write_solution(selected_releases=selected_releases, file_path='solution.txt')

    write_calls = m_open().write.call_args_list
    written_content = ''.join(args[0][0] for args in write_calls)

    assert written_content == expected_output


@pytest.mark.parametrize(
    "file_content, expected_output", [
        ("1 1\n2 1\n3 1\n9 1\n10 4\n10 2\n9 5\n10 3\n4 5\n", "5\n1 1\n2 2\n3 3\n4 8\n9 9\n"),
        ("1 1\n1 3\n1 2\n", "3\n1 3\n4 5\n6 6\n"),
        ("1 10\n", "1\n1 10\n"),
        ("10 1\n", "1\n10 10\n"),
        ("1 2\n3 2\n5 5\n10 1\n", "4\n1 2\n3 4\n5 9\n10 10\n"),
        ("9 3\n5 7\n", "0\n"),
        ("9 2\n3 8\n 1 3\n", "2\n1 3\n9 10\n"),
        ("9 2\n3 8\n", "1\n3 10\n"),
        ("1 2\n3 3\n5 3\n10 1\n", "4\n1 2\n3 5\n6 8\n10 10\n"),
        ("", "0\n"),
    ],
    ids=[
        "provided regular case",
        "multiple releases in the same day, fit all of them using postponement",
        "single long release fits entire sprint",
        "release on the last day",
        "releases are just fitting the sprint",
        "releases are not fitting in the sprint",
        "prioritize a number of releases over a release with the most days to verify",
        "prioritize a release with the most days to verify if number of releases remains the same",
        "postponement helps to fit 4 releases",
        "empty file",
    ]
)
def test_release_scheduler_with_postponements(mocker, file_content, expected_output):
    m_open = mocker.patch('builtins.open', new_callable=mock_open, read_data=file_content)
    args = MagicMock(
        input_filename='releases.txt',
        output_filename='solution.txt',
        allow_postponement=True,
        sprint_duration_days=10,
    )
    mocker.patch('src.cli_parser.parse_cli_arguments', return_value=args)

    releases = read_releases(file_path='releases.txt')
    selected_releases = select_releases(
        releases=releases,
        sprint_duration_days=args.sprint_duration_days,
        allow_postponement=args.allow_postponement,
    )
    write_solution(selected_releases=selected_releases, file_path='solution.txt')

    write_calls = m_open().write.call_args_list
    written_content = ''.join(args[0][0] for args in write_calls)

    assert written_content == expected_output


@pytest.mark.parametrize(
    "file_content, expected_exception", [
        ("1 a\n2 1\n", ValueError),
        ("1 1\n2\n3 1\n", ValueError),
        ("1 1 1\n3 2\n", ValueError),
        ("1-1\n3 2\n", ValueError),
        ("1 1\n2 1, 3 1\n", ValueError),
        ("1#1\n3 2\n", ValueError),
    ],
    ids=[
        "non-numeric symbols",
        "missing value in a line",
        "too many values in a line",
        "incorrect separator",
        "mixed correct and incorrect lines",
        "special characters as separator",
    ]
)
def test_release_scheduler_invalid_input(mocker, file_content, expected_exception):
    mocker.patch('builtins.open', new_callable=mock_open, read_data=file_content)
    args = MagicMock(
        input_filename='releases.txt',
        output_filename='solution.txt',
        allow_postponement=random.choice([True, False]),
        sprint_duration_days=10,
    )
    mocker.patch('src.cli_parser.parse_cli_arguments', return_value=args)

    with pytest.raises(expected_exception):
        releases = read_releases(file_path='releases.txt')
        select_releases(
            releases=releases,
            sprint_duration_days=args.sprint_duration_days,
            allow_postponement=args.allow_postponement,
        )
