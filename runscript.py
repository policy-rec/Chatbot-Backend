import subprocess
import os
import webbrowser 
import time        

REQUIREMENTS_FILE = "requirements.txt"

def install_dependencies(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return
    print(f"Installing dependencies from {filename}...")
    subprocess.check_call(["pip", "install", "-r", filename])

def run_uvicorn():
    print("Starting FastAPI server using uvicorn...")
    process = subprocess.Popen(["python", "-m", "uvicorn", "main:app", "--reload"])
    time.sleep(2) 
    webbrowser.open("http://127.0.0.1:8000/docs")  
    process.wait()

if __name__ == "__main__":
    try:
        run_uvicorn()
    except Exception as e:
        print(f"Error: {e}")