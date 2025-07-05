# run_tests.py
import subprocess
import os

def main():
    # Optional: Ensure behave.ini is loaded correctly
    print("🚀 Running BDD tests with Behave...\n")
    
    # Run behave with desired flags
    result = subprocess.run(
        ["behave", "--no-capture", "--no-logcapture"],
        cwd=os.path.join(os.getcwd(), "test", "features"),  # adjust if needed
        text=True
    )

    # Exit with behave's status code
    exit(result.returncode)

if __name__ == "__main__":
    main()
