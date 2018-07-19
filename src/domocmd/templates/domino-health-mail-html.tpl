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
              <td>Mail.MailBoxes.AccessConflicts</td>
              <td>< 2</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td>Mail.Waiting</td>
              <td>= 0</td>
              <td><= 20</td>
              <td><= 100</td>
              <td>> 100</td>
            </tr>
            <tr>
              <td>Mail.Dead</td>
              <td>= 0</td>
              <td><= 20</td>
              <td><= 100</td>
              <td>> 100</td>
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
            <a href="domino-health-mail.json">domino-health-mail.json</a>
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
              <th class="rotate-45"><div><span>Mail.MailBoxes.AccessConflicts</span></div></th>
              <th>&nbsp;</th>
              <th class="rotate-45"><div><span>Mail.Waiting</span></div></th>
              <th class="rotate-45"><div><span>Mail.Dead</span></div></th>
              <th>&nbsp;</th>
            </tr>
          </thead>
          <tbody id="domo-tbody-update">
            <tr>
              <td>ServerName</td>
              <td><i class="fa fa-check-circle text-success" data-toggle="tooltip" data-placement="top" title="Server.Trans.PerMinute: 677.0 [Good]"></i></td>
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
  $.getJSON('domino-health-mail.json', function (data) {
    console.log(data);
    $('#domo-page-title').html(data.title + ' - ' + data.now);

    var output = '';
    $.each(data.servers, function (key, val) {
      console.log(val);
      output += '<tr><td>' + val.name + '</td>';
      //_status_mailboxes
      output += '<td>' + renderStat("Mail.Mailbox.AccessConflicts",val.statistics) + '</td>';
      output += '<td>&nbsp;</td>';
      output += '<td>' + renderStat("Mail.Waiting",val.statistics) + '</td>';
      output += '<td>' + renderStat("Mail.Dead",val.statistics) + '</td>';
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