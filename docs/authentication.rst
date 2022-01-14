Authentication
==============

To provide a fast and easy experience, default authentication mecanism is fully delegated to a third party entity.

Github
------

Register a new application within your `github developer settings page <https://github.com/settings/developers>`_

To run locally, you can set values to : 

```
http://localhost:8000
http://localhost:8000/accounts/github/login/callback
```

Generate a secret Key and within Django administration reate a social applications from github with both values

Within django administration create the following Social Application with Github.

Go to /accounts/login and click on github button to login and access the application