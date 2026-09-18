# 🆓 Free Tier Deployment Guide for ARC Prize Solver 2026

Deploy **ARC Prize Solver** using **Kaggle Free Kernels (30h/wk GPU)**, **Hugging Face Spaces**, and **Cloudflare Tunnels**.

---

## 1. Free High-Performance Search: Kaggle Kernels
Kaggle provides **30 hours per week of free NVIDIA Tesla T4/P100 GPU compute**:
1. Push your solver to Kaggle using the Kaggle CLI:
   ```bash
   kaggle kernels push -p deploy/free/
   ```
2. Run offline test-time compute search across 400 competition evaluation tasks.

---

## 2. Interactive 2D Grid Visualizer: Hugging Face Spaces
Hugging Face offers **16 GB RAM and 2 vCPUs completely free**:
1. Create a Space with Docker SDK.
2. Push your `Dockerfile`, `src/`, and `README_HF.md`.

---

## 3. Localhost Tunnel for Demos: Cloudflare Tunnel
```powershell
# Windows
.\deploy\free\tunnel.ps1 -Port 3007

# Linux / macOS
./deploy/free/tunnel.sh 3007
```
