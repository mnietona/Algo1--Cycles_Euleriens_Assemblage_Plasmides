def __exit(msg):
    import pytest
    pytest.exit(msg)

def __try_to_load(mod, name=None):
    import importlib
    mod_name = mod if name is None else f'{mod}.{name}'
    try:
        mod = importlib.import_module(mod)
        if name is not None:
            mod.__dict__[name]
    except (ImportError, NameError):
        log_msg = f'Impossible de charger {mod_name}. Vérifiez votre installation'
        __exit(log_msg)

def pytest_configure(config, *args, **kwargs):
    import sys
    if sys.version_info.major != 3:
        __exit('Projet à rendre en Python 3')
    requirements = [
        ('difflib', 'SequenceMatcher'),
        ('io', 'StringIO'), ('contextlib', 'redirect_stdout')
    ]
    for mod, name in requirements:
        __try_to_load(mod, name)

