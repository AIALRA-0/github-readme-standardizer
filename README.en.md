<h1 align="center">github-readme-standardizer</h1>

Help every project explain its purpose and give first-time visitors a clear starting point

[Chinese guide](README.md) · [Get started](#2-get-started) · [Choose a template](references/adaptive-template.md) · [Choose a hero](references/hero-playbook.md)

![Three documents share headers and body structure, with blue, green and violet modules showing different content arrangements](docs/assets/readme/hero.svg)

Figure 1.1. Three content arrangements share one document structure

Read from left to right: headers and body shapes stay consistent while modules represent a visual overview, grouped capabilities and a content list.
This is a structural illustration. It explains adaptable composition and does not establish software behavior or successful checks.

## 1. Suitable tasks

A skill is a reusable set of instructions and supporting files that an assistant reads for a task. This skill helps maintainers organize landing pages consistently while retaining project-specific content. It does not run automatically or grant publication permission.

- Audit existing pages for broken entry points and unsupported claims
- Write a Chinese page and synchronize its facts with English
- Choose a first-use path based on the primary deliverable
- Select or create a useful hero image
- Check local files and page usability across display conditions

Chinese writing follows the complete current rules of the installed `human-readable-technical-writing` skill.
This repository maintains composition and visual choices without duplicating those writing rules.

## 2. Get started

Use an assistant that can read local skills, with `human-readable-technical-writing` already installed.
Confirm it can discover this repository's `SKILL.md`.

1. Make this repository available as a local skill, using the [skill entry point](SKILL.md).
2. Identify the target repository and specify a read-only audit or an edit.
3. Use the following example request.

```text
Use $github-readme-standardizer to audit the current repository.
Apply the complete latest rules of the installed $human-readable-technical-writing.
Only report problems with structure, first-use steps and the hero image, citing repository files.
```

This is a request to the assistant, not a terminal command.
The expected result is an evidence-backed report; this example does not request edits or publication.

To request changes, replace “Only report” with “Fix confirmed problems and synchronize both landing pages.”
For publication, name the repository and allowed operations separately and use `github-safe-publish`.

## 3. Consistent and adaptable structure

Every landing page answers purpose, first use, further use, status and limitations, and help and licensing.
A small tool may combine its example with first use; a course may replace installation with a reading entry point.

- [Chinese template](assets/README.zh.template.md): compact structure without assumed installation tools
- [English template](assets/README.en.template.md): matching information positions
- [Composition guide](references/adaptive-template.md): project-specific choices and a complete course example
- [Project profiles](references/profile-routing.md): ordering based on the primary deliverable
- [Optional modules](references/module-catalog.md): interface, measurement and component evidence
- [Chinese writing integration](references/writing-integration.md): first-use definitions and local review

Replace placeholders and remove optional content without supporting evidence.
Preserve existing licenses, citations and third-party attribution.

## 4. Choose a hero image

Decide what the image helps readers judge before choosing its production method.

- Use sanitized screenshots for representative real interfaces
- Show output from actual synthetic inputs when command behavior is central
- Draw editable diagrams for content or component relationships
- Generate illustrations for brand expression and label their role
- Omit the hero when it does not improve understanding

This repository uses a text-free structural illustration to avoid tiny mobile labels and share one asset between languages.

- [Hero playbook](references/hero-playbook.md): selection order and production brief
- [Production guide](references/visual-production.md): sources and local delivery
- [Privacy review](references/visual-privacy.md): visible and embedded information
- [Asset notes](docs/assets/readme/hero-notes.md): role and design basis

## 5. Check the result

Python runs the local documentation checks. The auditor reads files and reports findings without modifying the source; it cannot replace factual review or visual inspection.

Use Python 3.10 or newer and run this command from the repository root.

```powershell
# Check this repository's bilingual pages and their referenced files
python -X utf8 scripts/audit_readme.py .
```

- `PASS` means no hard errors were detected; review warnings and content separately
- For `FAIL`, inspect locations in `errors`, repair affected content and check again
- Chinese writing also requires the installed writing skill's review; the auditor cannot establish explanatory completeness
- Preview light, dark, desktop and narrow displays using the [validation guide](references/validation.md)

Test counts are not embedded in the landing page; consult the current [check history](https://github.com/AIALRA-0/github-readme-standardizer/actions).

## 6. Limitations and maintenance

- Automated checks cover implemented rules and cannot establish every fact, image right or reader's understanding
- Generated images cannot replace real interfaces or measurements
- Publication must follow target protection rules and user authorization
- No license file is included; public visibility does not establish permission to copy, modify or redistribute
- Report ordinary problems through [issues](https://github.com/AIALRA-0/github-readme-standardizer/issues)
- Follow the [contribution guide](CONTRIBUTING.md) for changes
- Follow the [security guide](SECURITY.md) for sensitive reports and keep secrets out of public records
- Sources and limits are recorded in the [research basis](references/research-basis.md)
