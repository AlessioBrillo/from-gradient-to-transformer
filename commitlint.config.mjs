export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'body-max-line-length': [2, 'always', 200],
    'footer-max-line-length': [2, 'always', 200],
    'header-max-length': [2, 'always', 121],
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'build', 'ci', 'chore', 'revert', 'merge', 'config']],
  },
  // Scoped, auditable exceptions (2026-08-08 .. 2026-08-18). Each entry
  // names one exact message permanently in merged history that violates a
  // rule and cannot be rewritten (force-push blocked on dev; squash bodies
  // are GitHub-generated). Exact-message scope, never rule-relaxing. These
  // will never leave history, so they stay; the process fixes are the local
  // `commitlint-head` + `commitlint-new` mirrors in ci-check.
  ignores: [
    (message) => message.startsWith('docs(meta): add micro-phase-18 verdict-window roadmap, wire home, log pre-flight'),
    (message) => message.startsWith('docs(meta): add micro-phase-19 roadmap, wire home, log pre-flight'),
    (message) => message.startsWith('ci(ci): pardon superseded micro-phase-19 step-0 body line'),
    (message) => message.startsWith('docs(meta): add micro-phase-20 execution-arc roadmap, wire home, log pre-flight'),
    (message) => message.startsWith('ci(ci): local commitlint mirror plus scoped pardon for mp-20 step-0'),
    (message) => message.startsWith('docs(meta): P=113 verdict NO-GROK (val 1.0, Fourier dense k_99=111/113); ADR-0003 rows 1-2 stamped'),
    (message) => message.startsWith('feat(grokking): P=113 verdict NO-GROK; microscope flag; R1/R2 checkpoint infra (mp-28)'),
    (message) => message.startsWith('docs(meta): pre-register micro-phase 36, the fifth question'),
    (message) => message.startsWith('docs(meta): add the MP-52 review and roadmap, wired into home as a companion'),
    (message) => message.startsWith("ci(ci): scoped pardon for the mp-52 roadmap commit's footer line plus a new-commit lint mirror"),
    (message) => message.startsWith("docs(meta): add the MP-53 execution roadmap with architect's review, wired into home as a companion (#88)"),
    (message) => message.startsWith("docs(meta): add the MP-54 review and roadmap, wired into home as a companion (#89)"),
    // MP-74 Session 0 & 1 commits (2026-08-24) - subject-case violations, force-push blocked
    (message) => message.startsWith('docs(phase7): MP-74 Session 0 — gate truthing, 30th-gen arc consumption, continuum choice'),
    (message) => message.startsWith('docs(phase7): MP-74 Session 1 — progress log, gate-debt ledger, neuron ablation & clean-clone scripts'),
    // MP-74 Session 4 commit (2026-08-25) - type "proof" not in conventional types, force-push blocked
    (message) => message.startsWith('proof(production): add clean-clone reproducibility proof (MP-74 Session 4)'),
    // PR #119 commits (2026-08-31) - footer-leading-blank and type "config"
    (message) => message.startsWith('ci(markdown-lint): exclude .opencode and .venv from markdownlint'),
    (message) => message.startsWith('config(markdownlint): increase line length limit to 1000'),
  ],
};