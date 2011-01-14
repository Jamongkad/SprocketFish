<%inherit file="base.mako" />
<%def name="title()">
    GearFish Search for: "${search_term}"
</%def>
<div class="container_12">
    <div id="searchd">
        <div id="title">Gear<span id="logo">Fish</span></div>       
        <form method="GET" action="/parts/search">
            <input type="text" name="searchd" value="${search_term}" id="search_box" />
            <input type="submit" value="search" id="search_btn"/>
        </form>
    </div>  
    <p style="height: 30px"></p>
    <div id="search_results" class="prefix_1">
        % if rp:
            % for d in rp:
                <div class="crd1 cl1 suffix_2">
                    <div style="">
                        <a class="l le" href="/parts/view?list_id=${d['sku']}&searchd=${search_term}">${unicode(d['title'], errors="ignore")}</a>
                            <span id="brand"> ${d['sku'].split(":")[0]}</span></div> 
                    <div style="line-height: 1.4">
                        ${d['excerpts'][0]}                   
                    </div>
                </div>
            % endfor
        % else:
            <b>No results found...</b>
        % endif
    </div>
</div>
