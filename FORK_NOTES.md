# EmergentMatter fork notes

This is a fork of [CMSL-HKUST/jax-am](https://github.com/CMSL-HKUST/jax-am)
preserved by EmergentMatter for AM-specific physics modules and ecosystem
continuity. Upstream is sparsely maintained (last push 2025-07-11); the
fork ensures we always have a working copy.

## Important: `jax_am/fem/` has been removed

Upstream marked the FEM module as deprecated and stated it would not be
updated in the future. From upstream's own README:

> "Check JAX-FEM. This is a design decision that aims to push the FEM
> module into a general-purpose, independent package that works for
> problems beyond additive manufacturing. Therefore, the code related to
> FEM in this repository (JAX-AM) will **NOT** be updated in the future."

Per that intent — which upstream announced but never completed — we've
removed:

- `jax_am/fem/` (~2.6 MB, the deprecated FEM module)
- `applications/fem/` (~4.0 MB, FEM demos that exercised the deprecated
  module)
- `demos/fem/` (~29 MB, additional FEM demos at the repo root that all
  imported from the deleted `jax_am.fem` and would have shipped as
  broken stubs)
- `gmsh` and `fenics-basix` from `setup.py` `install_requires`
  (verified zero imports in the surviving `cfd`, `lbm`, `phase_field`
  modules; both were FEM-only deps)

The FEM lineage is now exclusively at
[deepmodeling/jax-fem](https://github.com/deepmodeling/jax-fem),
mirrored at [EmergentMatter/jax-fem](https://github.com/EmergentMatter/jax-fem).

**New EmergentMatter consumers:**

- Use `jax_fem` (from the jax-fem fork) for all finite-element work —
  actively maintained, multiple element types, nonlinear analysis,
  sparse linear algebra, MMA optimizer.
- Use `jax_am.{cfd, lbm, phase_field}` for AM-specific physics —
  computational fluid dynamics, lattice-Boltzmann, and phase field
  methods respectively. These modules **do not** depend on the removed
  `jax_am.fem` (verified pre-removal).

## What remains in this fork

| Subpackage | Purpose | Status |
|---|---|---|
| `jax_am/cfd/` | Computational fluid dynamics for AM melt-pool flow | Independent, usable |
| `jax_am/lbm/` | Lattice-Boltzmann method (alternative fluid solver) | Independent, usable |
| `jax_am/phase_field/` | Phase field (dendrite formation, grain growth, Allen-Cahn) | Independent, usable |
| `jax_am/common.py` | Shared utilities | Used by all subpackages |

`setup.py` had `gmsh` and `fenics-basix` removed from `install_requires`
(zero imports in surviving code; both were FEM-only). `meshio` is
kept — it's actively used by `jax_am/common.py`, `jax_am/lbm/core.py`,
and most demos under `applications/{cfd,phase_field}/`.

## Suggested dependency layout for a new project

When a downstream EmergentMatter project needs both AM physics and FEM,
treat them as **independent peers**, not as a vertical stack:

```toml
# pyproject.toml of a downstream consumer
[project]
dependencies = [
    "jax>=0.4.30",
    "jax-fem",
    "jax-am",  # this fork
]

[tool.uv.sources]
jax-fem = { path = "../jax-fem", editable = true }
jax-am  = { path = "../jax-am",  editable = true }
```

`jax_am/{cfd,lbm,phase_field}` and `jax_fem` are unrelated solver
modules that compose at the *application* level (e.g., predicting
residual stress after a print run combines `jax_am.cfd` for melt-pool
flow → `jax_fem` for the stress solve). The two libraries don't depend
on each other internally.

## Rebase-against-upstream cost

Removing the deprecated FEM tree + its FEM-only deps is the entirety
of this fork's divergence from upstream. Concretely:

- `jax_am/fem/`, `applications/fem/`, `demos/fem/` — deleted paths
- 2 lines removed from `setup.py` (`gmsh`, `fenics-basix`)
- 1 new file (`FORK_NOTES.md`, this file)

If upstream ever revives jax-am development (unlikely given they've
stated otherwise), merge conflicts will be limited to the deleted
paths + the small setup.py diff — both trivially re-resolved by
`git rm` and a 2-line setup.py re-edit after rebase. We accept this
small ongoing cost as the price for a clean fork that doesn't ship
~35 MB of code marked "will not be updated."

## How this fork was created

```
gh repo fork CMSL-HKUST/jax-am --org EmergentMatter --clone=false
git clone https://github.com/EmergentMatter/jax-am.git
cd jax-am
git remote add upstream https://github.com/CMSL-HKUST/jax-am.git
git remote set-url --push upstream DISABLE_PUSH
git rm -r jax_am/fem applications/fem
# (this file) → git add FORK_NOTES.md
git commit + push to origin (EmergentMatter)
```

A bare-mirror backup of the upstream's full history is also kept at
`.backups/cmsl-hkust-jax-am.git` outside this repo.
