# how to pass args and run script:

# Bash:
#   python Install_And_Run_Program.py --video example\ video.mp4
# or
#   python Install_And_Run_Program.py --verbose --venv TEST --video 'example video.mp4'

# Powershell:
#   python  .\Install_And_Run_Program.py --video example\ video.mp4
# or
#   python  .\Install_And_Run_Program.py --verbose --venv TEST --video 'example video'.mp4

import argparse
import platform
import subprocess
import os
import venv

NAME_OF_SCRIPT_TO_RUN = "motion_Extraction.py"
VIRT_ENV_NAME = "venvName"
PACKAGES_TO_INSTALL_ARRAY = ["opencv-python"]# you can just keep adding to this like "pandas==2.1", "PIL==1.01", etc

# Create a virtual environment, don't activate it
def create_venv(venv_dir=VIRT_ENV_NAME):
    # Determine the activation script path & operating system (for user info only)
    pip_path, virt_env_python_path, activation_path, operating_sys = get_venv_data(venv_dir)

    print("\n===========--------===========--------===========\n")

    print(f"> Operating System detected: {operating_sys}")

    print("\n===========--------===========--------===========\n")

    print(f"> Creating / Updating {venv_dir} virtual environment, might take a sec...")

    venv.create(venv_dir, with_pip=True)

    print(f"\n> Virtual Environment Created at {venv_dir}")

    print(f"    ... to activate manually in terminal, use: {activation_path}")

    print("\n===========--------===========--------===========\n")


# Get path to the virtual environments pip -- might not need this
def get_venv_data(venv_dir=VIRT_ENV_NAME):
    operating_system = platform.system()
    if operating_system == "Windows":
        # return os.path.join(venv_dir, "Scripts", "pip.exe")
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        # return os.path.join(venv_dir, "bin", "pip")
        pip_path = os.path.join(venv_dir, "bin", "pip")
        activate_script = os.path.join(venv_dir, "bin", "activate")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    return pip_path, python_path, activate_script, operating_system


# Install Packages using the virtual environment's pip with trusted hosts
def pip_install_packages(packages,venv_dir=VIRT_ENV_NAME,extra_index_url=None, verbose=True, pre=False):
    print(f"> Installing Packages in {venv_dir}'s pip using trusted hosts, please be patient!")

    pip_path, virt_env_python_path, activation_path, operating_sys = get_venv_data(venv_dir)

    # Define Trusted Hosts:
    trusted_hosts = [
        "--trusted-host", "pypi.org",
        "--trusted-host", "pypi.python.org",
        "--trusted-host", "files.pythonhosted.org",
        "--trusted-host", "download.pytorch.org"
    ]
    
    for package in packages:
        try:
            print(f"    ... installing {package}")

            # base command
            cmd = [pip_path, "install"]

            # add trusted hosts
            cmd.extend(trusted_hosts)

            if pre:
                cmd.append("--pre")
            
            # add '-q' if not verbose
            if not verbose:
                cmd.append("-q")

            # add package name
            cmd.append(package)

            # add extra_index_url if it exists
            if extra_index_url:
                cmd.extend(["--extra-index-url",extra_index_url])

            if verbose:
                print(cmd)
            
            # run the command and capture the output
            result = subprocess.run(cmd, capture_output=not verbose, text=True)

            if result.returncode != 0:
                print(f"Error installing {package}:")
                print(result.stderr)

        except Exception as e:
            print(f"failed to install {package}: {e}")

    return

# run a python script using the virtual environment's interpreter
def run_script_in_venv(venv_dir,script_path, *args):
    print("\n===========--------===========--------===========\n")
        # Run the target script if requested
    print(f"> Running Target Script: {script_path}")

    pip_path, virt_env_python_path, activation_path, operating_sys = get_venv_data(venv_dir)

    cmd = [virt_env_python_path, script_path] + list(args)
    print("\n===========--------===========--------===========\n")
    # print(f"  -> {cmd}")
    subprocess.run(cmd)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true',
                        help='print pip install stuff')
    
    parser.add_argument('--venv', default=VIRT_ENV_NAME,
                        help='virtual environment directory name')
    
    parser.add_argument('--video', default="none",
                        help='input name / path of the video')    

    args = parser.parse_args()

    # # Setup Virt environment
    # install_requirements(venv_dir=args.venv, verbose=args.verbose)

    if args.video != "none":
        # Create virtual Environment
        create_venv(venv_dir=args.venv)

        # install packages
        pip_install_packages(PACKAGES_TO_INSTALL_ARRAY,
                             venv_dir=args.venv, verbose=args.verbose)
        
        # running target script
        run_script_in_venv(args.venv,NAME_OF_SCRIPT_TO_RUN, args.video)
    else:
        # catch if no video argument was provided
        print("===========--------===========--------===========")
        print("> You need to pass in the video you want to extract motion from, like this:")
        print("===========--------===========--------===========")

        print("Bash:")
        print("  python Install_And_Run_Program.py --video example\ video.mp4")
        print("or")
        print("  python Install_And_Run_Program.py --verbose --venv TEST --video 'example video.mp4'\n")
        print("Powershell:")
        print("  python  .\Install_And_Run_Program.py --video example\ video.mp4")
        print("or")
        print("  python  .\Install_And_Run_Program.py --verbose --venv TEST --video 'example video.mp4'")
