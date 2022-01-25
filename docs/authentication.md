# Authentication

**User accounts** are stored and managed by **django framework**, however delegating to a **third party identity provider** could **improve the user experience** and so should be the **default option**.

## Register an identity provider

You will need to use the **superuser account** created during the [installation process](installation) to **register a third party identity provider**.

```{tip}
After **login with a third party account**, you can use your **superuser account** to grant him **administator permissions**.
```

## Identity providers

### Github

Register a **new OAuth app** within the github [developer settings page](https://github.com/settings/developers).

To **run locally**, set the **homepage URL** to `http://localhost:8000` and the **authorization callback URL** as `http://localhost:8000/accounts/github/login/callback`. 

Keep the **Client ID**, and generate a **Client Secret** to enable the access.

Go to the [Django Socialapp model](http://localhost:8000/admin/socialaccount/socialapp/) page using a **superuser account** and **dd a Github Provider** with the newly generated **Client ID** and **Client Secret** as **Secret Key**.

You can then [logout](http://localhost:8000/admin/logout/) from the administration and try to login using the github button from the [accounts/login](http://localhost:8000/accounts/login) page.