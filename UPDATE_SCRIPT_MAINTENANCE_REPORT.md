## Update Script Maintenance Report

Date: 2026-03-04

- Root cause: updater failed on transient Yahoo Finance errors and workflow lacked explicit write permission.
- Fixes made: hardened financial fetch loop to tolerate per-symbol fetch failures, modernized workflow triggers/actions, and added `permissions: contents: write`.
- Validation: reviewed script exception handling and workflow commit guard.
- Known blockers: upstream Yahoo Finance rate limiting can still reduce completeness on some runs.
