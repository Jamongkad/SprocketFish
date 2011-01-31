<%def name="search_form(params=False)">
    <form method="GET" action="/parts/search" id="searchform">
        <input type="text" name="searchd" value="${params if params else ""}" id="search_box" />
        <input type="hidden" name="auth" value="" />
        <input type="hidden" name="site" value="" />
        <input type="submit" value="search" id="search_btn"/>
    </form>
    <div id="searchexpand" class="infobar">
        <a class="expando" href="">advanced search: by website and author...</a>
        <a class="show-expando" href="">[close]</a>
        <div id="helptext">
            <p>
               Use the following search parameters to narrow your results. 
               In case you want to select multiple search options add the pipe 
               character "|".
            </p>
            <br/>
            <div class="helpnodes">
                <b>@auth:{username}</b>
                <p>
                    Return posts submitted by {username} only. For multiple authors
                    use {username1|username2|...} <br/>
                    <i>e.g. to filter all posts by jamongkad <b>@auth:jamongkad</b></i><br/>
                    <i>e.g. to filter all posts by jamongkad and stik <b>@auth:jamongkad|stik</b></i>
                </p>
            </div>

            <div class="helpnodes">
                <b>@site:{site}</b>
                <p>
                    Return posts filtered by {site} only. For multiple sites use
                    {site1|site2|...}. <br/>
                    <i>e.g. to filter all posts by Grupo Toyota <b>@site:gt</b></i><br/>
                    <i>e.g. to filter all posts by Grupo Toyota and Honda Club <b>@site:gt|hcp</b></i>
                </p>
            </div>
            <div class="helpnodes">
                <p>Search sample to look for spoon mags on both hcp and gt and posted by user jamongkad</p>
                <b><i>e.g. spoon mags @site:hcp|gt @auth:jamongkad</i></b>
            </div>
        </div>
    </div>
</%def>
