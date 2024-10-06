from argparse import Namespace, ArgumentParser
import os
import logging
from pathlib import Path


def parse_cli_arguments() -> Namespace:
    """Parse command line arguments for the script and return them as a dictionary."""
    parser = ArgumentParser(description='Select optimal set of releases for a sprint.')

    parser.add_argument(
        '--file',
        dest='input_filename',
        default='../data/releases.txt',
        type=str,
        help='Path to the releases file (default: ../data/releases.txt)',
    )
    parser.add_argument(
        '--output',
        dest='output_filename',
        default='../data/solution.txt',
        type=str,
        help='Path to save the output file (default: ../data/solution.txt)',
    )
    parser.add_argument(
        '--loglevel',
        dest='log_level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Set the logging level (default: INFO)'
    )
    parser.add_argument(
        '--allow-postponement',
        dest='allow_postponement',
        action='store_true',
        help='Allow postponement of releases within sprint limits (default: False)'
    )
    parser.add_argument(
        '--sprint-duration-days',
        dest='sprint_duration_days',
        default=10,
        type=int,
        help='Sprint duration in working days (default: 10)'
    )

    args = parser.parse_args()

    script_dir: Path = Path(os.path.realpath(__file__)).parent
    args.input_filename = str(script_dir / args.input_filename)
    args.output_filename = str(script_dir / args.output_filename)

    numeric_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {args.log_level}')

    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(
        f"Arguments for program to start:\n"
        f"  Sprint duration: {args.sprint_duration_days} days\n"
        f"  Allow postponement: {args.allow_postponement}\n"
        f"  Source file: {args.input_filename}\n"
        f"  Output file: {args.output_filename}"
    )

    return args
