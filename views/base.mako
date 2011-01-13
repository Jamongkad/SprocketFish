<html>
    <head> 
        
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js" type="text/javascript"></script> 
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.3/jquery-ui.min.js" type="text/javascript"></script> 
        <script src="http://jquery-ui.googlecode.com/svn/tags/latest/external/jquery.bgiframe-2.1.1.js" type="text/javascript"></script> 
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.3/i18n/jquery-ui-i18n.min.js" type="text/javascript"></script>
        <script type="text/javascript" src="http://ajax.microsoft.com/ajax/jquery.validate/1.7/jquery.validate.min.js"></script>
        <script type="text/javascript" src="https://github.com/malsup/form/raw/master/jquery.form.js?v2.4"></script>

        <script type="text/javascript" src="/static/js/underscore-min.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.asmselect.js"></script>   

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

        $('a.browse-link').click(function() {
            mpmetrics.track('click browse', {'nav item' : 'browse'}, function() {
                window.location = "http://www.gearfish.com/parts/browse?pg=1";
            });
            return false;
        })
    </script> 
    <body>
    <%! import header %>
    ${header.index().GET()}
    <div class="container_12"> 
        ${self.body()}  
    </div>

    <div style="text-align: center; margin-top: 100px; margin-bottom: 100px;  font-size: 10px">
        about | legal | twitter | facebook | suppliers | &copy;2010 GearFish
        <br/><br/>
        <p>
        <a href="http://mixpanel.com/?from=partner"><img src="http://mixpanel.com/site_media/images/mixpanel_partner_logo.gif" alt="Mobile Analytics by Mixpanel" /></a>
        </p>
    </div>
    </body>
</html>
