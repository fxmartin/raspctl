<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Login &middot; RaspCTL</title>
    <meta name="author" content="Jan Carreras Prat">
    <link href="/static/css/bootstrap.css" rel="stylesheet">
    <link href="/static/css/login.css" rel="stylesheet">
    <link href="/static/css/bootstrap-responsive.css" rel="stylesheet">
</head>

<body>
    <noscript>
        <div class="error message" style="color: red; text-align:center;">
            <h3>Ooops!</h3>
            <p>
                I'm sorry! I've detected that you are blocking JavaScript (And I'm cool with that!) but this
                site just works <b>if JavaScript is enabled</b>.<br /> 
                Please, consider to whitelist this site for being able to use it. Thanks!
            </p>
        </div>
		<br />
    </noscript>

    <div class="container">
      <form class="form-signin" method="post" action="/login">
        <h2 class="form-signin-heading">Please sign in</h2>
        <input type="text" class="input-block-level" placeholder="Username" name="username">
        <input type="password" class="input-block-level" placeholder="Password" id="password" name="password">
        <div style="text-align: center">
            <button class="btn btn-large btn-primary" type="submit">Sign in</button>
        </div>
      </form>
    </div>
  </body>
</html>
