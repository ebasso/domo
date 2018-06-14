{% extends "layout.html" %} 
{% block head_css_extra %}
  <!-- DataTables CSS -->
  <link href="../vendor/datatables-plugins/dataTables.bootstrap.css" rel="stylesheet">

  <!-- DataTables Responsive CSS -->
  <link href="../vendor/datatables-responsive/dataTables.responsive.css" rel="stylesheet">
 {% endblock %} 
{% block content %}
<div class="row">
  <div class="col-lg-12">
    <h1 class="page-header">Disk Report - {{now}}</h1>
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
        <table width="100%" class="table" id="dataTables-example">
          <thead>
            <tr>
              <th>Server</th>
              <th>Used</th>
              <th>Total</th>
              <th>Percentage</th>
              <th>Other</th>
            </tr>
          </thead>
          <tbody>
            {% for server in servers %}
            <tr>
              <td>{{ server['name'] }}</td>
              <td>{{ server['disks_used_total_human'] }}</td>
              <td>{{ server['disks_size_total_human'] }}</td>
              <td>{{ server['disks_used_total_perc'] }}%</td>
              <td>
                <div class='bar'>
                  <div class="progress" style="float:left; width:100px; height:16px; ">
                    <div class="{% if (server['disks_used_total_perc'] >= 90) %}
                            progress-bar progress-bar-danger
                            {% elif (server['disks_used_total_perc'] >= 75) %}
                            progress-bar progress-bar-warning
                            {% else %}
                            progress-bar progress-bar-success
                            {% endif %}" style="width:{{server['disks_used_total_perc']}}px"></div>
                  </div>
                  <div style="clear:both"></div>
                </div>
              </td>
            </tr>
            {% endfor %}
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

<!-- DataTables JavaScript -->
<script src="../vendor/datatables/js/jquery.dataTables.min.js"></script>
<script src="../vendor/datatables-plugins/dataTables.bootstrap.min.js"></script>
<script src="../vendor/datatables-responsive/dataTables.responsive.js"></script>

<!-- Page-Level Demo Scripts - Tables - Use for reference -->
<script>
  $(document).ready(function () {
    $('#dataTables-example').DataTable({
      responsive: true
    });
  });
</script>
{% endblock %}