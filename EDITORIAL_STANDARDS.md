# Editorial Standards

## Tone and voice

- Write for a professional infrastructure engineer, not a beginner-only
  audience. Assume comfort with the command line and general IT concepts;
  explain vendor- and domain-specific terms on first use.
- Prefer direct, active-voice instructions ("Configure the VLAN...") over
  passive phrasing.
- Avoid marketing language. Describe trade-offs honestly, including when a
  vendor feature has known limitations.

## Structure

- Every chapter uses the section order defined in
  [templates/chapter.md](templates/chapter.md).
- Use `##` for top-level chapter sections and `###` for subsections; never
  skip a heading level.
- Numbered lists are for sequential procedures; bulleted lists are for
  unordered facts or options.

## Technical accuracy

- Record the software/platform baseline a chapter was written against in
  [SOFTWARE_VERSIONS.md](SOFTWARE_VERSIONS.md); do not imply a command or UI
  path is timeless.
- Code and CLI examples must be complete enough to run as shown, with
  placeholders clearly marked (for example `<VLAN_ID>`).
- Do not reproduce proprietary certification exam questions or licensed
  vendor courseware; describe blueprint domains and point to the official
  source instead.

## Markdown conventions

- One `H1` per file, matching the file's title.
- Relative links for anything inside the repository.
- Fenced code blocks with a language hint (`bash`, `yaml`, `text`).
- Tables for structured reference data (ports, version baselines, comparison
  matrices) rather than nested bullet lists.

## Accessibility

- Provide meaningful alt text for every image and diagram.
- Do not encode information in color alone in diagrams; pair color with a
  label or pattern.
