{% extends "layout.html" %} {% block content %}
<div class="row">
  <div class="col-lg-12">
    <h1 class="page-header">Disk Report - {{now}}</h1>
  </div>
  <!-- /.col-lg-12 -->
</div>
<!-- /.row -->
<div class="row">
  <div class="col-lg-9">
    <div class="panel panel-default">
      <div class="panel-heading">
        Disk Usage Environment
      </div>
      <!-- /.panel-heading -->
      <div class="panel-body">
        <span style="font-size:28px">Servers #: &nbsp;&nbsp;
          <span style="font-size: 75%;color: #777">{{server_count}}</span>
        </span>
        <br>
        <span style="float:left; font-size:28px">Total: &nbsp;&nbsp;</span>
        <div class='bar'>
          <div class="progress" style="float:left; width:300px; height:40px; ">
            <div class="{% if (environment_used_total_perc >= 89) %}
            progress-bar progress-bar-danger
            {% elif (environment_used_total_perc >= 75) %}
            progress-bar progress-bar-warning
            {% else %}
            progress-bar progress-bar-success
            {% endif %}" style="width:{{environment_used_total_perc * 3}}px"></div>
          </div>
          <span style="float:left; font-size:28px">&nbsp;&nbsp;
            <span style="font-size: 75%;color: #777">({{ environment_used_total_human }} / {{ environment_size_total_human }}) - {{ environment_used_total_perc}}%
            </span>
          </span>
          <div style="clear:both"></div>
        </div>
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
            <a href="report-disks.csv">report-disks.csv</a>
          </li>
          <li>
            <a href="report-disks.txt">report-disks.txt</a>
          </li>
          <li>
            <a href="report-disks.json">report-disks.json</a>
          </li>
          <li>
            <a href="report-disks.sql">report-disks.sql</a>
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
        Disk Usage by Server
      </div>
      <!-- /.panel-heading -->
      <div class="panel-body">
        <table width="100%" class="table">
          <thead>
            <tr>
              <th>Server</th>
              <th>Disk Usage Total</th>
              <th>Disk Usage Details</th>
            </tr>
          </thead>
          <tbody id="tbody-update">
          </tbody>
        </table>
        <!-- /.table-responsive -->
      </div>
      <!-- /.panel-body -->
    </div>
    <!-- /.panel panel-default -->
  </div>
  <!-- /.col-lg-12 -->
  <!-- /.panel-body -->
</div>
<!-- /.row -->
{% endblock %}
{% block body_javascript %}
<script>
  $.getJSON('report-disks.json', function (data) {
    console.log(data);
    var output = '';
    $.each(data.servers, function (key, val) {
      output += '<tr>';
      output += '<td>' + val.name + '</td>';
      output += '<td><div class="bar"><div class="progress" style="float:left; width:100px; height:16px; margin-bottom:1px;"><div class="progress-bar ';
      output += (val.disks_used_total_perc >= 89) ? ('progress-bar-danger') : ((val.disks_used_total_perc >= 75) ? ('progress-bar-warning') : ('progress-bar-success'))
      output += '" style="width:' + val.disks_used_total_perc + 'px">';
      output += '</div></div><span style="float:left; font-size:12px">&nbsp;&nbsp;Total <span style="font-size: 75%;color: #777">';
      output += '(' + val.disks_used_total_human + ' / ' + val.disks_size_total_human + ') - ' + val.disks_used_total_perc + '%';
      output += '</span></span><div style="clear:both"></div></td>';
      output += '<td>';
      $.each(val.disks, function (key2, val2) {
        output += '<div class="bar"><div class="progress" style="float:left; width:100px; height:16px; margin-bottom:1px;">';
        output += '<div class="progress-bar ';
        if (val2.label.indexOf('logdir') != -1) {
          output += (val2.used_perc >= 50) ? ('progress-bar-danger') : ((val2.used_perc >= 45) ? ('progress-bar-warning') : ('progress-bar-success'));
        } else {
          output += (val2.used_perc >= 89) ? ('progress-bar-danger') : ((val2.used_perc >= 75) ? ('progress-bar-warning') : ('progress-bar-success'));
        }
        output += '" style="width:'+ val2.used_perc + 'px">';
        output += '</div></div>';
        output += '<span style="float:left; font-size:12px">&nbsp;&nbsp;' + val2.label;
        output += '  <span style="font-size: 75%;color: #777">';
        output += '(' + val2.used_human + ' / ' + val2.size_human + ') - ' + val2.used_perc + '%</span>';
        output += '</span>';
        output += '<div style="clear:both"></div>';
        output += '</div>';
      });
      output += '</td>';
      output += '</tr>';
    });
    $('#tbody-update').html(output);
  });
</script>
{% endblock %}