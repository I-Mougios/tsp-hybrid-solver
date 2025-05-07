# Hybrid TSP Solver

A research project for my master's dissertation exploring the use of **Graph Neural Networks (GNNs)** to solve the **Traveling Salesman Problem (TSP)**. The project integrates a traditional **Linear Programming (LP)** solver to generate optimal routes and a **PyTorch Geometric**-based GNN to learn from those solutions. The infrastructure includes a **MongoDB** backend and containerized execution using **Docker**.

---
## 📁 Project Structure
tsp-hybrid-solver/

├── tsp/ # LP solver using scipy.optimize.linprog

├── gnn/ # GNN model and dataset (PyTorch Geometric)

├── container/ # MongoDB and data generation logic (inserts solved TSPs)

│ └── main.py # Generates 10,000 TSP instances and stores them in MongoDB

├── configs/ # Configuration management (INI + loader)

├── pytutils/ # Reusable utility package (only config used here)

├── jobs/ # Job package with modules for training, inference, and loading logic

├── main.py # Orchestrates full GNN pipeline: load data → train → predict

├── checkpoints # Saves the best model after the training and the predictions from the test set in a csv file

├── docker-compose.yml # Starts MongoDB and data generation container

└──  LICENSE # Open source license


## 🔧 Key Components

- **TSP Solver (LP-based)**: Uses `scipy.optimize.linprog` to generate optimal tours.
- **GNN Model**: Trained using PyTorch Geometric to approximate the LP-solved tours.
- **MongoDB Integration**: Stores solved TSP instances for use as graph datasets.
- **Dockerized Workflow**:
  - Spins up MongoDB and runs `container/main.py` to generate data.
  - Then, `main.py` (at root) consumes the data for training and prediction.
- **Modular Job System**: `load_tsp_dataset`, `train_gnn_model`, `load_model`, `get_predictions` are decoupled jobs orchestrated via a central interface.

---

## 🚀 Usage Guide

### Step 1: Generate Dataset (Requires Docker)

```bash
docker-compose up --build
```

### Step 2: Train the GNN Model and Get Predictions

The project’s top-level main.py provides a fully orchestrated pipeline to:

load the TSP dataset from MongoDB using job-based configuration,
train the GNN model with early stopping, gradient clipping, and warm-up support,
reload the best checkpoint, and
generate and save predictions on the test set.
This script makes use of orchestrator.run_job(...) to modularly trigger each step, making the workflow highly reusable and configurable via the configs.ini file.

ℹ️ Note: The MongoDB container must be running to access the stored TSP instances before training. Use docker-compose up to launch the MongoDB backend.
The script is structured for both notebook-style execution (e.g., PyCharm Pro / VSCode) and full pipeline runs.