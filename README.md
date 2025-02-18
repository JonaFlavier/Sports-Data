# Sports-Data

React Frontend with FastAPI 

## Instructions for Use

Follow the steps below to set up and run the project.

### 1. Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/JonaFlavier/Sports-Data.git
cd Sports-Data
```

### 2. Build and Start Docker Compose
Run the following command to build and start the containers:

```bash
docker-compose up --build -d
```

### 3. Access the Application
- Open your browser and go to **[http://localhost:3000](http://localhost:3000)** to access the React interface.
- View API documentation at **[http://localhost/docs](http://localhost/docs)**.

### 4. Stopping the Containers
To stop and remove containers, use:

```bash
docker-compose down
```

---

### 📌 Additional Notes
- Ensure **Docker** and **Docker Compose** are installed on your system.
- If any issues arise, check logs with:

  ```bash
  docker-compose logs -f
  ```

