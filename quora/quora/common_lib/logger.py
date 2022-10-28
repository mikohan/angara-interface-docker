import pathlib, os
from django.conf import settings


def logger(string, filename, dirname="common"):
    """
    Logging strings to BASE_DIR/logs/{dirnam}/{filename}
    dirname and filename needs to be passed as parameters
    """
    path = os.path.join(settings.BASE_DIR, "logs", dirname)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    final_path = os.path.join(path, filename)

    with open(final_path, "w") as file:
        file.write(string + "\n")
