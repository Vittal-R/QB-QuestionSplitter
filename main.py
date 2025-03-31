import subprocess
import os

def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running {script_name}: {e}")
    except FileNotFoundError:
        print(f"Script {script_name} not found.")

if __name__ == "__main__":
    # Define the paths to the scripts
    parsing_script = os.path.join(os.path.dirname(__file__), "parsingTest.py")
    organizing_script = os.path.join(os.path.dirname(__file__), "organizingText.py")

    # Run the parsing script
    run_script(parsing_script)

    # Run the organizing script
    run_script(organizing_script)