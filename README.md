# NEX-PULSE AI OPTIMIZER ⚡

> **Distinguished Engineering Project by Cristian David Quispe Lucas**

NEX-PULSE is an intelligent, low-level system optimization agent designed to monitor, evaluate, and proactively optimize Windows workstations without destroying active user processes.

## 🚀 Key Features

*   **Autonomous Intelligence:** Calculates dynamic system health scores using statistical Moving Averages (EWMA) on CPU and RAM telemetry.
*   **Non-Destructive Optimization:** Employs the native Windows `EmptyWorkingSet` kernel API to safely reclaim inactive memory from heavy applications (like Chrome or Games) without crashing or closing them.
*   **Proactive Auto-Clean:** Aggressively clears out temporary system files, bypassing locks silently to ensure stability.
*   **Robust Architecture:** Built with a clean monorepo structure, secure UAC privilege elevation, and bulletproof logging.

## 🛠 Technology Stack

*   **Core Engine:** Python 3.10+
*   **System Interfaces:** `psutil`, `ctypes` (Windows Kernel APIs)
*   **UI/Frontend:** Tauri, React, TypeScript, TailwindCSS (Cyberpunk Aesthetic)

## 📦 How to Build the `.exe`

This project includes a secure build pipeline to generate a false-positive-resistant Windows executable.

1. Ensure Python and `pip` are installed.
2. Install build dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```
3. Run the automated build script:
   ```bash
   .\scripts\build_exe.bat
   ```
4. The executable will be generated inside the `dist/` directory, requiring standard UAC Administrator privileges upon execution.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
