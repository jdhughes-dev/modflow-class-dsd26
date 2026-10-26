# Course Description
Class materials and schedule for the 2026 MODFLOW 6 advanced class at the DSD in Delft

## MODFLOW 6 preview build

Developmode builds of MODFLOW 6 with two development branches used in the class,
neither of which has been merged into MODFLOW 6:

- the `feat-swi` branch of
  [christianlangevin/modflow6](https://github.com/christianlangevin/modflow6/tree/feat-swi),
  the Seawater Intrusion (SWI) Package, and
- the `uzr-main` branch of
  [mjr-deltares/modflow6](https://github.com/mjr-deltares/modflow6/tree/uzr-main),
  the UZR Package, which solves the Richards equation for unsaturated flow,

merged into a single `mf6`.

The build uses the MODFLOW 6 release workflow in developmode, as the
[MODFLOW 6 nightly build](https://github.com/MODFLOW-ORG/modflow6-nightly-build) does:
binaries for Linux and Windows built with the Intel classic compiler, binaries for
macOS on Apple silicon built with gfortran, the tests, and the documentation.
Each build is posted under [Releases](../../releases), tagged with the UTC date
and time of the build and the two commits (`YYYYMMDD-HHMM-<feat-swi>-<uzr-main>`);
the newest is marked Latest, and the last 10 are kept.

`uzr-main` is merged into `feat-swi` in each job that checks out the source, by
the `.github/actions/merge-uzr` action. The two branches conflict in
`src/Model/GroundWaterFlow/gwf.f90`; the resolution is recorded in
`.github/rr-cache` and replayed by `git rerere`. If a change to either branch
causes a conflict with no recorded resolution, the build stops at the merge in
the first job and lists the files. Resolve the merge locally with rerere enabled
and copy the new entries in `.git/rr-cache` to `.github/rr-cache`:

```shell
git clone -b feat-swi https://github.com/christianlangevin/modflow6.git
cd modflow6
mkdir -p .git/rr-cache && cp -R ../.github/rr-cache/. .git/rr-cache/
git config rerere.enabled true
git pull --no-rebase https://github.com/mjr-deltares/modflow6.git uzr-main
# resolve the conflicts, then
git add -A && git commit --no-edit
cp -R .git/rr-cache/. ../.github/rr-cache/
```

The extended Windows build (parallel and NetCDF) is left out. To do that, the
workflow calls a copy of `.github/workflows/release.yml` from `feat-swi` with
the extended entries removed from the build and distribution matrices,
`${{ github.repository_owner }}/modflow6` replaced by `christianlangevin/modflow6`,
and the `uzr_ref` input and merge steps added. If the release workflow on the
branch changes, refresh the copy:

```shell
curl -sL https://raw.githubusercontent.com/christianlangevin/modflow6/feat-swi/.github/workflows/release.yml > .github/workflows/release.yml
```

and make the same changes again.

The `wt-uzr-spg` case of `autotest/test_gwf_uzr_wt.py` is skipped, by the test
filters in `release.yml`, because `uzr-main` changed the SPG input without
updating it. Remove the filter once the test is fixed on the branch.

The workflow runs nightly in mjr-deltares/modflow-class-dsd26 and builds only
when either branch has changed since the last release. Run it by hand from the
Actions tab, with `force` to rebuild unchanged branches; a fork runs it only by
hand.

Install the latest build with FloPy:

```shell
get-modflow --owner mjr-deltares --repo modflow-class-dsd26 :python
```

and generate the FloPy classes for the merged packages from the DFN asset of the
same release, unzipped:

```shell
python -m flopy.mf6.utils.generate_classes --dfnpath <path to unzipped dfns>
```

These builds are provisional and are not MODFLOW 6 releases.
