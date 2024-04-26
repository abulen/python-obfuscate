import os
import setuptools


def read(file):
    with open(os.path.join(os.path.dirname(__file__), file)) as infile:
        return infile.read()


__version__ = None
with open('obfuscate/__init__.py', 'r') as f:
    exec(next(line for line in f if "__version__" in line))

BRANCH = os.environ.get('GIT_BRANCH', None)
if BRANCH:
    BRANCH = BRANCH.replace("/", "_").replace("\\", "_")
BUILD = os.environ.get("BUILD_NUMBER", None)
COMMIT = os.environ.get('GIT_COMMIT', None)
TAG = os.environ.get('GIT_TAG', None)
if TAG:
    TAG = TAG.replace("/", "_").replace("\\", "_")

VERSION_STRING = ''.join(__version__)

if TAG:
    VERSION_STRING += f'.v{TAG}'
elif BRANCH != 'main' and BRANCH != 'master':
    VERSION_STRING += f'.dev{BUILD or 1}'
else:
    VERSION_STRING += f'.{BUILD or 1}'

if COMMIT:
    if BRANCH != 'main' and BRANCH != 'master':
        VERSION_STRING += f'+{BRANCH}-{COMMIT:.7}'

SETUP_PARAMS = {
    'name': 'python-obfuscate',
    'version': VERSION_STRING,
    'packages': setuptools.find_packages(include=('obfuscate', )),
    'url': 'https://github.com/abulen/python-obfuscate',
    'license': 'MIT',
    'author': 'Andrew Bulen',
    'author_email': 'anbulen@gmail.com',
    'description': 'Creates duplicated version of python directory with obfuscated code',
    'long_description': read('README.md'),
    'python_requires': '>=3.0',
    'install_requires': [
        'python-minimize',
    ],
    'extras_require': {
        'dev': [
            'pytest',
            'pytest-cov',
            'coverage',
        ]
    },
    'entry_points': {
        'console_scripts': [
            'obfuscate=obfuscate.obfuscate:main',
        ]
    }
}