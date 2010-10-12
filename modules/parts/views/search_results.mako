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

    <div id="search_results" class="prefix_1">
    % for post_id, title, list_id, sku, text, html, auth in rp.fetchall():
        <div class="crd1 cl1 suffix_3">
            <div id="brand">${sku.split(":")[0]}</div>
            <div style=""><a class="l le" href="/parts/view_topic/${sku}">${title}</a></div> 
            <%! import re %>
            <div>${" ".join(unicode(text, errors="ignore").split(" ")[0:40])}...</div>
        </div>
    % endfor
    </div>
</div>

