<%inherit file="base.mako" />
<%def name="title()">
    GearFish: Browse Parts
</%def>

<div class="container_12">
    <div id="searchd">
        <div id="title">Gear<span id="logo">Fish</span></div>       
        <form method="GET" action="/parts/search">
            <input type="text" name="searchd" value="" id="search_box_part_view" />
            <input type="submit" value="search" id="search_btn_part_view"/>
        </form>
        <div style="padding-top:10px">
            <form method="GET" action="/parts/browse">
            </form>
        </div>
    </div>

    <p style="height: 30px"></p>
    % if sl:
    <table>
        <tr>
            <td>
                <p>your selections</p>
            </td>
            <td valign="top">
                <div style="padding-left:10px">
                % if with_img:
                    <a href="/parts/browse?pg=${current_page}${connect_str or img_str_sl}${','.join([i for i in selected if chosen != i])}">
                        images[x]
                    </a>
                % endif

                    % if sl: 
                        % for choices in selected:
                            <a href="/parts/browse?pg=${current_page}${img_str}${connect_str}${','.join([i for i in selected if choices != i])}">
                                ${choices}[x]
                            </a>
                        % endfor
                    % endif
                </div>
            </td>
        </tr>
    </table>
    % endif

    <p style="height: 15px"></p>
    <table>
    <tr>
        <td valign="top" style="width:140px">
            <div style="padding-top:15px">
                <label>Filter posts by: </label>
                <div>
                <!--
                % if with_img == None:
                    <a href="/parts/browse?pg=${current_page}&with_img=1${connect_str}${img_str_sl}${','.join([i for i in selected if chosen != i])}">
                        with image
                    </a><br/>
                % endif
                -->

                % for site in remaining: 
                    <a href="/parts/browse?pg=${current_page}${img_str}&sl=${site.strip("'")},${','.join(selected)} ">${site.strip("'")}</a><br/>
                % endfor
                </div>
            </div>
        </td>
        <td>
            <div id="search_results"> 
                % for k, v in date_result.iteritems(): 
                    <div style="padding: 5px">
                         <p style="font-size: 2.5em; color: #CCCCCC">${k.strftime('%a %b %d')}</p>
                         % for i in v:
                             <div class="cl1 suffix_2">
                                 <div style="padding: 5px">
                                     <a class="le" style="font-size: 1.1em" 
                           href="/parts/view?list_id=${i[1]}${'&pg=%d' % [page for page in pages if current_page == page][0]}${'&sl=' + sl if sl else ''}${img_str if img_str else ''}"
                                         <b>${unicode(i[0], errors="ignore")}</b>
                                     </a>    
                                     <span id="brand"> ${i[1].split(":")[0]}</span>
                                 </div> 
                             </div>
                        % endfor
                    </div>
                % endfor
            </div>
        </td>
    </tr>
    </table>
    
    <div style="text-align: center">
        % if current_page is not 1:
            % if sl != None and with_img == None:
                <a href="/parts/browse?pg=${first}&sl=${sl}">first</a>
                <a href="/parts/browse?pg=${current_page - 1}&sl=${sl}"> << prev</a>
            % elif sl == None and with_img != None:
                <a href="/parts/browse?pg=${first}&with_img=1">first</a>
                <a href="/parts/browse?pg=${current_page - 1}&with_img=1"> << prev</a>
            % elif sl != None and with_img != None: 
                <a href="/parts/browse?pg=${first}&sl=${sl}&with_img=1">first</a>
                <a href="/parts/browse?pg=${current_page - 1}&sl=${sl}&with_img=1"> << prev</a>
            % else:
                <a href="/parts/browse?pg=${first}">first</a>
                <a href="/parts/browse?pg=${current_page - 1}"> << prev</a>
            % endif
        % endif 

        % for page in pages:
            % if current_page == page: 
               % if sl != None and with_img == None:
                    <a href="/parts/browse?pg=${page}&sl=${sl}"><b>${page}</b></a>
                % elif sl == None and with_img != None:
                    <a href="/parts/browse?pg=${page}&with_img=1"><b>${page}</b></a>
                % elif sl != None and with_img != None: 
                    <a href="/parts/browse?pg=${page}&sl=${sl}&with_img=1"><b>${page}</b></a>
                % else:
                    <a href="/parts/browse?pg=${page}"><b>${page}</b></a>
                % endif
            % else:
                % if sl != None and with_img == None:
                    <a href="/parts/browse?pg=${page}&sl=${sl}">${page}</a>
                % elif sl == None and with_img != None:
                    <a href="/parts/browse?pg=${page}&with_img=1">${page}</a>
                % elif sl != None and with_img != None: 
                    <a href="/parts/browse?pg=${page}&sl=${sl}&with_img=1">${page}</a>
                % else:
                    <a href="/parts/browse?pg=${page}">${page}</a>
                % endif
            % endif
        % endfor

        % if current_page is not last: 
            % if sl != None and with_img == None:
                <a href="/parts/browse?pg=${current_page + 1}&sl=${sl}"> next >> </a>
                <a href="/parts/browse?pg=${last}&sl=${sl}">last</a> 
            % elif sl == None and with_img != None:
                <a href="/parts/browse?pg=${current_page + 1}&with_img=1"> next >> </a>
                <a href="/parts/browse?pg=${last}&with_img=1">last</a>
            % elif sl != None and with_img != None: 
                <a href="/parts/browse?pg=${current_page + 1}&sl=${sl}&with_img=1"> next >> </a>
                <a href="/parts/browse?pg=${last}&sl=${sl}&with_img=1">last</a>
            % else:
                <a href="/parts/browse?pg=${current_page + 1}"> next >></a>
                <a href="/parts/browse?pg=${last}">last</a>
            % endif
        % endif
    </div>
</div>
