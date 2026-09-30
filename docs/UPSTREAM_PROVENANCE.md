# Upstream Provenance & Lineage Record

## 1. Upstream Metadata
- **Official Upstream Repository:** `https://github.com/ostrokach/proteinsolver`
- **Original Author:** Alexey Strokach et al. (*Cell Systems* 2020)
- **Original License:** MIT License (preserved)
- **Fork Acquisition HEAD:** `69ef0965a3fc3bf191804035b539720a06e58ba6`
- **Scientific Reference Commit:** `69ef0965a3fc3bf191804035b539720a06e58ba6`
- **Relationship:** The fork acquisition HEAD and the scientific reference commit are identical (`69ef0965`). There are zero subsequent commits on upstream `ostrokach/proteinsolver`.

## 2. Downstream Organization Repository
- **Repository:** `https://github.com/ProteinDesignRND/ProteinSolver`
- **Creation Mechanism:** GitHub Organization Fork (`gh repo fork ostrokach/proteinsolver --org ProteinDesignRND`).
- **History Preservation:** 100% of upstream commit history from 2019–2020 is preserved in the git tree.
- **Default Branch:** `main` (protected by GitHub Ruleset).

## 3. Remote Safety Configuration
- `origin`: `https://github.com/ProteinDesignRND/ProteinSolver.git` (fetch + push)
- `upstream`: `https://github.com/ostrokach/proteinsolver.git` (fetch)
- Upstream push URL is configured to `no_push` (`git remote set-url --push upstream no_push`) to prevent accidental upstream writes.
