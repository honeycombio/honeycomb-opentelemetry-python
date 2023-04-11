# honeycomb-opentelemetry-python changelog

## [0.2.0b0] - 2023-04-11

### Maintenance

826d7f15 maint: Update OTel packages to 1.17.0/0.38b0 (#127) | [@MikeGoldsmith](https://github.com/MikeGoldsmith)
90caadb6 maint: Set opentelemetry to version 1.16.0 (#125) | [@guillemtrebol](https://github.com/guillemtrebol)
f8e92fde maint: Use squash merge for dependabot auto-merge (#122) | [@JamieDanielson](https://github.com/JamieDanielson)
e370c664 maint: Update readme status (#121) | [@vreynolds](https://github.com/vreynolds)
d2048622 maint: Change experimental badge to active (#120) | [@JamieDanielson](https://github.com/JamieDanielson)
22b31822 maint: Improve ci time (#114) | [@JamieDanielson](https://github.com/JamieDanielson)
1df3e26f maint: Add auto-merge dependabot workflow (#113) | [@JamieDanielson](https://github.com/JamieDanielson)
3f62d57c maint(deps-dev): bump pylint from 2.16.2 to 2.17.1 (#115)
29b61d09 maint(deps-dev): bump pytest from 7.2.1 to 7.2.2 (#117)
1a955972 maint(deps-dev): bump coverage from 7.2.1 to 7.2.3 (#126)
60f5267c maint(deps-dev): bump importlib-metadata from 6.0.0 to 6.1.0 (#119)

## [0.1.2b0] - 2023-03-29

Initial beta release of Honeycomb's OpenTelemetry distribution for Python!

### Maintenance

- ci: require smoke tests for publish steps (#107) | [@pkanal](https://github.com/pkanal)
- maint: drop poetry locks from example apps (#111) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: add tests for auto instrumentation (#110) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint(deps-dev): bump coverage from 6.5.0 to 7.2.1 (#104)

## [0.1.1a3] - 2023-03-07

### Enhancements

- feat: move away from a ParentBased sampling approach. (#96) | [@emilyashley](https://github.com/emilyashley)
- feat: allow HONEYCOMB_API_ENDPOINT as an Option parsed as an environment variable (#99) | [@emilyashley](https://github.com/emilyashley)

### Maintenance

- doc: clarify SDK configuration options (command vs function) and final developing.md & readme.md audits (#105) | [@emilyashley](https://github.com/emilyashley)
- maint: grpc smoke tests for hello-world-flask application (#102) | [@emilyashley](https://github.com/emilyashley)
- maint: Flask smoke tests for http and collector. (#101) | [@emilyashley](https://github.com/emilyashley)
- maint: dockerizing flask app (#83) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: smoke test python app (#91) | [@JamieDanielson](https://github.com/JamieDanielson)
- maint: add coverage report html to circleci artifacts (#93) | [@emilyashley](https://github.com/emilyashley)
- maint: enable linting step in CI  (#92) | [@emilyashley](https://github.com/emilyashley)
- doc: audit of docstrings for dev-friendliness & relevance (#85) | [@emilyashley](https://github.com/emilyashley)

## [0.1.1a2] - 2023-02-22

A very alpha release.
