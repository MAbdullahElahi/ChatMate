from setuptools import setup
from datetime import date


year = date.today().year

APP = ["main.py"]
DATA_FILES = [
    "chatmate.gif"
]
OPTIONS = {
    "packages": ["methods.cpython-311.pyc", "openai", "aiohttp"],
    "iconfile": "chatmate.gif",
    "plist": {
        "CFBundleDevelopmentRegion": "English",
        "CFBundleIdentifier": "com.mabdulalhelahi.elahinexustech",
        "CFBundleVersion": "1.0 BETA",
        "NSHumanReadableCopyright": f"Copyright © {year}, ElahiNexusTech,  All Rights Reserved",
        "LSMinimumSystemVersion": "11.0.0"
    },
}

setup(
    app=APP,
    name="ChatMate",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)