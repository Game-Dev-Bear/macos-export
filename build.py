import os, shutil, stat

PYPATH = "/Library/Frameworks/Python.framework/Versions"
DEFAULT_VER = "Current"
EXEC_DATA = [
    "#!/bin/bash\n",
    "cd \"$(dirname \"$0\")/../Resources\"\n",
    "open -a Terminal ./run"
]
RUN_DATA = [
    "#!/bin/bash\n",
    "cd \"$(dirname \"$0\")\"\n",
    "./Python/bin/python3.10 main.py\n"
]
DEL_FILES = [".tiff",".icns",".png"]

def export(FILES=None, REQUIREMENTS=None, EXTRA=None, ICON=None, NAME=None, VERSION=None):

    # Globals
    global PYPATH, DEFAULT_VER, EXEC_DATA, RUN_DATA

    # Defaults
    ICON = ICON or None
    NAME = NAME or "Made with PyMacBuilder"
    NAME = NAME.replace(" ", "-")
    NAME_NO_APP = NAME
    NAME = NAME + ".app"
    VERSION = VERSION or DEFAULT_VER
    REQUIREMENTS = REQUIREMENTS or []

    # Create some variablese
    print("Setting up data")
    APP = f'build/{NAME}'
    RES = f'{APP}/Contents/Resources'
    RUN = f'{APP}/Contents/MacOS/{NAME_NO_APP}'

    # Create the build path
    print("Creating the build path")
    if not os.path.exists("build"):
        os.mkdir("build")
    
    # Delete old builds
    print("Deleting old builds")
    if os.path.exists(APP):
        shutil.rmtree(APP)

    # Build the basic structure
    print("Creating the structure")
    os.mkdir(APP)
    os.mkdir(f'{APP}/Contents')
    os.mkdir(f'{APP}/Contents/MacOS')
    os.mkdir(RES)

    # Start creating the exec/run bash file
    print("Creating run and exec")
    with open(RUN, "w") as f:
        f.writelines(EXEC_DATA)
        f.close()
    with open(RES+"/run", "w") as f:
        f.writelines(RUN_DATA)
        f.close()
    st = os.stat(RUN)
    os.chmod(RUN, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    st = os.stat(RES+"/run")
    os.chmod(RES+"/run", st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # Load all the files
    print("Loading all files")
    shutil.copy("main.py", RES)
    if FILES:
        for f in FILES:
            shutil.copy(f, RES)
    print("Loading all files")
    if EXTRA:
        for f in EXTRA:
            shutil.copytree(f, RES+"/"+f)
    
    # Install Python locally
    print("Installing python")
    shutil.copytree(PYPATH+"/3.10", RES+"/Python")

    # Remove unwanted packages
    print("Deleting all packages")
    for f in os.listdir(RES+"/Python/lib/python3.10"):
        try:
            if os.path.isfile(RES+"/Python/lib/python3.10/"+f):
                os.remove(RES+"/Python/lib/python3.10/"+f)
            else:
                shutil.rmtree(RES+"/Python/lib/python3.10/"+f)
        except:
            pass
    print("Deleting odd files")
    for f in os.listdir(RES+"/Python/lib/"):
        end=False
        for d in DEL_FILES:
            if f.endswith(d):
                os.remove(RES+"/Python/lib/"+f)
                end=True
        if end: continue
    print("Deleting share")
    shutil.rmtree(RES+"/Python/share")
    print("Deleting Resources")
    shutil.rmtree(RES+"/Python/Resources")
    print("Adding site package directory")
    os.mkdir(RES+"/Python/lib/python3.10/site-packages")
    print("Loading site packages")
    for package in REQUIREMENTS:
        os.system(f'pip install --target={RES+"/Python/lib/python3.10/site-packages"} {package}')

export()