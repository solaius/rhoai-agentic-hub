"""The triage report: a self-contained HTML page with per-row decisions and an
Export Decisions button.

This report renders authenticated Jira text (summaries, statuses), so it is
written under restricted/ ONLY and never into the tracked tree (spec decision
4: this repo is PUBLIC and Jira serves nothing anonymously).

The exported JSON is a PROPOSAL. It is not applied until the inline gate in
hub.jira-triage approves it line by line (spec decision 7).
"""
import html
import json

from . import triage

SECTIONS = (
    ("Untriaged", "needs_attention"),
    ("Waiting on Input", "waiting"),
    ("Backlogged", "backlogged"),
)

CSS = """
:root { color-scheme: light dark; }
body { font: 14px/1.5 system-ui, sans-serif; margin: 0; padding: 2rem;
       background: #fbfbfd; color: #1a1a1a; }
h1 { font-size: 1.4rem; margin: 0 0 .25rem; }
.scope { color: #666; font-size: .8rem; margin-bottom: 1.5rem;
         font-family: ui-monospace, monospace; word-break: break-all; }
.tiles { display: flex; gap: .75rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.tile { background: #fff; border: 1px solid #e3e3e8; border-radius: 8px;
        padding: .6rem 1rem; min-width: 5rem; }
.tile b { display: block; font-size: 1.5rem; }
.tile span { color: #666; font-size: .75rem; }
h2 { font-size: 1rem; margin: 1.75rem 0 .5rem; }
table { width: 100%; border-collapse: collapse; background: #fff;
        border: 1px solid #e3e3e8; border-radius: 8px; overflow: hidden; }
th, td { text-align: left; padding: .5rem .6rem; border-bottom: 1px solid #f0f0f3;
         vertical-align: top; }
th { background: #f6f6f8; font-size: .75rem; text-transform: uppercase;
     letter-spacing: .04em; color: #555; }
tr:last-child td { border-bottom: none; }
.key { font-family: ui-monospace, monospace; white-space: nowrap; }
.flag { display: inline-block; background: #fdecea; color: #a32; font-size: .7rem;
        padding: .1rem .35rem; border-radius: 4px; margin-right: .25rem; }
.why { color: #666; font-size: .75rem; }
.blocked { color: #a32; font-size: .72rem; }
.bar { position: sticky; top: 0; background: #fbfbfdee; padding: .75rem 0;
       backdrop-filter: blur(6px); display: flex; gap: .75rem; align-items: center;
       border-bottom: 1px solid #e3e3e8; margin-bottom: 1rem; z-index: 2; }
button { font: inherit; padding: .4rem .9rem; border-radius: 6px;
         border: 1px solid #c9c9d0; background: #fff; cursor: pointer; }
button.primary { background: #06c; color: #fff; border-color: #06c; }
#count { color: #666; font-size: .8rem; }
@media (prefers-color-scheme: dark) {
  body { background: #16161a; color: #e8e8ea; }
  .tile, table { background: #1e1e23; border-color: #33333a; }
  th { background: #26262c; color: #aaa; }
  td { border-color: #2a2a30; }
  .bar { background: #16161aee; border-color: #33333a; }
  button { background: #26262c; color: #e8e8ea; border-color: #3a3a42; }
}
"""

JS = """
function decisions() {
  const out = {};
  document.querySelectorAll('tr[data-key]').forEach(tr => {
    const sel = tr.querySelector('select');
    if (!sel || !sel.value) return;
    const rel = tr.querySelector('.release');
    const com = tr.querySelector('.commenttext');
    out[tr.dataset.key] = {
      action: sel.value,
      release: rel && rel.value ? rel.value.trim() : null,
      comment: com && com.value ? com.value.trim() : null,
      current_labels: JSON.parse(tr.querySelector('.labels-data').textContent || '[]')
    };
  });
  return out;
}
function refresh() {
  const n = Object.keys(decisions()).length;
  document.getElementById('count').textContent = n + ' decision(s) staged';
}
document.addEventListener('change', e => {
  if (e.target.tagName === 'SELECT') {
    const tr = e.target.closest('tr');
    const rel = tr.querySelector('.release');
    if (rel) rel.style.display = e.target.value === 'roadmap' ? '' : 'none';
    const com = tr.querySelector('.commenttext');
    if (com) com.style.display =
      (e.target.value === 'comment' || e.target.value === 'close') ? '' : 'none';
  }
  refresh();
});
function exportDecisions() {
  const payload = {
    exported_at: document.body.dataset.today,
    feature: document.body.dataset.feature,
    decisions: decisions()
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)],
                        {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'triage-decisions-' + payload.exported_at + '.json';
  a.click();
}
document.addEventListener('DOMContentLoaded', refresh);
"""


