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
    <%! import re, nltk %>
    <div id="search_results" class="prefix_1">
        % for i in rp:
            % for d in i['obj_data']:
                <div class="crd1 cl1 suffix_2">
                    <div style="">
                        <a class="l le" href="/parts/view/${d[3]}">${unicode(d[1], errors="ignore")}</a>
                            <span id="brand"> ${d[3].split(":")[0]}</span></div> 
                    <div style="line-height: 1.4">
                        ##${" ".join(unicode(d[4], errors="ignore").split(" ")[0:40])}...
                       
                        ${nltk.sent_tokenize(unicode(d[4], errors="ignore"))}
                       
                    </div>
                </div>
            % endfor 
        % endfor
    </div>
</div>

