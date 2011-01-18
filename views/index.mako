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
        <table class="categories" cellspacing="5" cellpadding="0" border="0">
            <tr valign="top" style="height: 30px">
                <td align="center" colspan="4" style="padding-top: 5px;"><a class="browse-link" href="/parts/browse?pg=1">Browse Newest Items</a></td>
            </tr>
            <tr style="height: 30px;">
                <td id="forum_node"><a class="JDMU" href="/parts/browse?pg=1&sl=JDMU">JDMUnderground</a></td>
                <td id="forum_node"><a class="HCP" href="/parts/browse?pg=1&sl=HCP">Honda Club Philippines</a></td>
                <td id="forum_node"><a class="GT" href="/parts/browse?pg=1&sl=GT">Grupo Toyota</a></td>
                <td id="forum_node"><a class="MLPH" href="/parts/browse?pg=1&sl=MLPH">MitsuLancerPh, Inc.</a></td>
            </tr>
        </table>
    </center>
</div>

