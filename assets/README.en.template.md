<div align="center">

<img src="docs/assets/readme/brand-mark.svg" alt="{{PROJECT_NAME}} brand mark" width="112">

<h1>{{PROJECT_NAME}}</h1>

<p><strong>{{ONE_LINE_VALUE}}</strong></p>

<p>{{TARGET_USERS}} · {{PRIMARY_USE_CASE}}</p>

<p>
  <img src="docs/assets/readme/badges/status.svg" alt="Project status: {{STATUS}}">
  <a href="README.md"><img src="docs/assets/readme/badges/language.svg" alt="Documentation languages: Chinese and English"></a>
  <a href="SECURITY.md"><img src="docs/assets/readme/badges/security.svg" alt="Security policy: read the security guide"></a>
  <a href="LICENSE"><img src="docs/assets/readme/badges/license.svg" alt="License: {{LICENSE}}"></a>
</p>

<p>
  <a href="#1-project-value">Project value</a> ·
  <a href="#3-quick-start">Quick start</a> ·
  <a href="#4-usage-example">Example</a> ·
  <a href="#5-system-architecture">Architecture</a> ·
  <a href="#6-validation-status">Validation</a> ·
  <a href="#10-support-and-contributing">Contributing</a>
</p>

<p><a href="README.md">简体中文</a> · <a href="README.en.md">English</a></p>

</div>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/readme/hero-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/readme/hero-light.png">
  <img src="docs/assets/readme/hero-light.png" alt="{{PROJECT_INTERFACE_TERMINAL_BEHAVIOR_OR_RUNTIME_RELATIONSHIP}}" width="100%">
</picture>

<div align="center">

Figure 1. {{FACTUAL_HERO_CAPTION}}

</div>

## 1 Project value

{{PROJECT_NAME}} helps {{TARGET_USERS}} complete {{PRIMARY_TASK}} and obtain {{OBSERVABLE_RESULT}}

### 1.1 Choose a path

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>Understand the project</h3>
      <p>{{HOW_TO_USE_THE_HERO_OR_CAPABILITY_MATRIX}}</p>
    </td>
    <td width="33%" valign="top">
      <h3>Validate locally</h3>
      <p>{{HOW_TO_COMPLETE_THE_FIRST_SAFE_RUN}}</p>
    </td>
    <td width="33%" valign="top">
      <h3>Prepare integration</h3>
      <p>{{HOW_TO_REVIEW_ARCHITECTURE_SECURITY_OR_API_BOUNDARIES}}</p>
    </td>
  </tr>
</table>

## 2 Core capabilities

<div align="center">

Table 2.1. {{PROJECT_NAME}} core capabilities

| Capability | Observable result | Current status |
|---|---|---|
| {{CAPABILITY_ONE}} | {{OBSERVABLE_RESULT}} | {{EVIDENCE_BACKED_STATUS}} |
| {{CAPABILITY_TWO}} | {{OBSERVABLE_RESULT}} | {{EVIDENCE_BACKED_STATUS}} |
| {{CAPABILITY_THREE}} | {{OBSERVABLE_RESULT}} | {{EVIDENCE_BACKED_STATUS}} |

</div>

## 3 Quick start

Prerequisites: {{RUNTIME_PLATFORM_OR_PERMISSION_REQUIREMENTS}}

```bash
git clone https://github.com/example-org/example-repo.git # Clone the repository through a placeholder organization
cd example-repo # Enter the repository before running project commands
npm install # Install the dependency versions selected by the lockfile
npm run dev # Start the local development environment and inspect its terminal output
```

Expected result: {{OBSERVABLE_INTERFACE_FILE_OR_TERMINAL_OUTPUT}}

## 4 Usage example

{{DESCRIBE_THE_CORE_FLOW_WITH_REAL_SANITIZED_INPUT_ACTION_AND_OUTPUT}}

## 5 System architecture

The following flow shows how {{PRIMARY_INPUT}} passes through {{CORE_COMPONENTS}} and produces {{FINAL_OUTPUT}}

<div align="center">

```mermaid
%% Show the core data direction and trust boundary with plain labels
flowchart TD
    A[{{PRIMARY_INPUT}}] --> B[{{LOCAL_PROCESSING}}]
    B --> C[{{CORE_CAPABILITY}}]
    C --> D[{{HUMAN_CONFIRMATION_OR_SAFETY_GATE}}]
    D --> E[{{OBSERVABLE_OUTPUT}}]
```

Figure 5.1. {{PROJECT_NAME}} core runtime relationship

</div>

### 5.1 Interface evidence (conditional)

Keep this module only when the repository has a real user interface and screenshots can be regenerated with synthetic data

