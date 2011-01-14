<%inherit file="base.mako" />
<%def name="title()">
    GearFish 
</%def>

<script type="text/javascript">
    $(function(){
        $('input[name="searchd"]').focus();
    })
</script>

<div style="text-align:center">
    <div id="title">Gear<span id="logo">Fish</span></div>       
    <div id="searchd">
        <form method="GET" action="/parts/search" id="searchform">
            <input type="text" name="searchd" value="" id="search_box" />
            <input type="submit" value="search" id="search_btn"/>
        </form>
        <p id="desc_text">GearFish is an auto enthusiast powered search engine.</p>
    </div> 
    <center>
    <p id="category_text">Browse by Forum Source</p>
 
    <table>
        <tr>
            % for site in sites:
                <td id="forum_node"><a class="${site.site_nm}" href="/parts/browse?pg=1&sl=${site.site_nm}">${site.site_nm}</a></td> 
            % endfor
        </tr>
    </table>
    </center>
</div>

