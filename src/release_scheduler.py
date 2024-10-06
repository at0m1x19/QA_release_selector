import logging
from typing import Dict, List

from src.cli_parser import parse_cli_arguments
from src.file_utils import read_releases, write_solution


def select_releases(
        releases: List[Dict[str, int]],
        sprint_duration_days: int,
        allow_postponement: bool,
) -> List[Dict[str, int]]:
    """
    Select the set of releases to verify as many releases as possible within sprint_length_days.
    If allow_postponement is True, releases can be postponed within sprint limits.
    """
    logging.info(f"Starting to select releases from provided data. Postponement allowed: {allow_postponement}")

    selected_releases: List[Dict[str, int]] = []
    earliest_start_day: int = 1  # For postponement mode
    previous_release_end_day: int = 0  # For non-postponement mode

    releases_possible_to_complete = []
    for release in releases:
        if (
                release['sprint_day'] <= sprint_duration_days
                and
                release['sprint_day'] + release['days_to_complete'] - 1 <= sprint_duration_days
        ):
            releases_possible_to_complete.append(release)
    logging.debug(
        f"Found {len(releases_possible_to_complete)} releases possible to verify within a sprint "
        f"of {sprint_duration_days} days: {releases_possible_to_complete}"
    )

    # Sort releases by sprint day and duration (descending for same start day)
    sorted_releases = sorted(
        releases_possible_to_complete,
        key=lambda release_: (release_['sprint_day'], -release_['days_to_complete'])
    )
    logging.debug(f"Sorted releases: {sorted_releases}")

    for release in sorted_releases:
        if allow_postponement:
            start_day = max(release['sprint_day'], earliest_start_day)
            end_day = start_day + release['days_to_complete'] - 1
            logging.debug(f"Trying to fit release: {release}, start day: {start_day}, end day: {end_day}")

            if end_day <= sprint_duration_days:
                logging.debug(f"Selected release: {release}, start day: {start_day}, end day: {end_day}")
                selected_releases.append({'sprint_day': start_day, 'days_to_complete': release['days_to_complete']})
                earliest_start_day = end_day + 1
        else:
            if release['sprint_day'] > previous_release_end_day:
                logging.debug(f"Selected release without postponement: {release}")
                selected_releases.append(release)
                previous_release_end_day = release['sprint_day'] + release['days_to_complete'] - 1

    logging.info(f"Number of selected releases: {len(selected_releases)}. Releases: {selected_releases}")
    return selected_releases


def main():
    args = parse_cli_arguments()
    releases = read_releases(file_path=args.input_filename)
    selected_releases = select_releases(
        releases=releases,
        sprint_duration_days=args.sprint_duration_days,
        allow_postponement=args.allow_postponement,
    )
    write_solution(selected_releases=selected_releases, file_path=args.output_filename)


if __name__ == "__main__":
    main()
