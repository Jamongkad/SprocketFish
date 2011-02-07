<html>
    <head> 

        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js" type="text/javascript"></script> 
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.3/jquery-ui.min.js" type="text/javascript"></script> 
        <script src="http://jquery-ui.googlecode.com/svn/tags/latest/external/jquery.bgiframe-2.1.1.js" type="text/javascript"></script> 
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.3/i18n/jquery-ui-i18n.min.js" type="text/javascript"></script>

        <!--
        <script type="text/javascript" src="/static/js/jquery.js"></script>
        <script type="text/javascript" src="/static/js/underscore-min.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.asmselect.js"></script>   
        -->

        <script type="text/javascript" src="/static/js/date.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.datePicker.js"></script>    
        <link rel="stylesheet" type="text/css" href="/static/css/sunguppy_1.2.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/reset.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/fluid_grid.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/jquery.asmselect.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/datePicker.css"></link>

        <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.3/themes/base/jquery-ui.css" type="text/css" media="all" /> 
        <link rel="stylesheet" href="http://static.jquery.com/ui/css/demo-docs-theme/ui.theme.css" type="text/css" media="all" /> 



        <title>${self.title()}</title>

    </head>
   <!-- First include the script: -->

    <script type="text/javascript">
        var mp_protocol = (("https:" == document.location.protocol) ? "https://" : "http://");
        document.write(unescape("%3Cscript src='" + mp_protocol + "api.mixpanel.com/site_media/js/api/mixpanel.js' type='text/javascript'%3E%3C/script%3E"));
    </script>


    <!-- Initialize it with your project token -->

    <script type="text/javascript">
        try {
            var mpmetrics = new MixpanelLib("3f80053e7a2c50d2919f7553c9dae366");
        } catch(err) {
            var null_fn = function () {};
            var mpmetrics = {
                track: null_fn,
                track_funnel: null_fn,
                register: null_fn,
                register_once: null_fn,
                register_funnel: null_fn,
                identify: null_fn
            };
        }

        mpmetrics.track("Unique Visitors");
        mpmetrics.track_funnel("Unique IP Visitors", 1, "View Homepage");

        $('a.browse-link').click(function() {
            mpmetrics.track('click browse', function() {
                window.location = "/parts/browse?pg=1";
            });
            return false;
        })
    </script> 

    <script type="text/javascript">
        $(function(){
            $('input[name="searchd"]').keyup(function() {
                var srchval = $(this).val();

                if(srchval.match(/@auth/)) {
                    var newval = /@auth:[a-zA-Z0-9_|]+/.exec(srchval);
                    $('input[name="auth"]').val(newval);
                } else { 
                    $('input[name="auth"]').val('');
                } 
                
                if(srchval.match(/@site/)) {
                    var newval = /@site:[a-zA-Z0-9_|]+/.exec(srchval);
                    $('input[name="site"]').val(newval);
                } else { 
                    $('input[name="site"]').val('');
                }
               
            }).focus().click(function() {  
                $('#searchexpand').slideDown();
            });

            $('#searchexpand, #helptext, .show-expando').hide();

            $("a.expando").click(function() {
                $('#helptext, .show-expando').slideDown();
                $('a.expando').slideUp();
                return false;  
            });

            $('a.show-expando').click(function() {
                $('#helptext, .show-expando').slideUp();
                $('a.expando').slideDown();
                return false;  
            });

        })
    </script>
    <body>
    <%! import header %>
    ${header.index().GET()}
    <div class="container_12"> 
        ${self.body()}  
    </div>

    <div class="footer">
        <a href="#">about</a> | <a href="#">legal</a> | <a href="#">twitter</a> | <a href="#">facebook</a> | <a href="#">suppliers</a>
        <div class="copy">&copy;2010 GearFish created by Mathew Wong</div>
        <br/>

        <p>  
        <a href="http://mixpanel.com/?from=partner"><img src="http://mixpanel.com/site_media/images/mixpanel_partner_logo.gif" alt="Mobile Analytics by Mixpanel" /></a>     
        </p>

    </div>
    </body>
</html>
