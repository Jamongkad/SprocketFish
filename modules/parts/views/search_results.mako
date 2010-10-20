<%inherit file="base.mako" />
<%def name="title()">
    GearFish Search for: "${search_term}"
</%def>

<div class="container_12">
    <p style="height: 30px"></p>
    <div id="searchd">
        <form method="GET" action="/parts/search">
            <input type="text" name="searchd" value="${search_term}" id="search_box" />
            <input type="submit" value="search" id="search_btn"/>
        </form>
    </div>  
    <p style="height: 30px"></p>
    <%! import re, nltk %>
    <div id="search_results" class="prefix_1">
        % for d in rp:
            <div class="crd1 cl1 suffix_2">
                <div style="">
                    <a class="l le" href="/parts/view/${d['sku']}">${unicode(d['title'], errors="ignore")}</a>
                        <span id="brand"> ${d['sku'].split(":")[0]}</span></div> 
                <div style="line-height: 1.4">
                    ${d['excerpts'][0]}                   
                </div>
            </div>
        % endfor 
    </div>
</div>
