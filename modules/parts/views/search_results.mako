<%inherit file="base.mako" />
<%def name="title()">
    GearFish Search for: "${search_term}"
</%def>
<div class="container_12">
    <div id="searchd">
        <div id="title">Gear<span id="logo">Fish</span></div>       
        <%include file="search_form.mako"/>
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
                        % if d['excerpts']:
                            ${d['excerpts'][0]}                   
                        % endif
                    </div>  
                </div>
            % endfor
        % else:
            <b>No results found...</b>
        % endif
    </div>
    % if num_rows >= 20:
    <div id="paginate-search">
        % if current_page is not 1 and current_page is not 0:
            <a href="/parts/search?searchd=${search_term}&pg=${current_page - 1}${'&site=' + site if site else ''}${'&auth=' + auth if auth else ''}">prev ${limit} results</a>
            &nbsp;
            &nbsp;
            &nbsp;
            &nbsp;
        % endif  
        % if current_page is not last: 
            % if current_page is 0:
                <a href="/parts/search?searchd=${search_term}&pg=${current_page + 2}${'&site=' + site if site else ''}${'&auth=' + auth if auth else ''}"> 
                    next ${limit} results
                </a>
            % else:
                <a href="/parts/search?searchd=${search_term}&pg=${current_page + 1}${'&site=' + site if site else ''}${'&auth=' + auth if auth else ''}"> 
                    next ${limit} results
                </a>
            % endif
        % endif
    </div>
    % endif
</div>
