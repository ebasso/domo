{% extends "layout.html" %}
{% block content %}
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
              <td>Replica.Cluster.SecondsOnQueue</td>
              <td><= 10</td>
              <td><= 15</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td>Replica.Cluster.SecondsOnQueue.Avg</td>
              <td><= 10</td>
              <td><= 15</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td>Replica.Cluster.WorkQueueDepth</td>
              <td><= 10</td>
              <td><= 15</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td>Replica.Cluster.WorkQueueDepth.Avg</td>
              <td><= 10</td>
              <td><= 15</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
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
            <a href="domino-health-cluster.json">domino-health-cluster.json</a>
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
              <th class="rotate-45"><div><span>Replica.Cluster.SecondsOnQueue</span></div></th>
              <th class="rotate-45"><div><span>Replica.Cluster.SecondsOnQueue.Avg</span></div></th>
              <th class="rotate-45"><div><span>Replica.Cluster.WorkQueueDepth</span></div></th>
              <th class="rotate-45"><div><span>Replica.Cluster.WorkQueueDepth.Avg</span></div></th>
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody id="domo-tbody-update">
            <tr>
              <td>ServerName</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
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
{% endblock %} 
{% block body_javascript %}
<script>
  $.getJSON('domino-health-cluster.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      //_status_replica_cluster
      output += '<td>' + renderStat("Replica.Cluster.SecondsOnQueue",val.statistics) + '</td>';
      output += '<td>' + renderStat("Replica.Cluster.SecondsOnQueue.Avg",val.statistics) + '</td>';
      output += '<td>' + renderStat("Replica.Cluster.WorkQueueDepth",val.statistics) + '</td>';
      output += '<td>' + renderStat("Replica.Cluster.WorkQueueDepth.Avg",val.statistics) + '</td>';      
      output += '<td>.</td>';
      output += '</tr>';
    });
    $('#domo-tbody-update').html(output);
  });

  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
</script>
{% endblock %}