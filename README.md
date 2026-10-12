# Team Notes: an Assure demo

Team Notes is a small Flask app where a team keeps shared notes. It exists to show what
[Assure](https://github.com/Symbolia-Assurance/assure-action) checks on a pull request. It is not a product.

- Anyone can open the home page and the sign-in form.
- Members sign in with a password and then a one-time code. Then they can read and write notes.
- Admins can list members and remove notes.

The members, passwords and codes in `app/store.py` are fictional placeholders.

## Run it

```sh
pip install -r requirements.txt
TEAM_NOTES_SECRET_KEY=change-me flask --app app run
```

## How the check runs

The workflow in `.github/workflows/assure.yml` runs on every pull request. It sends the
repository files, `declaration.json` and `requirements.md` to the Assure API with the
`python-auth-declared-model` profile. The check reads the routes registered in the source,
the guards on each route and the session keys that `declaration.json` names. It does not
run the app.

- `declaration.json` tells the check how this app signs people in: the session key that
  holds the signed-in user, the two guards, the view that sets the user, and the public routes.
- `requirements.md` states the rules the app must keep, in sentences the check can read.

Each rule reads one of three words:

- **holds**: the check showed the rule is kept in this code.
- **not established**: the check could not show it either way, and it says why.
- **disproven**: the check found a route that breaks the rule, and it names the route and the line.

The check is green when nothing is disproven.

## Licence

Apache-2.0. See `LICENSE`.
