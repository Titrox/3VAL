# Frontend – 3VAL

This is the **frontend** of 3VAL, the Chess AI project. It provides an interactive and engaging interface for users to play against the engine. A dynamic robot avatar reacts to the game in real-time with tailored emotions and messages based on the current board evaluation. The interface also allows users to adjust evaluation parameters and load FEN strings.

---

## Tech Stack

- **Vue 3** – Modern JavaScript framework
- **Vite** – Fast build tool and development server
- **JavaScript / HTML / CSS**

---

## Prerequisites

Before running the frontend, ensure the following are installed on your system:

- [Node.js](https://nodejs.org/) (version **16+** recommended)
- npm (comes with Node.js)

Check versions with:

```bash
node -v
npm -v
```
---

## Getting Started


1. Navigate to the frontend folder:

    ```bash
    cd frontend
    ```
   
2. Install the dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm run dev
    ```

4. Access the application:

After starting the dev server, Vite will provide a local development URL (typically http://localhost:5173). The exact URL will appear in your terminal.

---

## Features
- Robot reacts with emotions and spoken lines to evaluation changes
- Load custom FEN positions
- Dynamically adjust evaluation parameters (e.g. king safety, material)
- Responsive UI with real-time board updates

---

## Notes
- Make sure the backend (e.g. Spring Boot or Flask in Docker) is running and accessible via REST API.
- If you're running the backend locally, configure CORS or use a local proxy if needed.
- Audio features rely on browser support and may require user interaction to play.
