locals {
  query_files = fileset(path.module, "detections/**/*.yml")
  queries = {
    for file in local.query_files :
    basename(file) => yamldecode(file(file))
  }
}

resource "splunk_saved_searches" "alerts" {
  for_each = local.queries

  name           = each.value.name
  search         = each.value.search
  description    = each.value.description
  cron_schedule  = each.value.schedule
  actions        = "email"
  action_email   = jsonencode({
    to = each.value.alert_recipients
  })
  is_scheduled   = true
}