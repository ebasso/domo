{% extends "layout.html" %} {% block content %}
<div class="row">
    <div class="col-lg-12">
        <h1 class="page-header" id="domo-page-title">Em Desenvolvimento ...</h1>
    </div>
    <!-- /.col-lg-12 -->
</div>
<div id="domo-boards-area">
    <div class="row">
            <div class="col-lg-3 col-md-6">
                <div class="panel panel-primary">
                    <div class="panel-heading">
                        <div class="row">
                            <div class="col-xs-3">
                                <i class="fa fa-tasks fa-5x"></i>
                            </div>
                            <div class="col-xs-9 text-right">
                                <div class="huge">NN</div>
                                <div>Loading ...</div>
                            </div>
                        </div>
                    </div>
                    <a href="#">
                        <div class="panel-footer">
                            <span class="pull-left">View Details</span>
                            <span class="pull-right">
                                <i class="fa fa-arrow-circle-right"></i>
                            </span>
                            <div class="clearfix"></div>
                        </div>
                    </a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="panel panel-green">
                    <div class="panel-heading">
                        <div class="row">
                            <div class="col-xs-3">
                                <i class="fa fa-mobile fa-5x"></i>
                            </div>
                            <div class="col-xs-9 text-right">
                                <div class="huge">NN</div>
                                <div>Loading ...</div>
                            </div>
                        </div>
                    </div>
                    <a href="#">
                        <div class="panel-footer">
                            <span class="pull-left">View Details</span>
                            <span class="pull-right">
                                <i class="fa fa-arrow-circle-right"></i>
                            </span>
                            <div class="clearfix"></div>
                        </div>
                    </a>
                </div>
            </div>
            <div class="col-lg-3 col-md-6">
                <div class="panel panel-red">
                    <div class="panel-heading">
                        <div class="row">
                            <div class="col-xs-3">
                                <i class="fa fa-comments fa-5x"></i>
                            </div>
                            <div class="col-xs-9 text-right">
                                <div class="huge">NN</div>
                                <div>Loading ...</div>
                            </div>
                        </div>
                    </div>
                    <a href="#">
                        <div class="panel-footer">
                            <span class="pull-left">View Details</span>
                            <span class="pull-right">
                                <i class="fa fa-arrow-circle-right"></i>
                            </span>
                            <div class="clearfix"></div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
        <!-- /.row -->
</div>
<!-- domo-boards-area -->
<div class="row">
    <div class="col-lg-8">
        <div class="panel panel-default">
            <div class="panel-heading">
                <i class="fa fa-bell fa-fw"></i> Notifications Panel
            </div>
            <!-- /.panel-heading -->
            <div class="panel-body">
                <div class="list-group" id="domo-panel-notificatin-body">
                    <a href="#" class="list-group-item">
                        <i class="fa fa-comment fa-fw"></i> Loading ...
                        <span class="pull-right text-muted small">
                            <em>N minutes ago</em>
                        </span>
                    </a>
                    <a href="#" class="list-group-item">
                        <i class="fa fa-twitter fa-fw"></i> Loading ...
                        <span class="pull-right text-muted small">
                            <em>NN minutes ago</em>
                        </span>
                    </a>
                    <a href="#" class="list-group-item">
                        <i class="fa fa-shopping-cart fa-fw"></i> Loading ...
                        <span class="pull-right text-muted small">
                            <em>HH:MM AM</em>
                        </span>
                    </a>
                    <a href="#" class="list-group-item">
                        <i class="fa fa-money fa-fw"></i> Loading ...
                        <span class="pull-right text-muted small">
                            <em>Yesterday</em>
                        </span>
                    </a>
                </div>
                <!-- /.list-group -->
                <a href="#" class="btn btn-default btn-block">View All Alerts</a>
            </div>
            <!-- /.panel-body -->
        </div>
    </div>
    <!-- /.col-lg-12 -->
</div>
<!-- /.row -->
{% endblock %}
{% block body_javascript %}
<script>
    $.getJSON('dashboard.json', function (data) {
        console.log(data);
        $('#domo-page-title').html(data.title + ' - ' + data.now);
        var output = '<div class="row">';
        var i = 0;
        $.each(data.panels, function (key, val) {
            if (i > 3) {
                output += '</div><!-- /.row --><div class="row">';
                i = 0;
            }
            output += '<div class="col-lg-3 col-md-6">';
            output += '<div class="panel ' + val.pn + '">';
            output += '<div class="panel-heading"><div class="row"><div class="col-xs-3">';
            output += '<i class="fa ' + val.icon + ' fa-5x"></i>';
            output += '</div><div class="col-xs-9 text-right">';
            output += '<div class="huge">' + val.num + '</div>';
            output += '<div>' + val.msg + '</div>';
            output += '</div></div></div>';
            output += '<a href="' + val.href + '">';
            output += '<div class="panel-footer"><span class="pull-left">View Details</span><span class="pull-right">';
            output += '<i class="fa fa-arrow-circle-right"></i></span><div class="clearfix"></div></div></a></div></div>';
            i++;
        });
        output += '</div><!-- /.row -->';
        $('#domo-boards-area').html(output);
    });
  $.getJSON('dashboard-notifications.json', function (data) {
        //console.log(data);
        var output = '';
        $.each(data, function (key, val) {
            output += '<a href="' + val.href + '" class="list-group-item">';
            output += '<i class="fa ' + val.icon + ' fa-fw"></i> ' + val.msg;
            output += '<span class="pull-right text-muted small"><em>'+ val.when + '</em></span></a>';
        });
        $('#domo-panel-notificatin-body').html(output);
  });
</script>
{% endblock %}