<%inherit file="base.mako" />
<div class="container_12">

    <p style="height: 30px"></p>
    <div id="searchd">
        <%include file="search_form.mako"/>
    </div>   
    <div class="prefix_1" style="margin-top: 24px"> 
        % if srch:
            <a href="/parts/search?searchd=${srch}">search query > ${srch}</a> > ${rp[0][0]} 
        % else:
            <a href="/parts/browse?${pg}${sl}${img}">browse</a> > ${rp[0][0]} 
        % endif
    </div>
    <div class="prefix_1">
    % for d in rp:
        <div class="post_title">${d[0]}</div> 
        <div class="author">by ${d[2]} </div>
        <span class="date">on ${d[3]}</span>
        <div><a href="${d[4]}" target="_blank">original forum post</a></div>
        <!--
        <div class="flags"> 
            <div id="flagMsg">Please flag with care:</div> 
            <ul class="flag">
                <li><a href="/parts/mark?list_id=${list_id}&type=best">awesome deal!</a></li>
                <li><a href="/parts/mark?list_id=${list_id}&type=sold">mark as sold</a></li>
                <li><a href="/parts/mark?list_id=${list_id}&type=spam">spam/overpost</a></li>
            </ul>
        </div>
        -->
        <div style="padding-top: 20px">${unicode(d[1], errors="ignore")}</div>
    % endfor
    </div>
   
</div>

<%def name="title()">
    GearFish: ${rp[0][0]} 
</%def>
