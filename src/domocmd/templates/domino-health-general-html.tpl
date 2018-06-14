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
        <span style="font-size:28px">Servers #: &nbsp;&nbsp;
          <span style="font-size: 75%;color: #777">{{server_count}}</span>
        </span>
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
            <a href="domino-health-general.json">domino-health-general.json</a>
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
              <th style="width:140px">Elapsed.Time</th>
              <th class="rotate-45"><div><span>Server.AvailabilityIndex</span></div></th>
              <th class="rotate-45"><div><span>Server.Trans.PerMinute</span></div></th>
              <th class="rotate-45"><div><span>Server.ConcurrentTasks.Waiting</span></div></th>
              <th>&nbsp;</th>
              <th class="rotate-45"><div><span>Database.DB.BP.PCRIB</span></div></th>
              <th class="rotate-45"><div><span>Database.DbCache</span></div></th>
              <th class="rotate-45"><div><span>Database.DbCache.Over...</span></div></th>
              <th>&nbsp;</th>
              <th class="rotate-45"><div><span>Database.NAMELookupCache.1</span></div></th>
              <th class="rotate-45"><div><span>Database.NAMELookupCache.2</span></div></th>
              <th class="rotate-45"><div><span>Database.NAMELookupCache.3</span></div></th>
              <th>&nbsp;</th>
              <th class="rotate-45"><div><span>PF.PgFile.Total.PctUtil.Avg</span></div></th>
              <th class="rotate-45"><div><span>Update.PendingList</span></div></th>
            </tr>
          </thead>
          <tbody id="domo-tbody-update">
            <tr>
              <td>ServerName</td>
              <td>
                <i class="fa fa-check-circle text-success" title="Server.AvailabilityIndex: 63.0 [Good]"></i>
              </td>
              <td>
                <i class="fa fa-check-circle text-success" data-toggle="tooltip" data-placement="top" title="Server.Trans.PerMinute: 677.0 [Good]"></i>
              </td>
              <td>
                <i class="fa fa-check-circle text-success" data-toggle="tooltip" data-placement="top" title="Database.NAMELookupCache Database.NAMELookupCache - dnlcp_used= 71522336.0 , dnlcp_peak= 134217728.0 , hitrate=
                53.2882928848 [Good]"></i>
              </td>
              <td>
                <i class="fa fa-check-circle text-success" data-toggle="tooltip" data-placement="top" title="Domino.Cache.User Cache.HitRate: 17.6680984774 , maxsize= 8,192 [Bad"></i>
              </td>
              <td>
                <i class="fa fa-info-circle text-success" data-toggle="tooltip" data-placement="top" title="Database.NAMELookupCache Database.NAMELookupCache - dnlcp_used= 71522336.0 , dnlcp_peak= 134217728.0 , hitrate=
                53.2882928848 [Good]"></i>
              </td>
              <td>
                <i class="fa fa-question-circle text-primary" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
              </td>
              <td>
                <i class="fa fa-check-circle text-success" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
              </td>
              <td>
                <i class="fa fa-check-circle text-warning" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
              </td>
              <td>
                <i class="fa fa-times-circle text-danger" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
              </td>
              <td>
                <i class="fa fa-circle text-info" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
              </td>
              <td>
                <i class="fa fa-circle text-success" data-toggle="tooltip" data-placement="top" title="Tooltip on top"></i>
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
{% endblock %} {% block body_javascript %}
<script>
  $.getJSON('domino-health-general.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      output += '<td style="width:140px">' + val.statistics["Server.ElapsedTime"] + '</td>';
      //_status_server_performance
      output += '<td>' + renderStat("Server.AvailabilityIndex",val.statistics) + '</td>';
      output += '<td>' + renderStat("Server.Trans.PerMinute",val.statistics) + '</td>';
      output += '<td>' + renderStat("Server.ConcurrentTasks.Waiting",val.statistics) + '</td>';
      output += '<td>&nbsp;</td>';
      //_status_buffer_pool
      output += '<td>' + renderStat("Database.Database.BufferPool.PerCentReadsInBuffer",val.statistics) + '</td>';
      output += '<td>' + renderStat("Database.DbCache",val.statistics) + '</td>';
      output += '<td>' + renderStat("Database.DbCache.OvercrowdingRejections",val.statistics) + '</td>';
      output += '<td>&nbsp;</td>';
      //_status_database_namelookupcache
      output += '<td>' + renderStat("Database.NAMELookupCache.1",val.statistics) + '</td>';
      output += '<td>' + renderStat("Database.NAMELookupCache.2",val.statistics) + '</td>';
      output += '<td>' + renderStat("Database.NAMELookupCache.3",val.statistics) + '</td>';
      output += '<td>&nbsp;</td>';
      //_status_platform_pagingfile
      output += '<td>' + renderStat("Platform.PagingFile.Total.PctUtil.Avg",val.statistics) + '</td>';
      //_status_updall
      output += '<td>' + renderStat("Update.PendingList",val.statistics) + '</td>';
      output += '<td>.</td>';
      output += '</tr>';
    });
    $('#domo-tbody-update').html(output);
  });

  
</script>
{% endblock %}