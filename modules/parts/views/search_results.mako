<%inherit file="base.mako" />
<%def name="title()">
    SprocketFish Search for: "${search_term}"
</%def>

<div class="container_12">
    <p style="height: 30px"></p>
    <div id="searchd">
        <form method="post" action="/parts/search">
            <input type="text" name="searchd" value="${search_term}" id="search_box" />
            <input type="submit" value="search" id="search_btn"/>
        </form>
    </div>  
    <p style="height: 30px"></p>

    <div id="search_results" class="prefix_2">
    % for post_id, title, list_id, sku, text, html, auth in rp.fetchall():
        <div class="crd1">
            <div style=""><a class="l le" href="/parts/view_topic/${sku}">${title}</a></div> 
        </div>
    % endfor
    </div>
</div>

