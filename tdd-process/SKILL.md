---
name: TDD Process
description: "Strict test-driven development state machine with red-green-refactor cycles. Enforces test-first development, meaningful failures, minimum implementations, and full verification. Activates when user requests: 'use a TDD approach', 'start TDD', 'test-drive this'."
version: 1.0.0
---

# 🚨 CRITICAL: TDD STATE MACHINE GOVERNANCE 🚨

**EVERY SINGLE MESSAGE MUST START WITH YOUR CURRENT TDD STATE**

Format:
```
🔴 TDD: RED
🟢 TDD: GREEN
🔵 TDD: REFACTOR
⚪ TDD: PLANNING
🟡 TDD: VERIFY
⚠️ TDD: BLOCKED
```

**NOT JUST THE FIRST MESSAGE. EVERY. SINGLE. MESSAGE.**

When you read a file → prefix with TDD state
When you run tests → prefix with TDD state
When you explain results → prefix with TDD state
When you ask a question → prefix with TDD state

Example:
```
⚪ TDD: PLANNING
Writing test for negative price validation...

⚪ TDD: PLANNING
Running npm test to see it fail...

⚪ TDD: PLANNING
Test output shows: Expected CannotHaveNegativePrice error but received -50
Test fails correctly. Transitioning to RED.

🔴 TDD: RED
Test IS failing. Implementing minimum code to make it pass...
```

**🚨 FAILURE TO ANNOUNCE TDD STATE = SEVERE VIOLATION 🚨**

---

<meta_governance>
  <critical_override>
    THIS SKILL OPERATES UNDER STRICT STATE MACHINE GOVERNANCE.

    You CANNOT skip states.
    You CANNOT assume phase completion without evidence.
    You CANNOT proceed without satisfying post-conditions.
    You MUST announce state on EVERY message.
    You MUST validate transitions before executing them.

    VIOLATION OF STATE MACHINE = IMMEDIATE STOP + VIOLATION REPORT
  </critical_override>

  <state_consistency_protocol>
    🚨 ARCHITECTURAL CONSTRAINT #1: MANDATORY STATE CONSISTENCY CHECK 🚨

    BEFORE writing ANY response to user (this runs AUTOMATICALLY like a compiler):

    1. STATE RE-VALIDATION CHECKPOINT
       Ask yourself: "What TDD state am I claiming to be in?"

    2. EVIDENCE CHECK - Verify evidence exists in your recent tool calls:
       - If claiming PLANNING: Am I writing and running a test to see it fail?
       - If claiming RED: Did I see test FAILURE in PLANNING, test IS currently failing, am I implementing code?
       - If claiming GREEN: Did I implement code in RED and see test PASS, code COMPILE, code LINT, all IS currently passing?
       - If claiming REFACTOR: Test IS passing, code compiles, code lints, am I improving code quality?
       - If claiming VERIFY: Test IS passing, am I running full suite/lint/build?

    3. MANDATORY RECOVERY IF MISMATCH
       If you claim state X but lack evidence in your tool call history:

       🔥 STATE VIOLATION DETECTED
       "I claimed [STATE] but I have not satisfied its pre-conditions.
       Evidence missing: [what specific evidence is missing]
       Correct state is: [actual state based on evidence in tool history]
       Recovering to correct state now..."

    4. ONLY AFTER VALIDATION PASSES: Write response

    This check is ARCHITECTURAL, not optional. You cannot bypass it.
    Think of it like a compiler checking types before allowing compilation.
  </state_consistency_protocol>

  <state_announcement_enforcement>
    BEFORE writing ANY message to user:
    1. Check current state
    2. Write state prefix: `🔴 TDD: RED` (or current state)
    3. Then write your message
    4. NEVER skip step 2

    If you realize you forgot state prefix:
    - IMMEDIATELY announce: "⚠️ STATE VIOLATION DETECTED - Missing state announcement"
    - Announce correct current state
    - Continue
  </state_announcement_enforcement>
</meta_governance>

<state_machine>
  <diagram>
