import nox

files = (
    "main.py",
    "noxfile.py",
    "src/__init__.py",
    "src/baseclasses.py",
    "src/characters.py",
    "src/levels.py",
    "src/menu.py",
    "src/tools.py"
)

@nox.session
def format(session: nox.Session):
    session.install("-r", "requirements.txt")
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files, "--fix")
