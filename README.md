# Release Selector

This project helps optimize the number of software releases that can be validated within a given sprint. The app
provides the following key features:

- **No Overlapping Releases**: The app ensures that no two releases overlap during validation, each release is verified
  sequentially.

- **Sprint Time Limit**: All releases must be completed within the defined sprint period. Any release that extends
  beyond the sprint’s final day is discarded.

- **Postponement Option**: If the `--allow-postponement` flag is set, the app may delay the start of a release within
  the sprint period to maximize the total number of releases that can be verified.

- **Resource Allocation Efficiency**: When possible, the app prioritizes releases with longer durations, as long as this
  prioritization does not reduce the total number of releases that can be verified within the sprint.

The overall goal is to verify the maximum number of releases without exceeding the sprint limits, and using available
time in the most effective way.

- The input file should contain releases with each line formatted as:

  ```
  <start_day> <duration>
  ```

  Example `releases.txt`:

  ```
  1 1
  3 5
  6 3
  9 2
  ```

- The output file contains maximum number of validated releases within a spring and lines with days of the releases:

  ```
  <number_of_releases>
  <start_day> <end_day>
  ```

  Example `solution.txt`:

  ```
  3
  1 1
  3 7
  9 10
  ```

## Getting Started

### Prerequisites

- Docker
- Python (optional if running the app directly without Docker)

### Project Structure

- `src/`: Contains the main application logic.
- `tests/`: Contains tests for the application.
- `data/`: The folder where input and output files are stored.
- `requirements.txt`: Contains project dependencies.
- `Dockerfile`: Configuration for building and running the app or tests in a Docker container.

## Running the App with Docker

### 1. **Prepare Input File**

The input file should contain releases with expected format.

### 2. **Build the Docker Image**

To build the Docker image, navigate to the project folder and run:

   ```bash
   docker build -t release_selector .
   ```

### 3. **Run the App**

#### Running the App Without Postponement:

```bash
docker run -v $(pwd)/data:/app/data release_selector \
  --file /app/data/releases.txt \
  --output /app/data/solution.txt
```

#### Running the App With Postponement:

```bash
docker run -v $(pwd)/data:/app/data release_selector \
  --file /app/data/releases.txt \
  --output /app/data/solution.txt \
  --allow-postponement
```

The app will read `releases.txt` from the `data` directory, process it, and write the output to `solution.txt` in the
same directory.

### 4. **Running Tests**

To run tests for the app, use the following command:

```bash
docker run -e RUN_TESTS="true" release_selector
   ```

### Available Command-Line Arguments

- `--file`: Path to the releases file (default: `data/releases.txt`).
- `--output`: Path to the output file (default: `data/solution.txt`).
- `--loglevel`: Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default is `INFO`.
- `--allow-postponement`: If provided, allows postponement of releases within a sprint.
- `--sprint-duration-days`: Duration of the sprint in days (default: 10 days).

To see more info on available options, run:

```bash
docker run release_selector --help
   ```

### Running the App Without Docker

#### Create Virtual Env and Install Dependencies (optional, if tests run needed)

```bash
cd release_selector
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
   ```

#### Running the App Without Postponement:

```bash
python3 src/release_scheduler.py
```

#### Running the App With Postponement:

```bash
python3 src/release_scheduler.py --allow-postponement
```

#### Running Tests:

```bash
pytest -v
```

#### Getting Help:

```bash
python3 src/release_scheduler.py --help
```
