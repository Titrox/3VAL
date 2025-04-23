# 3VAL - Chess Engine

**3VAL** is a modular chess engine system with an interactive robot interface. The project consists of a modern frontend, a Spring Boot backend, and a Python-based chess engine running in a Docker container. Users can play against the AI and observe real-time evaluations and emotional reactions from a robot assistant.


![Debug Mode](./docs/images/Screenshot-Debug-Mode.png)

---

## Project Structure

```
3VAL/
├── api/                 # Spring Boot backend (REST API)
├── frontend/            # Vue.js frontend (Vite)
├── python-service/      # Python-based chess engine (Flask)
├── docs/                # Theory and implementation details
├── docker-compose.yml   # Launches the Flask engine container
├── README.md            # Project overview
```

---

## Getting Started

To run the full system, follow the steps below:

### 1. Start the Python Engine (Dockerized Flask Server)

Make sure Docker is installed and running, then execute from the root directory:

```bash
docker-compose up --build
```

This starts the Flask-based chess engine in a container on port **5000**.

### 2. Start the Backend (Spring Boot)

Follow the instructions in [`api/README.md`](api/README.md):

```bash
cd api
mvn spring-boot:run
```

The backend will launch on [http://localhost:8080](http://localhost:8080) and acts as a bridge between frontend and engine.

### 3. Start the Frontend (Vue 3 + Vite)

Follow the instructions in [`frontend/README.md`](frontend/README.md):

```bash
cd frontend
npm install
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173) by default.

---

## Features

- Interactive chessboard interface with reactive robot assistant
- Emotional response system with audio and message variation
- Fully customizable evaluation parameters (material, king safety, etc.)
- REST-based communication architecture
- Clean modular separation between frontend, backend, and engine

---

## Further Documentation

- [`frontend/README.md`](frontend/README.md) – UI setup and features
- [`api/README.md`](api/README.md) – Backend endpoints and setup
- [`implementation.pdf`](docs/implementation.pdf) – Details technical implementation and architecture
- [`theory.pdf`](docs/theory.pdf) – Describes algorithms like Minimax and evaluation strategies

---

## Requirements

- Docker + Docker Compose
- Java 17+ and Maven (for backend)
- Node.js 16+ and npm (for frontend)

---

## License

Open-source under the [MIT License](https://opensource.org/licenses/MIT)
