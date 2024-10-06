import logging
from typing import Union, List, Dict


def read_releases(file_path: str) -> List[Dict[str, int]]:
    """
    Read releases from a file and return a list of dictionaries.
    Each dictionary represents a release with keys 'sprint_day' and 'days_to_complete'.
    """
    logging.debug(f"Opening file to read releases.")
    with open(file_path, 'r') as file:
        releases = []
        for line in file:
            line = line.strip()
            if line:
                digit = line.split()
                if len(digit) != 2:
                    logging.error(f"Unexpected line format: {line}")
                    raise ValueError(f"Invalid format in line: {line}. Expected two integers.")
                try:
                    releases.append({
                        'sprint_day': int(digit[0]),
                        'days_to_complete': int(digit[1])
                    })
                except ValueError:
                    logging.error(f"Unexpected line format: {line}")
                    raise ValueError(f"Non-numeric values found in line: {line}. Both values must be integers.")

        logging.debug(f"Read {len(releases)} releases from the file. Releases: {releases}")
    logging.info("Completed reading releases.")

    return releases


def write_solution(selected_releases: List[Dict[str, int]], file_path: Union[str, bytes]) -> None:
    """
    Write the selected releases to a file in a format:
    number_of_releases
    day_of_start_verifying day_of_end_verifying
    """
    logging.debug(f"Starting write_solution to file: {file_path}.")
    with open(file_path, 'w') as file:
        file.write(f"{len(selected_releases)}\n")
        logging.debug(f"Number of releases: {len(selected_releases)}")
        for release in selected_releases:
            sprint_day = release['sprint_day']
            days_to_complete = release['days_to_complete']
            end_day = sprint_day + days_to_complete - 1
            file.write(f"{sprint_day} {end_day}\n")
            logging.debug(f"Writing release: start={sprint_day}, end={end_day}")

    logging.info(f"Completed writing to file.")
