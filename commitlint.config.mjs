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
  ],
};
