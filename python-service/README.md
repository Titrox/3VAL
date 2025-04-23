# 3VAL - Chess Engine (Python Service)

This directory contains the Python-based chess engine for the 3VAL project. It provides the core logic for evaluating chess positions and determining the best moves. This service runs within a Docker container and communicates with the Spring Boot backend via a REST API.

---

## Project Structure

python-service/
├── requirements.txt      # Python dependencies
├── validation.py         # Input validation functions
├── constants.py          # Constants for evaluation (PSQT, piece patterns)
├── Dockerfile            # Configuration for Docker container
├── evaluations-tests.py  # Unit tests for evaluation functions
└── searchfunction.py     # Contains the chess search algorithm


---

## Tech Stack

- **Python 3.10**
- **Flask** – Lightweight web framework for the REST API
- **Docker** – Containerization platform

---

## Prerequisites

Ensure Docker is installed and running on your system. The backend service relies on this container to function correctly.

- [Docker](https://www.docker.com/)

---

## Running the Service (via Docker Compose)

The Python engine is managed by Docker Compose. From the root directory of the 3VAL project, execute:

```bash
docker-compose up --build
```

This command builds and starts the Flask-based chess engine in a Docker container, making it accessible on port 5000.

---


## Self-Updating Docker Container (Volumes)
The Docker container for the Python service is configured to automatically detect and apply changes made within the python-service directory. This is achieved using Docker volumes defined in the docker-compose.yml:



```YAML
    volumes:
  - ./python-service:/app
  ```

Any modifications to the files within the /python-service directory on the host machine will be reflected inside the running Docker container, and the container will restart automatically to apply these changes. This eliminates the need to manually rebuild the container after each modification.

---

## Unit Tests

Comprehensive unit tests are implemented to ensure the reliability and correctness of the core engine functions, especially those related to evaluation. These tests can be executed at any time to verify that changes or enhancements do not negatively impact the engine's behavior.

To run the unit tests, navigate to the python-service directory and execute:


```bash
python -m unittest evaluations-tests -v
```


For more detailed test coverage analysis, you can use the coverage tool:

- Run tests and generate coverage data:

    ```bash
    coverage run -m unittest evaluations-tests
    ```
  
- Display coverage report in the terminal:

     ```bash
    coverage report -m
    ```

- Generate an HTML coverage report:
    
    ```bash
    coverage html
    ```

The HTML report will be created in a htmlcov directory, providing a visual overview of the test coverage.

---

## Communication with Backend

The Flask-based REST API in this service listens for requests from the Spring Boot backend (running on http://localhost:8080). 
The backend sends chess positions (in FEN notation) to this service for evaluation and to determine the best move. The engine then processes the request and returns the result to the backend.


---

## Related Files

../api/README.md – Backend API (Spring Boot) documentation
../docs/implementation.pdf – Technical implementation details
../docs/theory.pdf – Explanation of chess algorithms and evaluation strategies


