[scrapyd]
eggs_dir          = /var/lib/scrapyd/eggs
logs_dir          = /var/lib/scrapyd/logs
items_dir         = 
dbs_dir           = /var/lib/scrapyd/dbs
jobs_to_keep      = {{ SCRAPYD_KEEP_JOBS | default(5) }}
max_proc          = {{ SCRAPYD_MAX_PROC | default(0) }}
max_proc_per_cpu  = {{ SCRAPYD_MAX_PROC_PER_CPU | default(4) }}
finished_to_keep  = {{ SCRAPYD_KEEP_FINISHED | default(100) }}
poll_interval     = {{ SCRAPYD_POLL_INTERVAL | default(5) }}
bind_address      = {{ SCRAPYD_HOST | default('0.0.0.0') }}
http_port         = {{ SCRAPYD_PORT | default(6800) }}
debug             = off
runner            = scrapyd.runner
application       = scrapyd.app.application
launcher          = scrapyd.launcher.Launcher

[services]
schedule.json     = scrapyd.webservice.Schedule
cancel.json       = scrapyd.webservice.Cancel
addversion.json   = scrapyd.webservice.AddVersion
listprojects.json = scrapyd.webservice.ListProjects
listversions.json = scrapyd.webservice.ListVersions
listspiders.json  = scrapyd.webservice.ListSpiders
delproject.json   = scrapyd.webservice.DeleteProject
delversion.json   = scrapyd.webservice.DeleteVersion
listjobs.json     = scrapyd.webservice.ListJobs
daemonstatus.json = scrapyd.webservice.DaemonStatus
