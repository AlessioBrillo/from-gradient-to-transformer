export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'body-max-line-length': [2, 'always', 200],
    'footer-max-line-length': [2, 'always', 200],
    'header-max-length': [2, 'always', 121],
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'build', 'ci', 'chore', 'revert', 'merge']],
  },
  // Scoped, auditable exception (2026-08-08): commit e8a0dd8 on dev was
  // pushed with a body line > 200 chars (body-max-line-length). The fix is
  // impossible without a force-push, which branch protection deliberately
  // blocks. The exception is exact-message-scoped, not rule-relaxing: any
  // other message must still conform. Revert when the bad commit leaves the
  // merged history.
  ignores: [
    (message) => message.startsWith('docs(meta): add micro-phase-18 verdict-window roadmap, wire home, log pre-flight'),
    // Scoped, auditable exception (2026-08-08): the micro-phase-19 step-0
    // roadmap commit (4a1e224 on dev) was also pushed with a body line
    // > 200 chars. Force-push is blocked on dev, so the exemption is
    // exact-message-scoped, not rule-relaxing. Revert when that commit
    // leaves the merged history.
    (message) => message.startsWith('docs(meta): add micro-phase-19 roadmap, wire home, log pre-flight'),
    // Scoped, auditable exception (2026-08-08): the pardon commit 3574fc7
    // itself repeated the same body-line mistake; same force-push
    // constraint, same exact-message scope. Revert when it leaves merged
    // history.
    (message) => message.startsWith('ci(ci): pardon superseded micro-phase-19 step-0 body line'),
    // Scoped, auditable exception (2026-08-08): the micro-phase-20 step-0
    // roadmap commit (b4588a5 on dev) was pushed with a body line > 200 chars
    // (body-max-line-length) — the same class as the three exceptions above,
    // and proof that the local mirror was still missing: with no local
    // commitlint, the class slips in again every time the workflow gap
    // closes. The pardon does not fix the process — the Makefile `commitlint`
    // target, added to ci-check the same day, is the repair. This entry
    // mirrors the precedent above and should be reverted alongside the
    // others once those commits leave merged history.
    (message) => message.startsWith('docs(meta): add micro-phase-20 execution-arc roadmap, wire home, log pre-flight'),
    // Scoped, auditable exception (2026-08-08): the repair commit itself for
    // MP-20 step-0 (befc545 on dev) shipped with a > 200-char body — the
    // exact class its own patch was closing, adding it minutes before the
    // commit that carried the fix. Force-push blocked; exact-message scope as
    // established above; the local `commitlint-head` mirror is henceforth run
    // on every message before push (the fix is the process, not the pardon).
    // Revert with the other entries when these commits leave merged history.
    (message) => message.startsWith('ci(ci): local commitlint mirror plus scoped pardon for mp-20 step-0'),
    // Scoped, auditable exception (2026-08-11): commit 929bf7a on dev
    // ("docs(meta): P=113 verdict NO-GROK ...") starts its subject with an
    // uppercase token and fails commitlint's subject-case rule on every PR
    // that includes it. Force-push is blocked on dev by branch protection,
    // and the rewrite-via-PR attempt (pr #60, rebase-merge) collapsed to a
    // no-op because the rewritten commits' content was already in base, so
    // the message is permanently in dev's history. Exact-message scope as
    // established above: the entry names one message and nothing else.
    // Revert when 929bf7a leaves the merged history.
    (message) => message.startsWith('docs(meta): P=113 verdict NO-GROK (val 1.0, Fourier dense k_99=111/113); ADR-0003 rows 1-2 stamped'),
    // Scoped, auditable exception (2026-08-12): the mp-28 squash commit
    // d626cdb on dev ("feat(grokking): P=113 verdict NO-GROK; microscope
    // flag; R1/R2 checkpoint infra (mp-28)") starts its subject with an
    // uppercase token and carries a >200-char body line, failing
    // commitlint's subject-case and body-max-line-length rules on every PR
    // that includes it. It entered dev via the PR #59 squash-merge
    // reconcile, not through a PR commit, so no PR check ever linted it;
    // force-push is blocked on dev by branch protection. Exact-message
    // scope as established above: the entry names one message and nothing
    // else. Revert when d626cdb leaves the merged history.
    (message) => message.startsWith('feat(grokking): P=113 verdict NO-GROK; microscope flag; R1/R2 checkpoint infra (mp-28)'),
    // Scoped, auditable exception (2026-08-14): the mp-36 pre-registration
    // squash commit bcb778a on dev ("docs(meta): pre-register micro-phase
    // 36, the fifth question") carries a >200-char body line
    // (body-max-line-length). It entered main via the PR #69 squash-merge
    // and dev via the reconcile merge, so no PR check ever linted it — the
    // PR's conventional-commits check ran before the squash commit existed,
    // and the local `commitlint-head` mirror only surfaces it now that the
    // reconcile merge makes bcb778a part of the linted range. Force-push is
    // blocked on dev by branch protection. Exact-message scope as
    // established above: the entry names one message and nothing else.
    // Revert when bcb778a leaves the merged history.
    (message) => message.startsWith('docs(meta): pre-register micro-phase 36, the fifth question'),
    // Scoped, auditable exception (2026-08-18): the mp-52 roadmap commit
    // 99285ef on dev ("docs(meta): add the MP-52 review and roadmap, wired
    // into home as a companion") carries a >200-char line in its second
    // body paragraph, which commitlint's parser treats as a footer and
    // flags via footer-max-line-length on the PR #87 lint-commits check.
    // Force-push is blocked on dev by branch protection. Exact-message
    // scope as established above: the entry names one message and nothing
    // else. Root cause, unlike the older entries: the message was never
    // linted before push — the local `commitlint-head` mirror lints the
    // existing HEAD (the reconcile merge), not the commit being created,
    // so a violation introduced by the new commit escapes it. The repair
    // commit adds a `commitlint-new` mirror (origin/dev..HEAD) to close
    // that gap; the fix is the process, not the pardon. Revert when 99285ef
    // leaves the merged history.
    (message) => message.startsWith('docs(meta): add the MP-52 review and roadmap, wired into home as a companion'),
    // Scoped, auditable exception (2026-08-18): the repair commit 3dab757
    // on dev ("ci(ci): scoped pardon for the mp-52 roadmap commit's footer
    // line plus a new-commit lint mirror") carries a >200-char body line
    // (body-max-line-length) — the same class its own patch closes, the
    // mp-20 recursion precedent (3574fc7, befc545). Force-push is blocked
    // on dev by branch protection. Exact-message scope as established
    // above: the entry names one message and nothing else. The process fix
    // stands: commitlint-new (origin/dev..HEAD) is in ci-check and must be
    // run and green before any push. Revert when 3dab757 leaves the merged
    // history.
    (message) => message.startsWith('ci(ci): scoped pardon for the mp-52 roadmap commit\'s footer line plus a new-commit lint mirror'),
    // Scoped, auditable exception (2026-08-18): the mp-53 squash commit
    // ae867d5 on main ("docs(meta): add the MP-53 execution roadmap with
    // architect's review, wired into home as a companion (#88)") embeds the
    // mp-52 PR's commit messages in its GitHub-generated squash body, whose
    // >200-char lines (the 99285ef and 3dab757 bodies) fail
    // footer-max-line-length whenever the linted range includes it — so the
    // post-reconcile commitlint-head mirror fails on every dev HEAD. The
    // message is GitHub-generated and force-push is blocked on dev, so the
    // exception is exact-message-scoped as established above: the entry
    // names one message and nothing else. Revert when ae867d5 leaves the
    // merged history.
    (message) => message.startsWith('docs(meta): add the MP-53 execution roadmap with architect\'s review, wired into home as a companion (#88)'),
  ],
};