# Usage

## Authentification

This system uses **Django's built-in user management** for storing and managing user accounts. 

However, it also supports using a **third-party identity provider** to improve the user experience and make it the default option.

## Third-Party Identity Provider

To register a **third-party identity provider**, you will need to use the **superuser account** created during the [installation process](installation).

```{tip}
After logging in with a third-party account, you can use your superuser account to grant that user administrator permissions.
```

#### GitHub

- Register a new **OAuth app** on GitHub's [Developer Settings page](https://github.com/settings/developers).
- For local development, set the homepage URL to `http://localhost:8000` and the authorization callback URL to `http://localhost:8000/accounts/github/login/callback`.
- Keep the **Client ID** and generate a **Client Secret** to enable access.
- Go to the **Django Socialapp model** page using a superuser account and add a GitHub Provider with the newly generated Client ID and Client Secret as the Secret Key.
- Log out of the administration and try logging in using the GitHub button on the `accounts/login` page.
