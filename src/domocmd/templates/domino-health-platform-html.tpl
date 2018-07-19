{% extends "layout.html" %} {% block content %}
<div class="row">
  <div class="col-lg-12">
    <h1 class="page-header" id="domo-page-title">Loading ...</h1>
  </div>
  <!-- /.col-lg-12 -->
</div>
<!-- /.row -->
<div class="row">
  <div class="col-lg-9">
    <div class="panel panel-default">
      <div class="panel-heading">
        Domino Total Servers
      </div>
      <!-- /.panel-heading -->
      <div class="panel-body">
          <table class="table">
              <thead >
                <tr>
                  <th>Statistic</th>
                  <th>Excelent</th>
                  <th>Good</th>
                  <th>Warning</th>
                  <th>Bad</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Platform.PagingFile.Total.PctUtil.Avg</td>
                  <td><= 10</td>
                  <td><= 20</td>
                  <td><= 60</td>
                  <td>> 60</td>
                </tr>  
              </tbody>
            </table>
      </div>
      <!-- /.panel-body -->
    </div>
    <!-- /.panel -->
  </div>
  <!-- /.col-lg-12 -->
  <div class="col-lg-3">
    <div class="panel panel-default">
      <div class="panel-heading">
        Export Files
      </div>
      <!-- /.panel-heading -->
      <div class="panel-body">
        <ul>
          <li>
            <a href="domino-health-platform.json">domino-health-platform.json</a>
          </li>
        </ul>
      </div>
      <!-- /.panel-body -->
    </div>
    <!-- /.panel -->
  </div>
  <!-- /.col-lg-12 -->
</div>
<!-- /.row -->
<div class="row">
  <div class="col-lg-12">
    <div class="panel panel-default">
      <div class="panel-heading">
        Domino Health
      </div>
      <!-- /.panel-heading -->
      <div class="panel-body">
        <table width="100%" class="table table-header-rotated">
          <thead id="domo-thead-update">
            <tr>
              <th>Server</th>
              <th class="rotate-45"><div><span>PF.PgFile.Total.PctUtil.Avg</span></div></th>
              <th>&nbsp;</th>
              <th class="rotate-45">.</th>
            </tr>
          </thead>
          <tbody id="domo-tbody-update">
            <tr>
              <td>ServerName</td>
              <td>
                <i class="fa fa-check-circle text-success" title="Platform.PagingFile.Total.PctUtil.Avg: 0.0 [Good]"></i>
              </td>
              <td>
                .
              </td>
            </tr>
          </tbody>
        </table>
        <!-- /.table-responsive -->
      </div>
      <!-- /.panel-body -->
    </div>
    <!-- /.panel -->
  </div>
  <!-- /.col-lg-12 -->
</div>
<!-- /.row -->
<div class="row">
    <div class="col-lg-12">
      <div class="panel panel-default">
        <div class="panel-heading">
          Domino Statistics
        </div>
        <!-- /.panel-heading -->
        <div class="panel-body">
          <table class="table">
            <thead >
              <tr>
                <th>Statistic</th>
                <th>Excelent</th>
                <th>Good</th>
                <th>Warning</th>
                <th>Bad</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Platform.PagingFile.Total.PctUtil.Avg</td>
                <td><= 10</td>
                <td><= 20</td>
                <td><= 60</td>
                <td>> 60</td>
              </tr>  
            </tbody>
          </table>
        </div>
        <!-- /.panel-body -->
      </div>
      <!-- /.panel -->
    </div>
    <!-- /.col-lg-12 -->
  </div>
  <!-- /.row -->
{% endblock %} {% block body_javascript %}
<script>
  $.getJSON('domino-health-platform.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      //_status_platform_pagingfile
      output += '<td>' + renderStat("Platform.PagingFile.Total.PctUtil.Avg",val.statistics) + '</td>';
      output += '<td>.</td>';
      output += '</tr>';
    });
    $('#domo-tbody-update').html(output);
  });

  
</script>
{% endblock %}