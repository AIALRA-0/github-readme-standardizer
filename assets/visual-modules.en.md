# Optional README modules in English

Copy only evidence-backed modules, replace every placeholder, and keep numbering aligned with the Chinese modules

## A Hero visual

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/readme/hero-light.svg">
  <img src="docs/assets/readme/hero-light.svg" alt="{{OBJECT_RELATIONSHIP_AND_CONCLUSION_SHOWN_BY_THE_HERO}}" width="100%">
</picture>

<div align="center">Figure A.1. {{FACTUAL_CAPTION_WITHOUT_UNVERIFIED_PROMOTION}}</div>

## B Scientific result

<div align="center">

![{{METRIC_COMPARISON_AND_MAIN_CONCLUSION}}](docs/assets/readme/plots/{{FIGURE_FILE}})

Figure B.1. {{METRIC}}; x-axis: {{NAME_AND_UNIT}}; y-axis: {{NAME_AND_UNIT}}; sample size: {{COUNT}}; error: {{DEFINITION}}; updated {{DATE}}

</div>

Data: [`{{DATA_FILE}}`]({{DATA_RELATIVE_PATH}}) · Reproduce: `{{REPRODUCTION_COMMAND}}` · Limitation: {{CONCLUSION_NOT_SUPPORTED_BY_THIS_FIGURE}}

## C Interface gallery

<table>
  <tr>
    <td width="50%"><img src="docs/assets/readme/ui/{{SCREEN_ONE}}" alt="{{STARTING_STATE_AND_PRIMARY_ACTION}}" width="100%"></td>
    <td width="50%"><img src="docs/assets/readme/ui/{{SCREEN_TWO}}" alt="{{RESULT_STATE_AND_OBSERVABLE_FEEDBACK}}" width="100%"></td>
  </tr>
  <tr>
    <td align="center">Figure C.1. {{START_STATE_CAPTION}}</td>
    <td align="center">Figure C.2. {{RESULT_STATE_CAPTION}}</td>
  </tr>
</table>

## D Interface stability

| Scenario | Validation target | Current result | Evidence boundary |
|---|---|---|---|
| GitHub light | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| GitHub dark | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| Narrow viewport | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| Image failure | Alt text, caption, and body | {{RESULT}} | {{SCOPE}} |

## E Visual privacy

> [!IMPORTANT]
> Visuals on this page use synthetic data. Pixels, SVG source, image metadata, and external requests were checked before publication. {{REMAINING_EVIDENCE_BOUNDARY}}

## F Project pulse

Project pulse belongs at the end of the document and cannot replace functional, performance, or security evidence

| Metric | Current status | Source and update time | Fallback |
|---|---|---|---|
| Current release | {{STATUS}} | {{SOURCE_AND_DATE}} | Releases page |
| Build | {{STATUS}} | {{SOURCE_AND_DATE}} | Validation guide |
| Community trend | {{STATUS_OR_REMOVE_THIS_ROW}} | {{PROVIDER_SCOPE_AND_DATE}} | Native repository page |
