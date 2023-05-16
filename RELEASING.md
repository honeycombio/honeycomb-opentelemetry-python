# Releasing

- Use `poetry version patch` to update the version number using `major`, `minor`, `patch`, or the prerelease variants `prepatch` or `prerelease`.
  For example, to bump from v1.1.1 to the next patch version:

```shell
> poetry version patch # 1.1.1 -> 1.1.2
```

- Confirm the version number update appears in `src/pyproject.toml`.
- Update `CHANGELOG.md` with the changes since the last release.
- If this release bumps OTel versions, update `README.md`.
- Commit changes, push, and open a release preparation pull request for review.
- Once the pull request is merged, fetch the updated `main` branch.
- Apply a tag for the new version on the merged commit (e.g. `git tag -a v2.3.1 -m "v2.3.1"`)
- Push the tag upstream (this will kick off the release pipeline in CI) e.g. `git push origin v2.3.1`
- Copy change log entry for newest version into draft GitHub release created as part of CI publish steps.
  - Make sure to "generate release notes" in github for full changelog notes and any new contributors
- Publish the github draft release and this will kick off publishing to GitHub and the PyPI registry.
