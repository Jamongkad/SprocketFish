<html>
    <head> 
        <script type="text/javascript" src="/static/js/jquery.js"></script>
        <script type="text/javascript" src="/static/js/underscore-min.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.asmselect.js"></script>   

        <script type="text/javascript" src="/static/js/date.js"></script>   
        <script type="text/javascript" src="/static/js/jquery.datePicker.js"></script>   
        <link rel="stylesheet" type="text/css" href="/static/css/sunguppy_1.2.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/reset.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/fluid_grid.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/jquery.asmselect.css"></link>
        <link rel="stylesheet" type="text/css" href="/static/css/datePicker.css"></link>


        <title>${self.title()}</title>

    </head>
    <body>
    <%! import header %>
    ${header.index().GET()}
    <div class="container_12"> 
        ${self.body()}  
    </div>

    <div style="text-align: center; margin-top: 100px; margin-bottom: 100px;  font-size: 10px">
        about | legal | twitter | facebook | suppliers | &copy;2010 sprocketfish
    </div>
    </body>
</html>
