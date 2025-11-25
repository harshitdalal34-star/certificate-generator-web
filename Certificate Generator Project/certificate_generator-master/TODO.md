# TODO: Add Basic Login System to Certificate Generator

## Steps to Complete
- [x] Create `users.json` file in project root for storing user credentials.
- [x] Update `app.py`:
  - [x] Add necessary imports (json, werkzeug.security, flask.session).
  - [x] Configure Flask session secret key.
  - [x] Add helper functions for loading/saving users and password hashing.
  - [x] Add `/login` route (GET/POST) for sign-in.
  - [x] Add `/signup` route (GET/POST) for sign-up.
  - [x] Add `/logout` route for logging out.
  - [x] Protect `/` and `/generate` routes with login checks (redirect to login if not authenticated).
- [x] Create `templates/login.html` with form for username/password and error display.
- [x] Create `templates/signup.html` with form for username/password and error display.
- [x] Update `templates/index.html` to add logout button.
- [x] Test the implementation:
  - [x] Sign up a new user.
  - [x] Log in with valid credentials.
  - [x] Access certificate generator after login.
  - [x] Try accessing without login (should redirect).
  - [x] Log out and verify access blocked.
  - [x] Check users.json is updated correctly.
  - [x] Verify certificate generation still works as before.
