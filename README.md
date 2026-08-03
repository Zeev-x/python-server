# Python Server (Portable Edition)

A lightweight and portable **Python server** powered by [Reyette](https://github.com/Zeev-x).  
This project is designed to run directly from a **USB flash drive** without requiring a global Python installation, making it ideal for developers who need flexibility and portability.

---

## ✨ Features
- **Portable Python Runtime**: No need to install Python globally.  
- **USB Ready**: Carry your server anywhere and run it instantly.  
- **Simple Setup**: Just run the batch installer once.  
- **Custom Command (`pyr`)**: Execute Python scripts easily with a short command.  
- **Windows Support**: Optimized for Windows environments.  

---

## 📌 Notes
- Portable Python is currently supported **only on Windows**.  
- Ensure your USB drive has sufficient space for Python runtime and your scripts.  

---

## 🚀 Getting Started (Windows)
1. Clone or download this repository to your USB flash drive.  
2. Run the installer script:  
   ```bash
   install_portable_py.bat
   ```
   This will set up the portable Python environment.
3. Execute your Python scripts using the custom command:
   ```bash
   pyr main.py
   ```
   or
   ```bash
   pyr your_script.py
   ```
---

## Installing portable python windows
Run this:
```bash
curl -sL https://raw.githubusercontent.com/Zeev-x/python-server/refs/heads/main/install_portable_py.bat | cmd /c
```

## 📂 Project Structure
```
├── install_portable_py.bat   # Batch file to install portable Python
├── pyr.bat                   # Custom command wrapper
├── main.py                   # Example server script
└── README.md                 # Documentation
```
---

## 💡 Use Cases
* Running Python servers on shared or restricted PCs.
* Carrying development environments on-the-go.
* Quick prototyping without installing Python globally.
* Teaching or workshops where setup time must be minimal.
---

## 🔧 Troubleshooting
* If ```pyr``` is not recognized, ensure ```install_portable_py.bat``` has been executed successfully.
* Check that your USB drive is formatted with NTFS or exFAT for better compatibility.
* Scripts requiring external libraries should be installed inside the portable environment using ```pip```.
---

## 📜 License
* This project is released under the MIT License.
* Feel free to use, modify, and distribute with proper attribution.
---

## 👤 Author
* Developed by [Reyette](https://github.com/Zeev-x)
* Maintained and improved with portability in mind.
