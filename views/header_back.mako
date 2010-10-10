<%!
    import app_globals 
    from forms import LoginAccountForm, CreateAccountForm
    from view import render
    import masthead

    login  = LoginAccountForm()
    create = CreateAccountForm()
%>

${masthead.index().GET('Marie')}

<div id="nav_holder">
<ul class="top_nav">
    <li><a href="/">SunGuppy!</a></li>
    <li><a href="/kids">SunGuppy Kids!</a></li>
</ul>

<ul class='nav'>
    <li><strong>Login</strong>
        <ul>
            <li>
                <form method="POST" action="/login">
                    % if login.username.errors:
                        % for error in login.username.errors:
                        <b>${error}</b>
                        % endfor
                    % endif
                    <div>${login.username.label}: ${login.username()}</div>

                    % if login.password.errors:
                        % for error in login.password.errors:
                        <b>${error}</b>
                        % endfor
                    % endif
                    <div>${login.password.label}: ${login.password()}</div>
                    <input type="submit" value="submit" />
                </form>
            </li>
        </ul>
    </li> 

    <li><strong>Create your account now!</strong>
        <ul>
            <li>
                <form method="POST" action="/create_account">
                    % if create.username.errors:
                        % for error in create.username.errors:
                        <b>${error}</b>
                        % endfor
                    % endif
                    <div>${create.username.label}: ${create.username()}</div>

                    % if create.password.errors:
                        % for error in create.password.errors:
                        <b>${error}</b>
                        % endfor
                    % endif
                    <div>${create.password.label}: ${create.password()}</div>
                    <input type="submit" value="submit" />
                </form>
            </li>
        </ul>
    </li>

    <li><strong>account</strong>
        <ul>
            <li><a href="/logout">logout</a>
        </ul>
    </li>
</ul>
</div>

<div>

</div>