def _esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def _options(row):
    """The action menu for one row. close and approve appear only when the
    workflow actually offers the transition (spec decision 3), so the human
    cannot stage a decision that the gate will only reject later."""
    opts = ['<option value="">-- decide --</option>']
    for action in ("roadmap", "backlog", "needs-uxd", "clarify", "comment"):
        opts.append(f'<option value="{action}">{action}</option>')
    blocked = []
    for action in triage.TRANSITION_ACTIONS:
        transition, reason = triage.resolve_transition(
            action, row.get("transitions") or [])
        if transition is not None:
            opts.append(f'<option value="{action}">{action} '
                        f'({_esc(transition.get("to") or transition.get("name"))})'
                        f'</option>')
        else:
            blocked.append(f"{action}: {reason}")
    opts.append('<option value="skip">skip</option>')
    return "\n".join(opts), blocked


def _section_of(row):
    if row.get("classification") == "backlogged":
        return "Backlogged"
    if row.get("status") in ("Stakeholder Review", "Pending Approval"):
        return "Waiting on Input"
    return "Untriaged"


def _row_html(row, base_url):
    options, blocked = _options(row)
    flags = "".join(f'<span class="flag">{_esc(f)}</span>'
                    for f in row.get("flags") or [])
    suggestion = (row.get("suggestion") or {})
    # Advisory only: this hidden cell round-trips the scan-time labels into
    # the exported JSON so the gate can check "label already present, skip
    # it". It must never be used to build a Jira write payload (label writes
    # are atomic adds via JiraClient.add_label; see triage.plan_decisions).
    labels_json = _esc(json.dumps(row.get("labels") or []))
    blocked_html = ("".join(f'<div class="blocked">{_esc(b)}</div>'
                            for b in blocked))
    return f"""
<tr data-key="{_esc(row['key'])}" data-suggestion="{_esc(suggestion.get('action'))}">
  <td class="key"><a href="{_esc(base_url)}/browse/{_esc(row['key'])}"
      target="_blank" rel="noopener">{_esc(row['key'])}</a></td>
  <td>{_esc(row.get('summary'))}<div>{flags}</div>{blocked_html}</td>
  <td>{_esc(row.get('status'))}</td>
  <td>{_esc(row.get('assignee') or '-')}</td>
  <td>{_esc(row.get('updated'))}</td>
  <td>
    <select>{options}</select>
    <input class="release" placeholder="3.6" style="display:none" size="5">
    <textarea class="commenttext" placeholder="comment" style="display:none"
              rows="2"></textarea>
    <div class="why">{_esc(suggestion.get('reason'))}</div>
    <span class="labels-data" hidden>{labels_json}</span>
  </td>
</tr>"""


def render(feature, jql, rows, today, base_url):
    """A complete, self-contained HTML document. No network, no repo writes."""
    buckets = {name: [] for name, _ in SECTIONS}
    for row in rows:
        buckets[_section_of(row)].append(row)

    tiles = "".join(
        f'<div class="tile"><b>{len(buckets[name])}</b><span>{_esc(name)}</span></div>'
        for name, _ in SECTIONS)
    tiles += (f'<div class="tile"><b>{len(rows)}</b><span>Total</span></div>')

    sections = []
    for name, _ in SECTIONS:
        section_rows = buckets[name]
        if not section_rows:
            continue
        body = "".join(_row_html(r, base_url) for r in section_rows)
        sections.append(f"""
<h2>{_esc(name)} ({len(section_rows)})</h2>
<table>
  <thead><tr><th>Key</th><th>Summary</th><th>Status</th><th>Assignee</th>
             <th>Updated</th><th>Decision</th></tr></thead>
  <tbody>{body}</tbody>
</table>""")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Triage: {_esc(feature)}</title>
<style>{CSS}</style>
</head>
<body data-feature="{_esc(feature)}" data-today="{_esc(today.isoformat())}">
<h1>RFE triage: {_esc(feature)}</h1>
<div class="scope">{_esc(jql)}</div>
<div class="bar">
  <button class="primary" onclick="exportDecisions()">Export Decisions</button>
  <span id="count">0 decision(s) staged</span>
</div>
<div class="tiles">{tiles}</div>
{''.join(sections)}
<script>{JS}</script>
</body>
</html>
"""
