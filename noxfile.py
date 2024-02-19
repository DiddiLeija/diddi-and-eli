import nox

files = (
    "main.py",
    "noxfile.py",
    "src/__init__.py",
    "src/characters.py",
    "src/levels.py",
    "src/menu.py",
    "src/tools.py"
)

@nox.session
def format(session: nox.Session):
    "Format the codebase."
    session.install("-r", "requirements.txt")
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files, "--fix")  # TODO: ignore certain rules?

@nox.session
def lint(session: nox.Session):
    "Lint the codebase."
    session.install("-r", "requirements.txt")
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files)  # TODO: ignore certain rules?
