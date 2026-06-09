# ArticleProfile storage protocol

Reference document for `citation_coherence_verifier_agent.md` Stage 2.
Specifies the on-disk storage layout, slugification rules, locking
strategy, and the project-local override mechanism.

## Storage paths

| Path | Purpose | Precedence |
|------|---------|------------|
| `./working/profiles/{slug}.yaml` | Project-local override | First |
| `~/.manuscript-agents/profiles/{slug}.yaml` | User-global cache (default) | Fallback |

The verifier looks up the project-local path first. If a Profile exists
there, use it (read AND write). Otherwise, fall through to the
user-global path. **Project-local Profiles are never copied to
user-global automatically** — that would silently leak project-specific
annotations across manuscripts. The user can promote a Profile manually.

The user-global directory is created lazily on first write. Permissions:
0700 (user-only), set on first creation.

## DOI slugification

DOIs use characters that are inconvenient for filenames (`/`, `:`).
Slugify before storage.

### Algorithm

```
slug = doi
slug = slug.replace('/', '-')
slug = slug.replace(':', '-')
slug = slug.replace(' ', '_')   # extremely rare but possible
slug = slug.lower()
```

### Examples

| DOI | Slug | Storage path |
|-----|------|--------------|
| `10.1136/bmj.n71` | `10.1136-bmj.n71` | `~/.manuscript-agents/profiles/10.1136-bmj.n71.yaml` |
| `10.1056/NEJMoa1100356` | `10.1056-nejmoa1100356` | `~/.manuscript-agents/profiles/10.1056-nejmoa1100356.yaml` |
| `10.1016/j.brs.2016.12.014` | `10.1016-j.brs.2016.12.014` | `~/.manuscript-agents/profiles/10.1016-j.brs.2016.12.014.yaml` |

### Round-trip

```
doi  = slug.replace('-', '/', 1)   # only the FIRST dash is the registrant separator
```

The first dash splits registrant from suffix. Subsequent dashes within
the suffix (e.g., `j.brs` → kept as-is, no original dashes in suffix)
are preserved. The lowercasing is one-way (DOIs are case-insensitive
per RFC 3986 / DOI Handbook; the system stores case-folded for
consistency). When displaying, render via the canonical_metadata
fields, not the slug.

## Locking

Single-user assumption per BUILD_PLAN. Locking guards against the only
realistic concurrency: the same verifier invocation processing two
FactCards on the same Profile in parallel within one stage.

| Aspect | Strategy |
|--------|----------|
| Mechanism | POSIX advisory `flock(LOCK_EX)` on the YAML file during write |
| Timeout | 5 seconds |
| On timeout | Raise `PROFILE_LOCKED`; verifier requeues the write at end of turn |
| Read locking | None; reads are non-blocking (eventual consistency tolerated within a single stage) |
| Multi-process | Out of scope at v0.1. If detected, write a `multi_process_warning` to the report's `cache_warnings[]` |

## Append-only invariant

Writes only ADD entries to:

- `sections_processed[]`
- `author_stated_limitations[]`
- `known_findings[]`
- `caveats_encountered[]`
- `usage_log[]`

These five lists are append-only forever. No agent ever removes or
reorders entries. The user MAY edit `user_annotations[]` directly (e.g.,
"this paper has been retracted"); agents must never touch
`user_annotations`.

`completeness` is monotonically non-decreasing. `last_verified` is a
simple replacement. `canonical_metadata` is set once on first
materialization; subsequent verifier runs MAY refine null sub-fields
but must NOT overwrite non-null sub-fields without user confirmation.

### What "without user confirmation" means in practice

If a Stage 2 retrieval finds that the source paper's metadata has
changed (e.g., the journal corrected the publication year, or an author
was added in a corrigendum), the verifier:

1. Detects the discrepancy.
2. Surfaces it in the report's `cache_warnings[]` as `metadata_drift`.
3. Does NOT automatically update the Profile's `canonical_metadata`.
4. The user can resolve by editing the Profile manually or by adding a
   `user_annotation` recording the correction.

This is conservative by design. Silent metadata overwrites would erode
the reproducibility of past verifications.

## Project-local override semantics

When `./working/profiles/{slug}.yaml` exists, it wins for both reads
and writes for the duration of the project. The user-global Profile
(if any) is left untouched.

Use cases for the override:

- Working with a non-canonical source (e.g., a preprint version where
  the authoritative paper has different content).
- Sandbox experimentation without polluting the global cache.
- Sharing a Profile snapshot alongside a manuscript repository.

When the project completes and the user wants to merge insights back
into the global cache, that is a manual operation (the verifier does
not auto-merge — see "without user confirmation" above).

## Cache hygiene

| Concern | Strategy |
|---------|----------|
| Storage growth | Each Profile is small (~2-10 KB YAML). 1000 cached papers → ~5-10 MB. Negligible. |
| Stale Profiles | `last_verified` is the freshness signal. Verifier may treat Profiles older than 12 months as candidates for completeness re-assessment, but never auto-deletes. |
| Retracted papers | Surface via `caveats_encountered` AND `user_annotations`. Verifier never auto-deletes a Profile because its source was retracted; the retraction history is itself information. |
| Migration on schema change | When `article_profile_schema.yaml` `schema_version` bumps, profiles with older `schema_version` continue to work for read; writes upgrade in-place by adding any new required fields. Removed fields stay (the schema is only ever extended at v0.1). |

## See also

- `shared/article_profile_schema.yaml` — schema this protocol stores
- `manuscript-citations/agents/citation_coherence_verifier_agent.md` — Stage 2
- `manuscript-citations/references/citeaudit_pattern.md` — Stage 2 retrieval cost accounting
