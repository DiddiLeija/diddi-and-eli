import nox

nox.options.sessions = ("format", "lint")

files = (
    "main.py",
    "noxfile.py",
    "src/__init__.py",
    "src/characters.py",
    "src/levels.py",
    "src/menu.py",
    "src/tools.py",
)


@nox.session
def format(session: nox.Session):
    "Format the codebase."
    session.install("-r", "requirements.txt")
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files, "--fix")
    session.run("ruff", "format", *files)  # an important reinforcement to 'ruff check --fix'


@nox.session
def lint(session: nox.Session):
    "Lint the codebase."
    session.install("-r", "requirements.txt")
    session.install("-r", "test-requirements.txt")
    session.run("ruff", "check", *files)


@nox.session(name="reset-savedata")
def reset_savedata(session: nox.Session):
    "Clean up 'savedata.json', which should not have any contents, use it carefully."
    new_data = '{"level": "intro", "saved_coins": 0}'
    session.run(
        "python",
        "-c",
        "import io; js = io.open('savedata.json', 'w'); " f"js.write('{new_data}'); " "js.close()",
    )
