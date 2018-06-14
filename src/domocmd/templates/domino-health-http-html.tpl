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
            <a href="domino-health-http.json">domino-health-http.json</a>
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
              <th class="rotate-45"><div><span>Domino.Cache.Design.HitRate</span></div></th>
              <th class="rotate-45"><div><span>Domino.Cache.Design.DisplaceRate</span></div></th>
              <th class="rotate-45"><div><span>Domino.Cache.UserCache.HitRate</span></div></th>
              <th class="rotate-45"><div><span>Domino.Cache.UserCache.DisplaceRate</span></div></th>
              <th class="rotate-45"><div><span>NET.GroupCache.status</span></div></th>
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
{% endblock %} {% block body_javascript %}
<script>
  $.getJSON('domino-health-http.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      //_status_domino_cache_design
      output += '<td>' + renderStat("Domino.Cache.Design.HitRate",val.statistics) + '</td>';
      output += '<td>' + renderStat("Domino.Cache.Design.DisplaceRate",val.statistics) + '</td>';
      //_status_domino_cache_usercache
      output += '<td>' + renderStat("Domino.Cache.User Cache.HitRate",val.statistics) + '</td>';
      output += '<td>' + renderStat("Domino.Cache.User Cache.DisplaceRate",val.statistics) + '</td>';
      output += '<td>' + renderStat("NET.GroupCache",val.statistics) + '</td>';
      output += '<td>.</td>';
      output += '</tr>';
    });
    $('#domo-tbody-update').html(output);
  });

  
</script>
{% endblock %}