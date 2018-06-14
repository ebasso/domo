{% extends "layout.html" %}
{% block content %}
<div class="row">
  <div class="col-lg-12">
    <h1 class="page-header">Traveler - {{now}}</h1>
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
            {% endif %}" style="width:{{bar_pixel * 3}}px"></div>
          </div>
          <span style="float:left; font-size:28px">&nbsp;&nbsp;
            <span style="font-size: 75%;color: #777">({{ environment_used_total_human }} / {{ environment_size_total_human }}) - {{ environment_used_total_perc_human
              }}%
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
            <a href="report-traveler.csv">report-traveler.csv</a>
          </li>
          <li>
            <a href="report-traveler.txt">report-traveler.txt</a>
          </li>
          <li>
            <a href="report-traveler.json">report-traveler.json</a>
          </li>
          <li>
            <a href="report-traveler.sql">report-traveler.sql</a>
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
          <tbody>
            {% for server in servers %}
            <tr>
              <td>{{ server['name'] }}</td>
              <td>
                <div class='bar'>
                  <div class="progress" style="float:left; width:100px; height:16px; margin-bottom:1px;">
                    <div class={% if (server[ 'disks_used_total_perc']>= 89) %} "progress-bar progress-bar-danger" {% elif (server['disks_used_total_perc'] >= 75) %} "progress-bar progress-bar-warning" {% else %} "progress-bar progress-bar-success" {% endif %} style="width:{{ server['disks_used_total_perc_human']
                      }}px">
                    </div>
                  </div>
                  <span style="float:left; font-size:12px">&nbsp;&nbsp;Total
                    <span style="font-size: 75%;color: #777">({{ server['disks_used_total_human'] }} / {{ server['disks_size_total_human'] }}) - {{ server['disks_used_total_perc_human']
                      }}%
                    </span>
                  </span>
                  <div style="clear:both"></div>
                </div>
              </td>
              <td>
                {% for disk in server['disks'] %} {% set dangerBar,warningBar = 89,75 %} {% if disk['label'].find('logdir') != -1 %} {% set dangerBar,warningBar = 50,45 %} {% endif %}
                <div class='bar'>
                  <div class="progress" style="float:left; width:100px; height:16px; margin-bottom:1px;">
                    <div class={% if (disk[ 'used_perc']>= dangerBar) %} "progress-bar progress-bar-danger" {% elif (disk['used_perc'] >= warningBar) %} "progress-bar progress-bar-warning" {% else %} "progress-bar progress-bar-success" {% endif %} style="width:{{ disk['used_perc_human']
                      }}px">
                    </div>
                  </div>
                  <span style="float:left; font-size:12px">&nbsp;&nbsp;{{ disk['label'] }}
                    <span style="font-size: 75%;color: #777">({{ disk['used_human'] }} / {{ disk['size_human'] }}) - {{ disk['used_perc_human'] }}%</span>
                  </span>
                  <div style="clear:both"></div>
                </div>
                {% endfor %}
              </td>
            </tr>
            {% endfor %}
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