```
                  user request
                       ↓
                 ┌──────────┐
            ┌────│ PLANNING │────┐
            │    └─────┬────┘    │
            │          │         │
            │  test fails        │
            │  correctly         │
  unclear   │          ↓         │ blocker
            │    ┌──────────┐    │
            └────│   RED    │    │
                 │          │    │
                 │ Test IS  │    │
                 │ failing  │    │
                 └────┬─────┘    │
                      │          │
              test    │          │
              passes  │          │
                      ↓          │
                 ┌──────────┐    │
                 │  GREEN   │    │
                 │          │    │
                 │ Test IS  │    │
                 │ passing  │    │
                 └────┬─────┘────┘
                      │
          refactoring │
          needed      │
                      ↓
                 ┌──────────┐
            ┌────│ REFACTOR │
            │    │          │
            │    │ Improve  │
            │    │ design   │
            │    └────┬─────┘
            │         │
            │    done │
            │         │
            │         ↓
            │    ┌──────────┐
            │    │  VERIFY  │
            │    │          │
            │    │ Run full │
  fail      │    │ suite +  │
            │    │ lint +   │
            └────│ build    │
                 └────┬─────┘
                      │
                 pass │
                      │
                      ↓
                 [COMPLETE]
```
  </diagram>

  <states>
    <state name="PLANNING">
      <prefix>⚪ TDD: PLANNING</prefix>
      <purpose>Writing a failing test to prove requirement</purpose>

      <pre_conditions>
        ✓ User has provided a task/requirement/bug report
        ✓ No other TDD cycle in progress
      </pre_conditions>

      <actions>
        1. Analyze requirement/bug
        2. Ask clarifying questions if needed
        3. Determine what behavior needs testing
        4. Identify edge cases
        5. Write test for specific behavior
        6. Run test (use Bash tool to execute test command)
        7. VERIFY test fails correctly
        8. Show exact failure message to user (copy/paste verbatim output)
        9. Justify why failure message proves test is correct
        10. If failure is "method doesn't exist" - implement empty/dummy method and re-run from step 6
        11. Repeat until you get a "meaningful" failure
        12. Improve the code to produce a more explicit error message. Does the test failure provide a precise reason for the failure, if not ask the user if they want to make it better.
        13. Transition to RED
      </actions>

      <post_conditions>
        ✓ Test written and executed
        ✓ Test FAILED correctly (red bar achieved)
        ✓ Failure message shown to user verbatim
        ✓ Failure reason justified (proves test is correct)
        ✓ Failure is "meaningful" (not setup/syntax error)
      </post_conditions>

      <validation_before_transition>
        BEFORE transitioning to RED, announce:
        "Pre-transition validation:
        ✓ Test written: [yes]
        ✓ Test executed: [yes]
        ✓ Test failed correctly: [yes]
        ✓ Failure message shown: [yes - output above]
        ✓ Meaningful failure: [yes - justification]

        Transitioning to RED - test is now failing for the right reason."
      </validation_before_transition>

      <transitions>
        - PLANNING → RED (when test fails correctly - red milestone achieved)
        - PLANNING → BLOCKED (when cannot write valid test)
      </transitions>
    </state>

    <state name="RED">
      <prefix>🔴 TDD: RED</prefix>
      <purpose>Test IS failing for the right reason. Implement minimum code to make it pass.</purpose>

      🚨 CRITICAL: You are in RED state - test IS CURRENTLY FAILING. You MUST implement code and see test PASS, code COMPILE, code LINT before transitioning to GREEN.
      DO NOT transition to GREEN until you have:
      1. Implemented minimum code to address the failure
      2. Executed the test with Bash tool
      3. Seen the SUCCESS output (green bar)
      4. Executed compile check and seen SUCCESS
      5. Executed lint check and seen PASS
      6. Shown all success outputs to the user

      <pre_conditions>
        ✓ Test written and executed (from PLANNING)
        ✓ Test IS FAILING correctly (red bar visible)
        ✓ Failure message shown and justified
        ✓ Failure is "meaningful" (not setup/syntax error)
      </pre_conditions>

      <actions>
        1. Analyze failure message from failing test
        2. Determine MINIMUM change to pass test
        3. Implement ONLY that minimum change
        4. Run test (use Bash tool to execute test command)
        5. VERIFY test PASSES (green bar)
        6. Show exact success message to user (copy/paste verbatim output)
        7. Run quick compilation check (e.g., tsc --noEmit, or project-specific compile command)
        8. Run lint on changed code
        9. If compile/lint fails: Fix issues and return to step 4 (re-run test)
        10. Show compile/lint success output to user
        11. Justify why implementation is minimum
        12. ONLY AFTER completing steps 4-11: Announce post-condition validation
        13. ONLY AFTER validation passes: Transition to GREEN

        🚨 YOU CANNOT TRANSITION TO GREEN UNTIL TEST PASSES, CODE COMPILES, AND CODE LINTS 🚨
      </actions>

      <post_conditions>
        ✓ Minimum code implemented
        ✓ Test executed
        ✓ Test PASSES (green bar - not red)
        ✓ Success message shown to user verbatim
        ✓ Code compiles (no compilation errors)
        ✓ Code lints (no linting errors)
        ✓ Compile/lint output shown to user
        ✓ Implementation is minimum (justified)
      </post_conditions>

      <validation_before_transition>
        🚨 ARCHITECTURAL CONSTRAINT #4: POST-CONDITION EVIDENCE LINKS 🚨

        BEFORE transitioning to GREEN, announce with SPECIFIC EVIDENCE REFERENCES:
        "Post-condition validation:
        ✓ Minimum code implemented: [yes] - Changes: [brief description]
        ✓ Test executed: [yes] - Evidence: Bash tool call at [timestamp/message number]
        ✓ Test PASSES (green bar): [yes] - Evidence: See output showing [specific success indicator]
        ✓ Success message: [exact output copied verbatim] - Evidence: Copied from [location]
        ✓ Code compiles: [yes] - Evidence: [compile command output]
        ✓ Code lints: [yes] - Evidence: [lint command output]
        ✓ Compile/lint output shown: [yes] - Evidence: [where shown to user]
        ✓ Implementation is minimum: [yes] - Justification: [why this is minimum]

        Evidence index:
        - Tool call reference: [when/where in conversation]
        - Command executed: [exact command]
        - Output location: [specific message or line reference]
        - User-facing output: [where you showed output to user]
        - Compile command: [exact command used]
        - Lint command: [exact command used]

        All post-conditions satisfied. Test is NOW PASSING, code COMPILES, code LINTS. Transitioning to GREEN."

        IF you cannot provide specific evidence links:
        "⚠️ CANNOT TRANSITION - Missing evidence for post-condition: [which one]
        Cannot reference: [what's missing from tool history]
        Staying in RED state (test still failing) to address: [issue]"
      </validation_before_transition>

      <critical_rules>
        🚨 ARCHITECTURAL CONSTRAINT #2: EXPLICIT TOOL CALL VERIFICATION 🚨

        BEFORE claiming GREEN transition, VERIFY in your tool call history:

        MANDATORY VERIFICATION CHECKLIST (you must literally look back):
        1. [ ] Search your recent messages for code implementation
        2. [ ] Confirm test command was executed (npm test, pytest, cargo test, etc.)
        3. [ ] Locate the test output in the function_results block
        4. [ ] Verify output shows SUCCESS/PASS (green bar, not red bar)
        5. [ ] Confirm compile command was executed (tsc --noEmit, etc.)
        6. [ ] Verify compilation succeeded (no errors)
        7. [ ] Confirm lint command was executed (eslint, etc.)
        8. [ ] Verify linting passed (no errors)
        9. [ ] Confirm you showed test/compile/lint output to user in your message

        IF YOU CANNOT CHECK ALL 9 BOXES BY REFERENCING SPECIFIC PRIOR MESSAGES:
        🔥 VIOLATION - Cannot transition to GREEN
        "I was about to transition to GREEN, but my tool history verification shows:
        [ ] Code was implemented - Evidence: [Edit/Write tool reference or MISSING]
        [ ] Bash tool was invoked with test command - Evidence: [line/message reference or MISSING]
        [ ] Test output was received - Evidence: [reference or MISSING]
        [ ] Output showed SUCCESS/PASS (green bar) - Evidence: [specific success message or MISSING]
        [ ] Compile command was executed - Evidence: [line/message reference or MISSING]
        [ ] Compilation succeeded - Evidence: [compile output or MISSING]
        [ ] Lint command was executed - Evidence: [line/message reference or MISSING]
        [ ] Linting passed - Evidence: [lint output or MISSING]
        [ ] Output was shown to user - Evidence: [message reference or MISSING]
        [ ] Implementation is minimum - Evidence: [justification or MISSING]

        Missing evidence means I cannot transition. Test is STILL RED. Staying in RED state."

        ADDITIONAL CRITICAL RULES:
        🚨 RED state means test IS FAILING - you cannot be GREEN until test PASSES, code COMPILES, code LINTS
        🚨 NEVER transition to GREEN without FIRST implementing code
        🚨 NEVER transition to GREEN if test still FAILS (must see green bar/pass)
        🚨 NEVER transition to GREEN if code doesn't compile (must see successful compilation)
        🚨 NEVER transition to GREEN if code has lint errors (must see lint pass)
        🚨 NEVER transition to GREEN without showing test/compile/lint success output verbatim
        🚨 NEVER implement more than minimum required to pass test
        🚨 ALWAYS run test using Bash tool AFTER implementing
        🚨 ALWAYS run compile check AFTER test passes
        🚨 ALWAYS run lint check AFTER compile succeeds
        🚨 ALWAYS show exact success messages verbatim to user
        🚨 ALWAYS justify why implementation is minimum
      </critical_rules>

      <transitions>
        - RED → GREEN (when test PASSES, code COMPILES, code LINTS - green milestone achieved)
        - RED → BLOCKED (when cannot make test pass or resolve compile/lint errors)
        - RED → PLANNING (when test failure reveals requirement was misunderstood)
      </transitions>
    </state>

    <state name="GREEN">
      <prefix>🟢 TDD: GREEN</prefix>
      <purpose>Test IS passing for the right reason. Assess code quality and decide next step.</purpose>

      <pre_conditions>
        ✓ Test exists and PASSES (from RED)
        ✓ Test IS PASSING for the right reason (green bar visible)
        ✓ Code compiles (no compilation errors)
        ✓ Code lints (no linting errors)
        ✓ Pass output was shown and implementation justified as minimum
      </pre_conditions>

      <actions>
        1. Review the implementation that made test pass
        2. Check code quality against object calisthenics
        3. Check for feature envy
        4. Check for dependency inversion opportunities
        5. Check naming conventions
        6. Decide: Does code need refactoring?
        7a. If YES refactoring needed → Transition to REFACTOR
        7b. If NO refactoring needed → Transition to VERIFY
      </actions>

      <post_conditions>
        ✓ Test IS PASSING (green bar)
        ✓ Code quality assessed
        ✓ Decision made: refactor or verify
      </post_conditions>

      <validation_before_transition>
        BEFORE transitioning to REFACTOR or VERIFY, announce:
        "Post-condition validation:
        ✓ Test IS PASSING: [yes - green bar visible]
        ✓ Code quality assessed: [yes]
        ✓ Decision: [REFACTOR needed / NO refactoring needed, go to VERIFY]

        All post-conditions satisfied. Transitioning to [REFACTOR/VERIFY]."

        IF any post-condition NOT satisfied:
        "⚠️ CANNOT TRANSITION - Post-condition failed: [which one]
        Staying in GREEN state to address: [issue]"
      </validation_before_transition>

      <critical_rules>
        🚨 GREEN state means test IS PASSING, code COMPILES, code LINTS - if any fail, you're back to RED
        🚨 NEVER skip code quality assessment
        🚨 NEVER transition if test is not passing
        🚨 NEVER transition if code doesn't compile or lint
        🚨 ALWAYS assess whether refactoring is needed
        🚨 Go to REFACTOR if improvements needed, VERIFY if code is already clean
      </critical_rules>

      <transitions>
        - GREEN → REFACTOR (when refactoring needed - improvements identified)
        - GREEN → VERIFY (when code quality satisfactory - no refactoring needed)
        - GREEN → RED (if test starts failing - regression detected, need new failing test)
      </transitions>
    </state>

    <state name="REFACTOR">
      <prefix>🔵 TDD: REFACTOR</prefix>
      <purpose>Tests ARE passing. Improving code quality while maintaining green bar.</purpose>

      <pre_conditions>
        ✓ Tests ARE PASSING (from GREEN)
        ✓ Code compiles (no compilation errors)
        ✓ Code lints (no linting errors)
        ✓ Refactoring needs identified
        ✓ Pass output was shown
      </pre_conditions>

      <actions>
        1. Analyze code for design improvements
        2. Check against object calisthenics
        3. Check for feature envy
        4. Check for dependency inversion opportunities
        5. Check naming conventions
        6. If improvements needed:
           a. Explain refactoring
           b. Apply refactoring
           c. Run test to verify behavior preserved
           d. Show test still passes
        7. Repeat until no more improvements
        8. Transition to VERIFY
      </actions>

      <post_conditions>
        ✓ Code reviewed for quality
        ✓ Object calisthenics applied
        ✓ No feature envy
        ✓ Dependencies inverted
        ✓ Names are intention-revealing
        ✓ Tests still pass after each refactor
        ✓ Test output shown after each refactor
      </post_conditions>

      <validation_before_transition>
        BEFORE transitioning to VERIFY, announce:
        "Post-condition validation:
        ✓ Object calisthenics: [applied/verified]
        ✓ Feature envy: [none detected]
        ✓ Dependencies: [properly inverted]
        ✓ Naming: [intention-revealing]
        ✓ Tests pass: [yes - output shown]

        All post-conditions satisfied. Transitioning to VERIFY."
      </validation_before_transition>

      <critical_rules>
        🚨 NEVER skip object calisthenics check
        🚨 NEVER refactor without running tests after
        🚨 NEVER use generic names (data, utils, helpers)
        🚨 ALWAYS apply dependency inversion
        🚨 ALWAYS verify tests pass after refactor
      </critical_rules>

      <transitions>
        - REFACTOR → VERIFY (when code quality satisfactory)
        - REFACTOR → RED (if refactor broke test - write new test for edge case)
        - REFACTOR → BLOCKED (if cannot refactor due to constraints)
      </transitions>
    </state>

    <state name="VERIFY">
      <prefix>🟡 TDD: VERIFY</prefix>
      <purpose>Tests ARE passing. Run full test suite + lint + build before claiming complete.</purpose>

      <pre_conditions>
        ✓ Tests ARE PASSING (from GREEN or REFACTOR)
        ✓ Code compiles (no compilation errors)
        ✓ Code lints (no linting errors)
        ✓ Either: Refactoring complete OR no refactoring needed
      </pre_conditions>

      <actions>
        1. Run full test suite (not just current test)
        2. Capture and show output
        3. Run lint
        4. Capture and show output
        5. Run build
        6. Capture and show output
        7. If ALL pass → Transition to COMPLETE
        8. If ANY fail → Transition to BLOCKED or RED
      </actions>

      <post_conditions>
        ✓ Full test suite executed
        ✓ All tests PASSED
        ✓ Test output shown
        ✓ Lint executed
        ✓ Lint PASSED
        ✓ Lint output shown
        ✓ Build executed
        ✓ Build SUCCEEDED
        ✓ Build output shown
      </post_conditions>

      <validation_before_completion>
        BEFORE claiming COMPLETE, announce:
        "Final validation:
        ✓ Full test suite: [X/X tests passed - output shown]
        ✓ Lint: [passed - output shown]
        ✓ Build: [succeeded - output shown]

        All validation passed. TDD cycle COMPLETE.

        Session Summary:
        - Tests written: [count]
        - Refactorings: [count]
        - Violations: [count]
        - Duration: [time]"

        IF any validation FAILED:
        "⚠️ VERIFICATION FAILED
        Failed check: [which one]
        Output: [failure message]

        Routing to: [RED/BLOCKED depending on issue]"
      </validation_before_completion>

      <critical_rules>
        🚨 NEVER claim complete without full test suite
        🚨 NEVER claim complete without lint passing
        🚨 NEVER claim complete without build passing
        🚨 ALWAYS show output of each verification
        🚨 NEVER skip verification steps
      </critical_rules>

      <transitions>
        - VERIFY → COMPLETE (when all checks pass)
        - VERIFY → RED (when tests fail - regression detected)
        - VERIFY → REFACTOR (when lint fails - code quality issue)
        - VERIFY → BLOCKED (when build fails - structural issue)
      </transitions>
    </state>

    <state name="BLOCKED">
      <prefix>⚠️ TDD: BLOCKED</prefix>
      <purpose>Handle situations where progress cannot continue</purpose>

      <pre_conditions>
        ✓ Encountered issue preventing progress
        ✓ Issue is not user error or misunderstanding
      </pre_conditions>

      <actions>
        1. Clearly explain blocking issue
        2. Explain which state you were in
        3. Explain what you were trying to do
        4. Explain why you cannot proceed
        5. Suggest possible resolutions
        6. STOP and wait for user guidance
      </actions>

      <post_conditions>
        ✓ Blocker documented
        ✓ Context preserved
        ✓ Suggestions provided
        ✓ Waiting for user
      </post_conditions>

      <critical_rules>
        🚨 NEVER improvise workarounds
        🚨 NEVER skip steps to "unblock" yourself
        🚨 ALWAYS stop and wait for user
      </critical_rules>

      <transitions>
        - BLOCKED → [any state] (based on user guidance)
      </transitions>
    </state>

    <state name="VIOLATION_DETECTED">
      <prefix>🔥 TDD: VIOLATION_DETECTED</prefix>
      <purpose>Handle state machine violations</purpose>

      <trigger>
        Self-detected violations:
        - Forgot state announcement
        - Skipped state
        - Failed to validate post-conditions
        - Claimed phase complete without evidence
        - Skipped test execution
        - Changed assertion when test failed
      </trigger>

      <actions>
        1. IMMEDIATELY announce: "🔥 STATE VIOLATION DETECTED"
        2. Explain which rule/state was violated
        3. Explain what you did wrong
        4. Announce correct current state
        5. Ask user permission to recover
        6. If approved, return to correct state
      </actions>

      <example>
        "🔥 STATE VIOLATION DETECTED

        Violation: Forgot to announce state on previous message
        Current actual state: RED

        Recovering to correct state...

        🔴 TDD: RED
        [continue from here]"
      </example>
    </state>
  </states>
</state_machine>

<rules>
  <rule id="1">
    <title>No Green Without Proof</title>
    <state_enforcement>
      This rule is ENFORCED by GREEN and VERIFY state post-conditions.
      You CANNOT transition from GREEN without test pass evidence.
      You CANNOT transition from VERIFY without full suite pass evidence.
    </state_enforcement>

    <principle>
      If you didn't see green test output, you don't get to say the tests passed. No exceptions.
    </principle>

    <requirements>
      1. Never mark tests as "completed" or "passed" unless:
        - They have actually executed to completion
        - All relevant tests are GREEN (passing)
        - You have seen the actual test output confirming success
      2. Test execution is mandatory, not optional:
        - Don't ask permission to run tests - just run them
        - If tests fail to run due to environment issues, that's a BLOCKER
        - Investigate and resolve (check README, documentation) before proceeding
      3. Phase completion integrity:
        - GREEN state cannot transition without test pass evidence
        - VERIFY state cannot complete without full suite pass evidence
        - Missing evidence = VIOLATION_DETECTED
      4. The verification hierarchy:
        - ❌ Compilation success ≠ tests pass
        - ❌ Type checking success ≠ tests pass
        - ❌ "The code looks right" ≠ tests pass
        - ✅ Only actual test execution with passing results = tests pass
    </requirements>

    <validation>
      GREEN state post-conditions require:
      ✓ Test executed: [yes]
      ✓ Test passed: [yes]
      ✓ Pass output: [shown to user]
    </validation>
  </rule>

  <rule id="2">
    <title>Test failure messages must be shown and justified before entering RED</title>
    <state_enforcement>
      This rule is ENFORCED by PLANNING state post-conditions.
      You CANNOT transition from PLANNING to RED without showing failure message.
      You CANNOT transition from PLANNING to RED without justifying failure.
    </state_enforcement>

    <principle>
      When writing a test in PLANNING state, run it and show the precise message explaining why the test failed. Then explain why the error message correctly demonstrates the test is failing for the right reason. Only after this can you enter RED state (where test IS failing and you implement code to fix it).
    </principle>

    <example_scenario>
      We are in PLANNING state. We add test named "Cannot have negative price". We run the test and it fails (as expected). We show the failure and justify it. Now we can transition to RED.
    </example_scenario>

    <examples>
      <correct>
        Error message: "Expected CannotHaveNegativePrice error but received -50"

        Your output in PLANNING: "The test failed as expected because we haven't implemented negative price logic. Here's the exact failure message: 'Expected CannotHaveNegativePrice error but received -50'. This is the right failure - it proves our test is checking for the error. Transitioning to RED state (test is now failing)."
      </correct>
      <incorrect>
        Error message: "Database migration failed" <-- this is a setup issue, it doesn't demonstrate that we have a good test

        Your output: "The test failed. We have now entered the RED state"
      </incorrect>
    </examples>

    <validation>
      PLANNING state post-conditions require:
      ✓ Test FAILED correctly (red bar achieved)
      ✓ Failure message: [exact verbatim output]
      ✓ Failure justified: [explanation of why this proves test is correct]
      ✓ Meaningful failure: [not setup/syntax error]
    </validation>
  </rule>

  <rule id="3">
    <title>Implement minimum functionality to make a test pass</title>
    <state_enforcement>
      This rule is ENFORCED by RED state post-conditions.
      You CANNOT transition from RED to GREEN without justifying minimum implementation.
    </state_enforcement>

    <principle>
      When in RED state (test IS failing), you may only implement the minimum functionality to make it pass. This is crucial to an effective TDD strategy. Otherwise, you may implement logic that is not fully covered by the test - because you haven't proven the test fails for that specific reason.
    </principle>

    <examples>
      <correct>
        In RED state. Error message: Test failed - method blah() does not exist

        Your output: I'm in RED (test is failing). I will implement an empty blah() method because that is the minimum required to advance past this error. Then I'll run the test again.
      </correct>
      <incorrect>
        In RED state. Error message: Test failed - method blah() does not exist

        Your output: Great, I'm in RED. I'll now implement the whole blah method with all required functionality and transition to GREEN.
      </incorrect>
    </examples>

    <validation>
      RED state post-conditions require:
      ✓ Minimum implementation: [yes - explain why it's minimum]
    </validation>
  </rule>

  <rule id="4">
    <title>Don't be a lazy thinker</title>
    <state_enforcement>
      This rule applies in PLANNING and BLOCKED states.
      When asking questions, predict user response.
    </state_enforcement>

    <principle>
      When you ask the user a question, don't just throw options at the user. Take some time to think about what the user will say. Imagine you are the user, how do you think they will respond to your question based on previous discussions, preferences, and the current context? Present your questions along with what you think the user will respond.
    </principle>

    <examples>
      <correct>
        "The test is failing. Should I: 1. fix it  2. just implement the code and commit the changes? Since we are following a TDD process and this is important logic, I'm sure you're going to prefer option 1."
      </correct>
      <incorrect>
        "The test failed. What should I do? 1. fix it 2. move on 3. something else? I'll wait for your response"
      </incorrect>
    </examples>
  </rule>

  <rule id="5">
    <title>Green phase requires build and lint</title>
    <state_enforcement>
      This rule is ENFORCED by VERIFY state post-conditions.
      You CANNOT claim cycle complete without build and lint passing.
    </state_enforcement>

    <principle>
      Never tell the user that the green phase is completed if there are build or lint errors. The definition of green is build, lint, and test are all green.
    </principle>

    <examples>
      <correct>
        "🟡 TDD: VERIFY

        All tests are passing and we have completed the GREEN phase. The build and lint checks successfully pass.

        Final validation:
        ✓ Full test suite: [12/12 passed]
        ✓ Lint: [passed]
        ✓ Build: [succeeded]

        TDD cycle COMPLETE."
      </correct>
      <incorrect>
        "Congratulations. All tests are passing and we have completed the GREEN phase. I have no idea if the build or lint works I just care about the tests"
      </incorrect>
    </examples>

    <validation>
      VERIFY state post-conditions require:
      ✓ Lint executed: [yes]
      ✓ Lint passed: [yes]
      ✓ Build executed: [yes]
      ✓ Build succeeded: [yes]
    </validation>
  </rule>

  <rule id="6">
    <title>Add observability, avoid assumptions</title>
    <state_enforcement>
      This rule applies during REFACTOR state.
      When refactoring, add observability to make failures debuggable.
    </state_enforcement>

    <principle>
      Add observability to code so that when a test fails you can check the debug data to identify why it went wrong.

      Example: create a "report" object and each time a decision is made, update the "report" object. E.g.
      report.addFailedCheck(...) or report.reportSuccess(...)

      When a test fails, use this object to understand what went wrong. If it's not useful, add more observability until it is.
    </principle>
  </rule>

  <rule id="7">
    <title>Don't change assertions when test fails</title>
    <state_enforcement>
      CRITICAL: This rule prevents invalid GREEN transitions.
      If test fails, you CANNOT "fix" it by changing assertion.
      You must go to PLANNING or BLOCKED to understand root cause.
    </state_enforcement>

    <principle>
      When a test fails, do not change the assertion so that the test passes. When a test fails it is identifying a regression - this is the whole point of a test. To understand why it's failing and clarify what is supposed to happen - what did you do to break it.
    </principle>

    <examples>
      <correct>
        Output: Test Failed expect 8 to equal 9.
        Your behaviour: Something we have changed has broken this test. We have introduced a regression. What is the correct behaviour supposed to be here? Is this a true regression or do we have a bad test.

        🟢 TRANSITION: GREEN → PLANNING

        ⚪ TDD: PLANNING
        Investigating regression...
      </correct>
      <incorrect>
        Output: Test Failed expect 8 to equal 9.
        Your behaviour: I will update the test to expect 9 instead of 8
      </incorrect>
    </examples>

    <violation_detection>
      IF you find yourself about to change an assertion to make test pass:
      🔥 TDD: VIOLATION_DETECTED
      "Detected attempt to change assertion. This violates Rule #7.
      Proper action: Investigate why behavior changed.
      Transitioning to PLANNING to understand root cause."
    </violation_detection>
  </rule>

  <rule id="8">
    <title>Fail Fast - No Silent Fallbacks</title>
    <state_enforcement>
      This rule applies during GREEN and REFACTOR states.
      When implementing, fail fast with clear errors.
    </state_enforcement>

    <principle>
      Do not fall back to whatever data is available when the expected data is not there. This can cause problems that are hard to detect later. FAIL FAST - make the error easier to identify and resolve.
    </principle>

    <examples>
      <incorrect>
        <code>
          function extractName(content: Content): string {
            return content.eventType ?? content.className ?? 'Unknown'
          }
        </code>
        <reason>Silent fallback hides the problem - you'll never know that eventType is missing</reason>
      </incorrect>
      <correct>
        <code>
          function extractName(content: Content): string {
            if (!content.eventType) {
              throw new Error(
                `Expected 'eventType' to exist in content, but it was not found. ` +
                `Content keys: [${Object.keys(content).join(', ')}]`
              )
            }
            return content.eventType
          }
        </code>
        <reason>Fails immediately with a clear error message showing exactly what's missing</reason>
      </correct>
    </examples>

    <warning>
      When you specify that certain data is required (e.g., via `oneOfFields(['eventType', 'eventTypeStatic'])`), the code must throw an error if none of those fields exist. Do not silently fall back to alternative data.
    </warning>
  </rule>

  <rule id="9">
    <title>Follow dependency inversion principle - no hard dependencies</title>
    <state_enforcement>
      This rule is ENFORCED during REFACTOR state.
      Post-condition: Dependencies inverted.
    </state_enforcement>

    <principle>
      Do not directly instantiate classes or invoke static methods from another file within a method. Pass dependencies into the constructor or function to reduce coupling.
    </principle>

    <examples>
      <incorrect>
        <code>
          function extractName(content: Content): string {
            const nameExtractor = new NameExtractor()
            return nameExtractor.extract(content)
          }
        </code>
        <reason>Very tight coupling. Hard to change and test, unclear dependencies.</reason>
      </incorrect>
      <correct>
        <code>
           function extractName(content: Content): string {
             return this.nameExtractor.extract(content)
           }
        </code>
        <reason>delegates to dependency which can be easily switched out or tested</reason>
      </correct>
    </examples>

    <validation>
      REFACTOR state post-conditions require:
      ✓ Dependencies: [properly inverted - no direct instantiation]
    </validation>
  </rule>

  <rule id="10">
    <title>Do not guess or make assumptions - find hard data</title>
    <state_enforcement>
      This rule applies in ALL states.
      NEVER use "probably" - always find evidence.
    </state_enforcement>

    <principle>
      Do not use words like "probably" - this means you're guessing and most of the time you're wrong. Instead, find hard facts to prove an idea. Your guesses are meaningless and nobody wants to hear them.
    </principle>

    <examples>
      <incorrect>
        The issue is We're getting duplicates (probably because we scan with multiple definitions)
        <reason>"Probably" is a guess. It's not a fact. Therefore it is useless until proven.</reason>
      </incorrect>
      <correct>
        The issue is we're getting duplicates. I will add some diagnostics to find out why this is the case.
        <reason>Finds hard evidence instead of guessing</reason>
      </correct>
    </examples>

    <violation_detection>
      IF you catch yourself using "probably", "maybe", "might be":
      STOP immediately
      Add observability/logging
      Run code to get hard evidence
      Report facts, not guesses
    </violation_detection>
  </rule>

  <rule id="11">
    <title>Write minimal, non-redundant test assertions</title>
    <state_enforcement>
      This rule is ENFORCED during RED state.
      When writing test assertions, eliminate redundancy.
      Stronger assertions subsume weaker assertions.
    </state_enforcement>

    <principle>
      Write only the assertions that add actual test coverage. Avoid redundant assertions that are logically implied by stronger assertions. Each assertion should test something that isn't already guaranteed by other assertions in the same test.
    </principle>

    <explanation>
      When an assertion verifies a specific value, it implicitly verifies:
      - The value is defined/not null
      - The value has the correct type
      - The value has the correct length (for strings/arrays)

      These implied checks are redundant and clutter the test without adding coverage.
    </explanation>

    <examples>
      <redundant>
        <code>
          expect(result).toBeDefined()
          expect(result.length).toBe(35)
          expect(result).toBe('36 Proctorpark, Pierre Van Reynevel')
        </code>
        <reason>
          If the third assertion passes, the first two are automatically true.
          This is assertion clutter - three assertions testing one thing.
        </reason>
      </redundant>

      <minimal>
        <code>
          expect(result).toBe('36 Proctorpark, Pierre Van Reynevel')
        </code>
        <reason>
          Single assertion verifies the exact value. If this passes, we know:
          - result is defined (toBe would fail on undefined)
          - result has length 35 (toBe compares the full string)
          - result equals the expected value

          One assertion, complete coverage of the concept.
        </reason>
      </minimal>

      <redundant>
        <code>
          expect(user).not.toBeNull()
          expect(user.id).toBeDefined()
          expect(user.id).toBe(123)
        </code>
        <reason>
          Three assertions, but only the last one provides actual test coverage.
          The first two add no value.
        </reason>
      </redundant>

      <minimal>
        <code>
          expect(user.id).toBe(123)
        </code>
        <reason>
          If user is null or user.id is undefined, this assertion fails anyway.
          The error message and stack trace make the problem obvious.
          No need for defensive assertion scaffolding.
        </reason>
      </minimal>
    </examples>

    <critical_distinction>
      This rule is about REDUNDANT assertions testing the SAME concept.

      DIFFERENT: Multiple assertions for ONE concept = Acceptable when needed
      Example: Testing that an array contains exactly the right items
      ```
      expect(items.length).toBe(2)
      expect(items[0]).toBe('first')
      expect(items[1]).toBe('second')
      ```
      These are testing different aspects of the same concept (array contents).

      SAME: Multiple assertions where stronger subsumes weaker = Redundant
      Example: Checking defined before checking exact value
      ```
      expect(value).toBeDefined()  // <- redundant
      expect(value).toBe('exact')  // <- this is enough
      ```
      The specific value check makes the defined check unnecessary.
    </critical_distinction>

    <validation>
      RED state self-check when writing assertions:
      "For each assertion in this test:
      - What does this assertion prove that other assertions don't?
      - If I remove this assertion, does test coverage decrease?
      - Is this checking for something already implied by a stronger assertion?

      If an assertion doesn't add unique coverage → it's redundant clutter."
    </validation>

    <state_enforcement_detail>
      During RED state, when analyzing test you just wrote:
      ✓ Assertions are minimal: [yes - each assertion adds unique coverage]
      ✓ No redundant checks: [yes - no toBeDefined before toBe, no length before exact value]
      ✓ Test focuses on one concept: [yes - all assertions verify the same behavior]
    </state_enforcement_detail>
  </rule>

  <meta_rule>
    <title>State Machine Override</title>
    <principle>
      ALL rules above are ENFORCED through state machine post-conditions.
      You CANNOT violate a rule because you CANNOT transition without satisfying post-conditions.

      If you attempt to skip validation → VIOLATION_DETECTED
      If you forget state announcement → VIOLATION_DETECTED
      If you claim completion without evidence → VIOLATION_DETECTED

      The state machine is the enforcement layer.
      The rules define what must be true.
      The post-conditions make the rules checkable.
    </principle>
  </meta_rule>

  <repetition_for_reinforcement>
    🚨 CRITICAL REMINDERS 🚨

    1. EVERY message starts with state announcement
    2. NEVER skip state transitions
    3. ALWAYS validate post-conditions before transitioning
    4. NEVER claim test passed without showing output
    5. NEVER claim test failed without showing output
    6. ALWAYS justify failure messages in RED
    7. ALWAYS justify minimum implementation in GREEN
    8. ALWAYS run full suite + lint + build in VERIFY
    9. NEVER change assertions to make tests pass
    10. NEVER guess - always find hard evidence
    11. NEVER write redundant assertions - stronger assertions subsume weaker ones

    FAILURE TO FOLLOW = VIOLATION_DETECTED
  </repetition_for_reinforcement>
</rules>

<final_critical_reminders>
  🚨 TRIPLE REPETITION FOR MAXIMUM ADHERENCE 🚨

  1. STATE ANNOUNCEMENTS ARE MANDATORY
     - EVERY message starts with state prefix
     - Format: `🔴 TDD: RED` (or current state)
     - NO EXCEPTIONS

  2. POST-CONDITIONS MUST BE VALIDATED
     - BEFORE every transition
     - Announce validation results
     - If ANY post-condition fails → CANNOT TRANSITION

  3. TEST OUTPUT MUST BE SHOWN
     - NEVER claim test passed without showing output
     - NEVER claim test failed without showing output
     - Output must be verbatim

  4. COMPILATION AND LINTING REQUIRED
     - NEVER transition to GREEN without compiling code
     - NEVER transition to GREEN without linting code
     - Show compile/lint output verbatim
     - Fix compile/lint errors in RED state

  5. MINIMUM IMPLEMENTATION ONLY
     - In RED state (test failing), implement ONLY minimum to pass
     - Justify why it's minimum
     - Extra logic goes in next TDD cycle

  6. FULL VERIFICATION REQUIRED
     - Run full suite (not just one test)
     - Run lint
     - Run build
     - Show all outputs
     - ALL must pass before claiming complete

  7. NEVER CHANGE ASSERTIONS TO PASS
     - Test failure = regression or bad test
     - Investigate root cause
     - Go to PLANNING if needed
     - Do NOT "fix" by changing expected value

  8. NO GUESSING ALLOWED
     - Never use "probably", "maybe", "might be"
     - Add observability/logging
     - Get hard evidence
     - Report facts only

  9. VIOLATIONS ARE TRACKED
     - Self-detect violations immediately
     - Announce: "🔥 STATE VIOLATION DETECTED"
     - Recover to correct state

  10. STATE MACHINE IS LAW
      - Cannot skip states
      - Cannot auto-advance
      - Cannot bypass validation
      - State machine enforces ALL rules

  11. MINIMAL ASSERTIONS ONLY
      - Write only assertions that add unique coverage
      - Stronger assertions subsume weaker ones
      - No toBeDefined before toBe(value)
      - No length checks before exact value checks
      - Each assertion must test something new

  THESE RULES ARE YOUR CORE OPERATING SYSTEM.
  VIOLATION = SYSTEM FAILURE.
  ADHERENCE = SUCCESSFUL TDD.
</final_critical_reminders>
