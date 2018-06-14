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
            <a href="traveler-statistics.json">traveler-statistics.json</a>
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
        <table width="100%" class="table">
          <thead id="domo-thead-update">
            <tr>
              <th>Server</th>
              <th>Status</th>
              <th>Availability Index</th>
              <th>Numero de Usuarios</th>
              <th>Numero de Devices</th>
            </tr>
          </thead>
          <tbody id="domo-tbody-update">
            <tr>
              <td>ServerName</td>
              <td>Yellow</td>
              <td>97</td>
              <td>35</td>
              <td>78</td>
            </tr>
            <tr>
              <td>ServerName2</td>
              <td>Green</td>
              <td>100</td>
              <td>130</td>
              <td>280</td>
            </tr>
            <tr>
              <td>ServerName3</td>
              <td>Yellow</td>
              <td>75</td>
              <td>430</td>
              <td>765</td>
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
  $.getJSON('traveler-statistics.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      output += '<td>' + toBootstrap(val.status) + '</td>';
      output += '<td>' + val.ai + '</td>';
      output += '<td>' + val.user + '</td>';
      output += '<td>' + val.devices + '</td>';
      output += '</tr>';
    });
    $('#domo-tbody-update').html(output);
  });

  $(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });

  function toBootstrap(status) {

    if (status == 'Green') {
      return '<span class="label label-success">Green</span>';
    }
    if (status == 'Yellow') {
      return '<span class="label label-warning">Yellow</span>';
    }
    if (status == 'Red'){
    return '<span class="label label-danger">Red</span>';
    }
    return '';
  }
  
  
</script>
{% endblock %}