# Python Obfuscate

Tool for iterating over python package directory and obfuscating all python files.
All other file extensions are copied in their original state.
Optionally minimizes the python code prior to obfuscation.

Examples:

    # obfuscate entire package
    obfuscate -vv -m /src/package /install/dir/package

    # obfuscate file
    obfuscate -vv -m myfile.py myfile_obs.py

### Options

- -v, --verbose    *output verbosity*
- -m, --minimize   *Minimize python code prior to obfuscation*
- -n, --dry-run    *Does not process any files (use with verbose to show process)*

## *__WARNING!__*

Code must be obfuscated on the system on which it inteded to be executed.
Changes to system/dependencies may break the functionality of the obfuscated code.