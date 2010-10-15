<!--
${mast}
${logged_in}
-->
<div id="nav_holder">
    <ul class="sprocket_nav">
        <!--<li><strong><a href="/">SprocketFish</a></strong></li>-->
        <li><strong><a href="/">Parts</a></strong></li>
        <li><strong><a href="/">Categories</a></strong></li>
        <li><strong><a href="/">Tools</a></strong></li>
    </ul>

    <ul class="nav">
        % if not logged_in:
            <li><strong><a href="/site/sa/login">Login</a></strong></li>
            <li><strong><a href="/site/sa/register">Register</a></strong></li>
        % else:
            <li><strong>account</strong>
                <ul>
                    <li><a href="/logout">logout</a>
                </ul>
            </li>
        % endif
        
    </ul>
</div>

<div>

</div>
