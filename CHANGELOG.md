# Changelog

## [v0.3.0](https://github.com/pyapp-kit/app-model/tree/v0.3.0) (2024-09-17)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.8...v0.3.0)

**Implemented enhancements:**

- feat: Include command/control-0 for OriginalSize in StandardKeyBindings [\#220](https://github.com/pyapp-kit/app-model/pull/220) ([psobolewskiPhD](https://github.com/psobolewskiPhD))
- feat: add support for `.svg` file paths as `Action` icon [\#219](https://github.com/pyapp-kit/app-model/pull/219) ([dalthviz](https://github.com/dalthviz))
- feat: add action keybinding info over tooltip [\#218](https://github.com/pyapp-kit/app-model/pull/218) ([dalthviz](https://github.com/dalthviz))

## [v0.2.8](https://github.com/pyapp-kit/app-model/tree/v0.2.8) (2024-07-19)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.7...v0.2.8)

**Implemented enhancements:**

- feat: more flexible keybinding parser [\#213](https://github.com/pyapp-kit/app-model/pull/213) ([tlambert03](https://github.com/tlambert03))
- feat: Add `filter_keybinding` to `KeyBindingRegistry` [\#212](https://github.com/pyapp-kit/app-model/pull/212) ([lucyleeow](https://github.com/lucyleeow))
- feat: add a way to get a user-facing string representation of keybindings [\#211](https://github.com/pyapp-kit/app-model/pull/211) ([dalthviz](https://github.com/dalthviz))
- feat: add Sequences to expressions [\#202](https://github.com/pyapp-kit/app-model/pull/202) ([tlambert03](https://github.com/tlambert03))

**Merged pull requests:**

- perf: faster `Expr.eval` by precompiling expressions [\#197](https://github.com/pyapp-kit/app-model/pull/197) ([tlambert03](https://github.com/tlambert03))

## [v0.2.7](https://github.com/pyapp-kit/app-model/tree/v0.2.7) (2024-05-08)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.6...v0.2.7)

**Implemented enhancements:**

- feat: give registries more control over registration of actions [\#194](https://github.com/pyapp-kit/app-model/pull/194) ([tlambert03](https://github.com/tlambert03))

## [v0.2.6](https://github.com/pyapp-kit/app-model/tree/v0.2.6) (2024-03-25)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.5...v0.2.6)

**Fixed bugs:**

- fix: Do not use lambda in QMenuItemAction.destroyed callback [\#183](https://github.com/pyapp-kit/app-model/pull/183) ([Czaki](https://github.com/Czaki))

## [v0.2.5](https://github.com/pyapp-kit/app-model/tree/v0.2.5) (2024-03-18)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.4...v0.2.5)

**Fixed bugs:**

- fix: handle qmods like QT5 for pyside6 not 6.4 [\#179](https://github.com/pyapp-kit/app-model/pull/179) ([psobolewskiPhD](https://github.com/psobolewskiPhD))

**Merged pull requests:**

- chore: add format to pre-commit [\#182](https://github.com/pyapp-kit/app-model/pull/182) ([tlambert03](https://github.com/tlambert03))
- chore: use ruff format instead of black [\#181](https://github.com/pyapp-kit/app-model/pull/181) ([tlambert03](https://github.com/tlambert03))
- ci: change test suite to cover more qt versions [\#180](https://github.com/pyapp-kit/app-model/pull/180) ([tlambert03](https://github.com/tlambert03))
- ci\(dependabot\): bump softprops/action-gh-release from 1 to 2 [\#178](https://github.com/pyapp-kit/app-model/pull/178) ([dependabot[bot]](https://github.com/apps/dependabot))
- ci: Add testing of napari/utils/\_tests/test\_key\_bindings.py [\#173](https://github.com/pyapp-kit/app-model/pull/173) ([Czaki](https://github.com/Czaki))
- ci: \[pre-commit.ci\] autoupdate [\#172](https://github.com/pyapp-kit/app-model/pull/172) ([pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci))

## [v0.2.4](https://github.com/pyapp-kit/app-model/tree/v0.2.4) (2023-12-21)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.3...v0.2.4)

**Implemented enhancements:**

- feat: export register\_action function at top level [\#170](https://github.com/pyapp-kit/app-model/pull/170) ([tlambert03](https://github.com/tlambert03))

**Documentation:**

- Fix doc typo for `register_action` [\#168](https://github.com/pyapp-kit/app-model/pull/168) ([aganders3](https://github.com/aganders3))
- docs: Add ref to in n out getting started [\#167](https://github.com/pyapp-kit/app-model/pull/167) ([lucyleeow](https://github.com/lucyleeow))

**Merged pull requests:**

- ci\(dependabot\): bump aganders3/headless-gui from 1 to 2 [\#165](https://github.com/pyapp-kit/app-model/pull/165) ([dependabot[bot]](https://github.com/apps/dependabot))
- ci\(dependabot\): bump actions/setup-python from 4 to 5 [\#164](https://github.com/pyapp-kit/app-model/pull/164) ([dependabot[bot]](https://github.com/apps/dependabot))
- refactor: remove comparison between Keybinding and string [\#146](https://github.com/pyapp-kit/app-model/pull/146) ([tlambert03](https://github.com/tlambert03))

## [v0.2.3](https://github.com/pyapp-kit/app-model/tree/v0.2.3) (2023-12-12)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.2...v0.2.3)

**Implemented enhancements:**

- feat: add top level Application.context [\#145](https://github.com/pyapp-kit/app-model/pull/145) ([tlambert03](https://github.com/tlambert03))
- feat: add `CommandRule.icon_visible_in_menu` [\#135](https://github.com/pyapp-kit/app-model/pull/135) ([tlambert03](https://github.com/tlambert03))
- feat: return QModelToolBar from call to QModelMainWindow.addModelToolBar [\#134](https://github.com/pyapp-kit/app-model/pull/134) ([tlambert03](https://github.com/tlambert03))
- feat: accept single string id as menu key in Actions.menus [\#133](https://github.com/pyapp-kit/app-model/pull/133) ([tlambert03](https://github.com/tlambert03))
- feat: support iconify icon keys [\#130](https://github.com/pyapp-kit/app-model/pull/130) ([tlambert03](https://github.com/tlambert03))
- feat: Show shortcut in `KeyBinding.__repr__` [\#126](https://github.com/pyapp-kit/app-model/pull/126) ([Czaki](https://github.com/Czaki))
- feat: support py312 [\#124](https://github.com/pyapp-kit/app-model/pull/124) ([tlambert03](https://github.com/tlambert03))

**Fixed bugs:**

- fix: catch runtime error on QModelSubmenu cleanup [\#151](https://github.com/pyapp-kit/app-model/pull/151) ([tlambert03](https://github.com/tlambert03))

**Tests & CI:**

- test: add test for mult\_file [\#140](https://github.com/pyapp-kit/app-model/pull/140) ([tlambert03](https://github.com/tlambert03))
- test: enforce 100 percent test coverage on project [\#136](https://github.com/pyapp-kit/app-model/pull/136) ([tlambert03](https://github.com/tlambert03))

**Documentation:**

- docs: remove minify plugin [\#154](https://github.com/pyapp-kit/app-model/pull/154) ([tlambert03](https://github.com/tlambert03))
- docs: use griffe-fieldz instead of builtin-extension [\#149](https://github.com/pyapp-kit/app-model/pull/149) ([tlambert03](https://github.com/tlambert03))
- docs: documentation overhaul [\#142](https://github.com/pyapp-kit/app-model/pull/142) ([tlambert03](https://github.com/tlambert03))
- docs: Fix bullet points in `Exp` [\#125](https://github.com/pyapp-kit/app-model/pull/125) ([lucyleeow](https://github.com/lucyleeow))

**Merged pull requests:**

- chore: Provide information about callback registered [\#166](https://github.com/pyapp-kit/app-model/pull/166) ([Czaki](https://github.com/Czaki))
- style: type cleanup/modernization [\#156](https://github.com/pyapp-kit/app-model/pull/156) ([tlambert03](https://github.com/tlambert03))
- ci: \[pre-commit.ci\] autoupdate [\#152](https://github.com/pyapp-kit/app-model/pull/152) ([pre-commit-ci[bot]](https://github.com/apps/pre-commit-ci))
- ci: Update CI workflow to include reusable test [\#150](https://github.com/pyapp-kit/app-model/pull/150) ([tlambert03](https://github.com/tlambert03))
- style: better qt typing [\#141](https://github.com/pyapp-kit/app-model/pull/141) ([tlambert03](https://github.com/tlambert03))
- ci: Unpin pyside6 in tests [\#138](https://github.com/pyapp-kit/app-model/pull/138) ([tlambert03](https://github.com/tlambert03))
- chore: remove setup.py, update ruff [\#131](https://github.com/pyapp-kit/app-model/pull/131) ([tlambert03](https://github.com/tlambert03))
- refactor: use pydantic-compat [\#128](https://github.com/pyapp-kit/app-model/pull/128) ([tlambert03](https://github.com/tlambert03))

## [v0.2.2](https://github.com/pyapp-kit/app-model/tree/v0.2.2) (2023-09-25)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.1...v0.2.2)

**Fixed bugs:**

- fix: propagate \_recurse value in `QModelSubmenu.update_from_context` method [\#122](https://github.com/pyapp-kit/app-model/pull/122) ([Czaki](https://github.com/Czaki))

**Merged pull requests:**

- ci\(dependabot\): bump actions/checkout from 3 to 4 [\#121](https://github.com/pyapp-kit/app-model/pull/121) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v0.2.1](https://github.com/pyapp-kit/app-model/tree/v0.2.1) (2023-08-30)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.2.0...v0.2.1)

**Fixed bugs:**

- fix: properly connect events for Contexts comprised of other Contexts [\#119](https://github.com/pyapp-kit/app-model/pull/119) ([kne42](https://github.com/kne42))

## [v0.2.0](https://github.com/pyapp-kit/app-model/tree/v0.2.0) (2023-07-13)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.1.4...v0.2.0)

**Implemented enhancements:**

- feat: map win and cmd to meta [\#113](https://github.com/pyapp-kit/app-model/pull/113) ([tlambert03](https://github.com/tlambert03))
- feat: support pydantic v2 [\#98](https://github.com/pyapp-kit/app-model/pull/98) ([tlambert03](https://github.com/tlambert03))

**Fixed bugs:**

- fix: Amend preferences `StandardKeyBinding` [\#104](https://github.com/pyapp-kit/app-model/pull/104) ([lucyleeow](https://github.com/lucyleeow))
- fix: fix menu titles in QtModelMenuBar [\#102](https://github.com/pyapp-kit/app-model/pull/102) ([tlambert03](https://github.com/tlambert03))

**Tests & CI:**

- ci: test pydantic1 [\#115](https://github.com/pyapp-kit/app-model/pull/115) ([tlambert03](https://github.com/tlambert03))

**Documentation:**

- docs: Move `_expressions.py` docstring to be included in documentation [\#107](https://github.com/pyapp-kit/app-model/pull/107) ([lucyleeow](https://github.com/lucyleeow))

## [v0.1.4](https://github.com/pyapp-kit/app-model/tree/v0.1.4) (2023-04-06)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.1.3...v0.1.4)

**Merged pull requests:**

- build: pin pydantic \< 2 [\#96](https://github.com/pyapp-kit/app-model/pull/96) ([tlambert03](https://github.com/tlambert03))

## [v0.1.3](https://github.com/pyapp-kit/app-model/tree/v0.1.3) (2023-04-06)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.1.2...v0.1.3)

**Fixed bugs:**

- fix: don't use mixin for menus [\#95](https://github.com/pyapp-kit/app-model/pull/95) ([tlambert03](https://github.com/tlambert03))

## [v0.1.2](https://github.com/pyapp-kit/app-model/tree/v0.1.2) (2023-03-07)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.1.1...v0.1.2)

**Fixed bugs:**

- fix: Fix typo in execute\_command method [\#86](https://github.com/pyapp-kit/app-model/pull/86) ([davidbrochart](https://github.com/davidbrochart))
- fix: Fix ctrl meta key swap \(for real this time \(i think\)\) [\#82](https://github.com/pyapp-kit/app-model/pull/82) ([kne42](https://github.com/kne42))

**Tests & CI:**

- Precommit updates [\#88](https://github.com/pyapp-kit/app-model/pull/88) ([tlambert03](https://github.com/tlambert03))

**Documentation:**

- docs: fix docs build \(add ToggleRule\) [\#79](https://github.com/pyapp-kit/app-model/pull/79) ([tlambert03](https://github.com/tlambert03))

**Merged pull requests:**

- build: use hatch for build and ruff for linting [\#81](https://github.com/pyapp-kit/app-model/pull/81) ([tlambert03](https://github.com/tlambert03))
- chore: rename napari org to pyapp-kit [\#78](https://github.com/pyapp-kit/app-model/pull/78) ([tlambert03](https://github.com/tlambert03))

## [v0.1.1](https://github.com/pyapp-kit/app-model/tree/v0.1.1) (2022-11-10)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.1.0...v0.1.1)

**Implemented enhancements:**

- feat: support python 3.11 [\#77](https://github.com/pyapp-kit/app-model/pull/77) ([tlambert03](https://github.com/tlambert03))

**Fixed bugs:**

- fix: fix unsupported operand [\#76](https://github.com/pyapp-kit/app-model/pull/76) ([tlambert03](https://github.com/tlambert03))

**Merged pull requests:**

- refactor: Use a dict \(as an ordered set\) instead of a list for menus registry [\#74](https://github.com/pyapp-kit/app-model/pull/74) ([aganders3](https://github.com/aganders3))
- ci\(dependabot\): bump styfle/cancel-workflow-action from 0.10.1 to 0.11.0 [\#72](https://github.com/pyapp-kit/app-model/pull/72) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v0.1.0](https://github.com/pyapp-kit/app-model/tree/v0.1.0) (2022-10-10)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.9...v0.1.0)

**Fixed bugs:**

- fix: properly detect when ctrl and meta swapped on mac [\#64](https://github.com/pyapp-kit/app-model/pull/64) ([kne42](https://github.com/kne42))
- fix various bugs [\#63](https://github.com/pyapp-kit/app-model/pull/63) ([kne42](https://github.com/kne42))

**Merged pull requests:**

- chore: changelog v0.1.0 [\#69](https://github.com/pyapp-kit/app-model/pull/69) ([tlambert03](https://github.com/tlambert03))
- feat: convert keybinding to normal class [\#68](https://github.com/pyapp-kit/app-model/pull/68) ([kne42](https://github.com/kne42))
- ci\(dependabot\): bump styfle/cancel-workflow-action from 0.10.0 to 0.10.1 [\#66](https://github.com/pyapp-kit/app-model/pull/66) ([dependabot[bot]](https://github.com/apps/dependabot))

## [v0.0.9](https://github.com/pyapp-kit/app-model/tree/v0.0.9) (2022-08-26)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.8...v0.0.9)

**Implemented enhancements:**

- feat: eval expr when creating menus [\#61](https://github.com/pyapp-kit/app-model/pull/61) ([tlambert03](https://github.com/tlambert03))

**Documentation:**

- docs: fix a few typos in docs [\#60](https://github.com/pyapp-kit/app-model/pull/60) ([alisterburt](https://github.com/alisterburt))

## [v0.0.8](https://github.com/pyapp-kit/app-model/tree/v0.0.8) (2022-08-21)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.7...v0.0.8)

**Implemented enhancements:**

- feat: add ToggleRule for toggleable Actions [\#59](https://github.com/pyapp-kit/app-model/pull/59) ([tlambert03](https://github.com/tlambert03))

**Tests & CI:**

- ci: add napari tests [\#57](https://github.com/pyapp-kit/app-model/pull/57) ([tlambert03](https://github.com/tlambert03))

**Merged pull requests:**

- refactor: switch to extra ignore [\#58](https://github.com/pyapp-kit/app-model/pull/58) ([tlambert03](https://github.com/tlambert03))

## [v0.0.7](https://github.com/pyapp-kit/app-model/tree/v0.0.7) (2022-07-24)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.6...v0.0.7)

**Merged pull requests:**

- build: relax runtime typing extensions dependency [\#49](https://github.com/pyapp-kit/app-model/pull/49) ([tlambert03](https://github.com/tlambert03))

## [v0.0.6](https://github.com/pyapp-kit/app-model/tree/v0.0.6) (2022-07-24)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.5...v0.0.6)

**Implemented enhancements:**

- feat: add get\_app class method to Application [\#48](https://github.com/pyapp-kit/app-model/pull/48) ([tlambert03](https://github.com/tlambert03))

## [v0.0.5](https://github.com/pyapp-kit/app-model/tree/v0.0.5) (2022-07-23)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.4...v0.0.5)

**Implemented enhancements:**

- test: more test coverage [\#46](https://github.com/pyapp-kit/app-model/pull/46) ([tlambert03](https://github.com/tlambert03))
- feat: add register\_actions [\#45](https://github.com/pyapp-kit/app-model/pull/45) ([tlambert03](https://github.com/tlambert03))
- fix: small getitem fixes for napari [\#44](https://github.com/pyapp-kit/app-model/pull/44) ([tlambert03](https://github.com/tlambert03))
- feat: qt key conversion helpers [\#43](https://github.com/pyapp-kit/app-model/pull/43) ([tlambert03](https://github.com/tlambert03))

**Fixed bugs:**

- fix: fix sorting when group is None [\#42](https://github.com/pyapp-kit/app-model/pull/42) ([tlambert03](https://github.com/tlambert03))

**Tests & CI:**

- tests: more qtest coverage [\#47](https://github.com/pyapp-kit/app-model/pull/47) ([tlambert03](https://github.com/tlambert03))

## [v0.0.4](https://github.com/pyapp-kit/app-model/tree/v0.0.4) (2022-07-16)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.3...v0.0.4)

**Implemented enhancements:**

- feat: add toggled to command [\#41](https://github.com/pyapp-kit/app-model/pull/41) ([tlambert03](https://github.com/tlambert03))
- feat: raise\_synchronous option, and expose app classes [\#40](https://github.com/pyapp-kit/app-model/pull/40) ([tlambert03](https://github.com/tlambert03))

## [v0.0.3](https://github.com/pyapp-kit/app-model/tree/v0.0.3) (2022-07-14)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.2...v0.0.3)

**Merged pull requests:**

- fix: expression hashing and repr [\#39](https://github.com/pyapp-kit/app-model/pull/39) ([tlambert03](https://github.com/tlambert03))

## [v0.0.2](https://github.com/pyapp-kit/app-model/tree/v0.0.2) (2022-07-13)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/v0.0.1...v0.0.2)

**Merged pull requests:**

- chore: move tlambert03/app-model to napari [\#38](https://github.com/pyapp-kit/app-model/pull/38) ([tlambert03](https://github.com/tlambert03))
- fix: allow older qtpy [\#37](https://github.com/pyapp-kit/app-model/pull/37) ([tlambert03](https://github.com/tlambert03))
- docs: Add Documentation [\#36](https://github.com/pyapp-kit/app-model/pull/36) ([tlambert03](https://github.com/tlambert03))
- feat: cache qactions \[wip\] [\#35](https://github.com/pyapp-kit/app-model/pull/35) ([tlambert03](https://github.com/tlambert03))
- feat: updating demo [\#34](https://github.com/pyapp-kit/app-model/pull/34) ([tlambert03](https://github.com/tlambert03))
- build: pin min typing extensions [\#33](https://github.com/pyapp-kit/app-model/pull/33) ([tlambert03](https://github.com/tlambert03))
- feat: add standard keybindings [\#32](https://github.com/pyapp-kit/app-model/pull/32) ([tlambert03](https://github.com/tlambert03))
- feat: frozen models [\#31](https://github.com/pyapp-kit/app-model/pull/31) ([tlambert03](https://github.com/tlambert03))
- refactor: restrict to only one command per id [\#30](https://github.com/pyapp-kit/app-model/pull/30) ([tlambert03](https://github.com/tlambert03))

## [v0.0.1](https://github.com/pyapp-kit/app-model/tree/v0.0.1) (2022-07-06)

[Full Changelog](https://github.com/pyapp-kit/app-model/compare/3a1e61cc7b0b249a9f2e3fce9cfa6cf6b766cb2a...v0.0.1)

**Merged pull requests:**

- refactor: a number of fixes [\#26](https://github.com/pyapp-kit/app-model/pull/26) ([tlambert03](https://github.com/tlambert03))
- feat: demo app [\#24](https://github.com/pyapp-kit/app-model/pull/24) ([tlambert03](https://github.com/tlambert03))
- test: fix pre-test [\#23](https://github.com/pyapp-kit/app-model/pull/23) ([tlambert03](https://github.com/tlambert03))
- build: add py.typed [\#22](https://github.com/pyapp-kit/app-model/pull/22) ([tlambert03](https://github.com/tlambert03))
- feat: add injection model to app [\#21](https://github.com/pyapp-kit/app-model/pull/21) ([tlambert03](https://github.com/tlambert03))
- feat: allow callbacks as strings [\#18](https://github.com/pyapp-kit/app-model/pull/18) ([tlambert03](https://github.com/tlambert03))
- refactor: create backend folder [\#17](https://github.com/pyapp-kit/app-model/pull/17) ([tlambert03](https://github.com/tlambert03))
- feat: Keybindings! [\#16](https://github.com/pyapp-kit/app-model/pull/16) ([tlambert03](https://github.com/tlambert03))
- feat: more qt support, submenus, etc [\#11](https://github.com/pyapp-kit/app-model/pull/11) ([tlambert03](https://github.com/tlambert03))
- feat: Add qt module [\#10](https://github.com/pyapp-kit/app-model/pull/10) ([tlambert03](https://github.com/tlambert03))
- feat: combine app model [\#9](https://github.com/pyapp-kit/app-model/pull/9) ([tlambert03](https://github.com/tlambert03))
- test: more test coverage, organization, and documentation [\#7](https://github.com/pyapp-kit/app-model/pull/7) ([tlambert03](https://github.com/tlambert03))
- fix: Fix windows keybindings tests [\#5](https://github.com/pyapp-kit/app-model/pull/5) ([tlambert03](https://github.com/tlambert03))
- ci\(dependabot\): bump codecov/codecov-action from 2 to 3 [\#2](https://github.com/pyapp-kit/app-model/pull/2) ([dependabot[bot]](https://github.com/apps/dependabot))
- ci\(dependabot\): bump styfle/cancel-workflow-action from 0.9.1 to 0.10.0 [\#1](https://github.com/pyapp-kit/app-model/pull/1) ([dependabot[bot]](https://github.com/apps/dependabot))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
