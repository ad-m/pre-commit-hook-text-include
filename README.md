# Text include for pre-commit git hooks

Text include for [pre-commit](http://pre-commit.com).

This hook validates includes of content of another file in text files.

<!--TOC-->

- [How-to](#how-to)
  - [Configure pre-commit](#configure-pre-commit)
  - [Invoke pre-commit](#invoke-pre-commit)
    - [On every commit](#on-every-commit)
    - [On demand](#on-demand)
- [License](#license)

<!--TOC-->

## How-to

### Configure pre-commit

Add to `.pre-commit-config.yaml` in your git repo:

<!-- [START text-include file='./examples/.pre-commit-config.yaml' pre='```yaml' post='```'] -->
```yaml
  - repo: https://github.com/ad-m/pre-commit-hook-text-include
    rev: 0.0.1  # or specific tag
    hooks:
        - id: text-include
```
<!-- [END text-include] -->

Specify in included file section by adding marker:

- start section marker: `[START my-section]`
- end section marker: `[END my-section]`

Use that section by adding marker:

- start section marker eg.: `[START my-section file='./examples/.pre-commit-config.yaml' pre='```yaml' post='```']`
- end section marker: `[START my-section]`

Replace `my-section` with any custom section name.

:bulb: If a pre-commit hook changes a file,
the hook fails with a warning that files were changed.

## Supported parameter

| Name | Required | Comment |
| ---- | --- | ---- |
| `file` | Yes | File of source of section |
| `pre` | No | Line to add before included section eg. mark as code|
| `post` | No | Line to add after included section eg. end mark as code |

### Invoke pre-commit

#### On every commit

If you want to invoke the checks as a git pre-commit hook, run:

```bash
# Run on every commit.
pre-commit install
```

#### On demand

If you want to run the checks on-demand (outside of git hooks), run:

```bash
# Run on-demand.
pre-commit run --all-files
```

## License

The code in this repo is licensed under the [MIT License](LICENSE).
