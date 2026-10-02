-- Deliberately incomplete fixture: a successful build is not a proof audit.
namespace AuditFixture

theorem proved : True := by trivial

theorem unfinished : False := by
  sorry

theorem dependsOnUnfinished : False := unfinished

axiom localAssumption : False

theorem assumesLocalAxiom : False := localAssumption

end AuditFixture
