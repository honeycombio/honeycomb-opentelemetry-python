# Releasing

- Update the version number in `pyproject.toml`. Our current versioning uses the `b` for `beta`, so a patch bump for `0.4.0b0` would go to `0.4.1b0` and a minor bump from `0.4.1b0` would go to `0.5.0b0`.
- Update `CHANGELOG.md` with the changes since the last release. Consider automating with a command such as these two:
  - `git log $(git describe --tags --abbrev=0)..HEAD --no-merges --oneline > new-in-this-release.log`
  - `git log --pretty='%C(green)%d%Creset- %s | %an'`
- If the upstream OpenTelemetry package versions have changed, update `README.md` with new versions and links.
- Commit changes, push, and open a release preparation pull request for review.
- Once the pull request is merged, fetch the updated `main` branch.
- Apply a tag for the new version on the merged commit (e.g. `git tag -a v2.3.1 -m "v2.3.1"`)
- Push the tag upstream (this will kick off the release pipeline in CI) e.g. `git push origin v2.3.1`
- Ensure that there is a draft GitHub release created as part of CI publish steps (this will also publish to PyPI).
- Click "generate release notes" in GitHub for full changelog notes and any new contributors
- Publish the github draft release - if it is a prerelease (e.g., beta) click the prerelease checkbox.
