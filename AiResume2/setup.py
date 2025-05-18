import subprocess
import sys
#We had chatgbt help us debug and write the code.
def check_and_install_dependencies():
    print("Checking and installing dependencies for AI Resume Analyzer...")
    
    with open('requirements.txt') as f:
        required_packages = [line.strip() for line in f if line.strip()]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            package_name = package.split('==')[0]
            __import__(package_name)
            print(f"✓ {package} is already installed")
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("\nInstalling missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
    else:
        print("\nAll required packages are already installed!")
    
    print("\nSetup complete! You can now run the application with: streamlit run main.py")

if __name__ == "__main__":
    check_and_install_dependencies()