<table>
  <tr>
    <td width="50%"><img src="docs/assets/readme/ui/{{START_SCREEN_FILE}}" alt="{{START_STATE_PRIMARY_ACTION_AND_OBSERVABLE_TARGET}}" width="100%"></td>
    <td width="50%"><img src="docs/assets/readme/ui/{{RESULT_SCREEN_FILE}}" alt="{{RESULT_STATE_FEEDBACK_AND_NEXT_STEP}}" width="100%"></td>
  </tr>
  <tr>
    <td align="center">Figure 5.2. {{FACTUAL_START_STATE_CAPTION}}</td>
    <td align="center">Figure 5.3. {{FACTUAL_RESULT_STATE_CAPTION}}</td>
  </tr>
</table>

### 5.2 Scientific result (conditional)

Keep this module only when the data, statistical definition, and reproduction entry point can be published

<div align="center">

![{{METRIC_COMPARISON_AND_MAIN_CONCLUSION}}](docs/assets/readme/plots/{{FIGURE_FILE}})

Figure 5.4. x-axis: {{NAME_AND_UNIT}}; y-axis: {{NAME_AND_UNIT}}; sample size: {{COUNT}}; error: {{DEFINITION}}; updated {{DATE}}

</div>

Data: [`{{DATA_FILE}}`]({{DATA_RELATIVE_PATH}}) · Reproduce: `{{REPRODUCTION_COMMAND}}` · Limitation: {{CONCLUSION_NOT_SUPPORTED_BY_THE_FIGURE}}

### 5.3 Visual stability (keep when visuals exist)

| Scenario | Validation target | Current result | Evidence boundary |
|---|---|---|---|
| GitHub light | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| GitHub dark | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| Narrow viewport | {{TARGET}} | {{RESULT}} | {{SCOPE}} |
| Image failure | Alt text, caption, and body | {{RESULT}} | {{SCOPE}} |

## 6 Validation status

The following results come from {{CHECK_COMMAND_CI_RECORD_OR_RELEASE_EVIDENCE}}

<div align="center">

Table 6.1. {{PROJECT_NAME}} validation scope

| Check target | Validation method | Result | Evidence boundary |
|---|---|---|---|
| {{TARGET_ONE}} | `{{COMMAND_OR_RECORD}}` | {{RESULT}} | {{COVERAGE}} |
| {{TARGET_TWO}} | `{{COMMAND_OR_RECORD}}` | {{RESULT}} | {{COVERAGE}} |

</div>

## 7 Data security

- {{DATA_SAVED_BY_THE_PROJECT_AND_STORAGE_LOCATION}}
- {{EXTERNAL_SERVICE_ENABLEMENT_AND_LEAST_PRIVILEGE}}
- {{SANITIZATION_RULES_FOR_LOGS_SCREENSHOTS_AND_EXPORTS}}
- {{CHECK_RESULT_FOR_PIXELS_SVG_SOURCE_FILE_METADATA_AND_REMOTE_VISUAL_REQUESTS}}
- Report vulnerabilities through the private channel in [SECURITY.md](SECURITY.md)

## 8 Project status

Project status: {{RELEASED_EXPERIMENTAL_MAINTAINED_OR_ARCHIVED}}

Supported scope: {{VERSIONS_PLATFORMS_AND_CAPABILITIES_BACKED_BY_EVIDENCE}}

## 9 Limitations

- {{UNSUPPORTED_USE_CASE}}
- {{UNVERIFIED_PLATFORM_OR_ENVIRONMENT}}
- {{DEPLOYMENT_OR_DATA_RESPONSIBILITY_RETAINED_BY_THE_USER}}

## 10 Support and contributing

- Usage questions: {{DISCUSSION_OR_DOCUMENTATION_ENTRY}}
- Reproducible defects: {{ISSUE_TRACKER_ENTRY}}
- Security reports: [SECURITY.md](SECURITY.md)
- Contribution workflow: [CONTRIBUTING.md](CONTRIBUTING.md)
- License terms: [LICENSE](LICENSE)

## 11 Project pulse (conditional and always last)

Project pulse supplements current maintenance and community state. It cannot replace functional, performance, quality, or security evidence

| Metric | Current status | Source and update time | Fallback |
|---|---|---|---|
| Current release | {{STATUS}} | {{SOURCE_AND_DATE}} | Releases page |
| Build | {{STATUS}} | {{SOURCE_AND_DATE}} | Validation guide |
| Community trend | {{STATUS_OR_REMOVE_THIS_ROW}} | {{PROVIDER_QUERY_SCOPE_AND_DATE}} | Native repository page |
