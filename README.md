# Team Notes: an Assure demo

**Your AI writes the code. Assure checks it before it ships.**

Team Notes is a small Flask app where a team keeps shared notes. It exists to show, on real pull requests,
what [Assure](https://github.com/Symbolia-Assurance/assure-action) checks on every change. It is not a product.

> **Early access opens 13 October 2026.** Free to start. Join the community Discord (link in the launch post)
> and we'll set Assure up on your repository.

## See it work: three pull requests

| Pull request | What changed | What Assure said |
|---|---|---|
| [#1 Add Assure](https://github.com/Symbolia-Assurance/assure-demo/pull/1) | Adds the Assure check to the workflow | **green**: every rule in `requirements.md` holds; 2 catalogue checks not established, each with its reason |
| [#2 Agent: add CSV export for admins](https://github.com/Symbolia-Assurance/assure-demo/pull/2) | An AI-style change adds `GET /admin/export` and forgets the sign-in guard | **red**: `R1 — disproven — app/__init__.py:107`, the route reachable without signing in |
| #2, after the fix | Adds `@login_required` and `@admin_required` to the export | **green** again: every rule holds |

Open a pull request's **Checks** tab and expand the **Assure check** step to read the full result. Runs on `main` also
keep the full result as a downloadable file (`assure-verdict`, under the run's artefacts).

## Your rules, in plain English: `requirements.md`

```markdown
- R1 [auth]: No route outside the declared public routes is reachable without signing in.
- R2 [auth]: Routes that carry a declared role guard are reachable only by that role.
- R3 [auth]: The signed-in identity is set only after second-factor verification.
- R4 [auth]: Signing out always returns to the signed-out state.
```

Each rule is checked on every pull request, and each reading names its evidence: the route, the guard and the
line. A rule the check cannot decide reads **not established** and says what it needs. It never reads as a pass.

## Three words

- **holds**: the check showed the rule is kept in this code.
- **not established**: the check could not show it either way, and it says why.
- **disproven**: the check found where the code breaks the rule, and names the route and the line.

The check is green when nothing is disproven.

## What the check reads

The check reads the source; it does not run the app. For this app it read ten routes, the two guards
(`login_required`, `admin_required`) on each, and the session keys `declaration.json` names:

| Route | Guards |
|---|---|
| `GET /`, `GET /login`, `POST /login`, `POST /login/code`, `POST /logout` | public |
| `GET /notes`, `POST /notes`, `GET /notes/<id>` | `login_required` |
| `GET /admin/users`, `POST /admin/notes/<id>/delete` | `login_required`, `admin_required` |

- `declaration.json` tells the check how this app signs people in: the session key that holds the signed-in
  user, the two guards, the view that sets the user, and the public routes.
- `requirements.md` states the rules the app must keep.

## Add Assure to your repository

1. Copy `.github/workflows/assure.yml` into your repository.
2. Add your `declaration.json` and a `requirements.md` at the root (start from this repository's).
3. Add an `ASSURE_API_KEY` repository secret. During early access we issue keys from the Discord.

The workflow here includes a short step that packs the repository files for the check. A one-step version of the
Action, and sign-in with GitHub's own workflow identity instead of a stored key, are on the way.

**Served today:** Python (Flask) sign-in, PostgreSQL and HTTP configuration. More frameworks are in progress.

## Premium (USD 20 a month, early access)

Premium builds a formal model of your app's sign-in once, when you upgrade, and checks rules that go beyond the
catalogue, in your own words. During early access we run the first build with you.

## What Assure does not claim

It checks what it reads and names what it could not read. It does not run your app, certify a deployment, or call
code secure. A rule it cannot decide stays **not established**, with the reason.

## Run the app

```sh
pip install -r requirements.txt
TEAM_NOTES_SECRET_KEY=change-me flask --app app run
```

The members, passwords and codes in `app/store.py` are fictional placeholders.

## Licence

Apache-2.0. See `LICENSE`.
