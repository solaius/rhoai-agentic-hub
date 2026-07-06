# Canonical resource URIs

One canonical form per source system. `hub.file` normalizes on intake; the
linter format-checks `resource:` on `reference` entries (known domains must
match; unknown domains are a warning only).

| source | canonical form |
|---|---|
| Google Docs/Sheets/Slides | `https://docs.google.com/(document\|spreadsheets\|presentation)/d/<id>` — strip `/edit`, query params, fragments |
| Jira | `https://redhat.atlassian.net/browse/<KEY>` |
| Slack channel / thread | `https://redhat-internal.slack.com/archives/<CHANNEL>[/p<ts>]` |
| GitHub repo / file | `https://github.com/<org>/<repo>[/blob/<ref>/<path>]` |
