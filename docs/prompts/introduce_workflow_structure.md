You are upgrading CRIS Companion to support structured workflow phases.

Objective:
Introduce a workflow structure WITHOUT changing current behavior.

Rules:

* Do NOT implement full loop yet
* Do NOT introduce recursion
* Do NOT change existing output behavior

Instead:

* Introduce workflow phases as functions:

  * select_module()
  * build_prompt()
  * generate()
  * refactor() (stub only)

* Engine.run() must still execute single-pass

* Add logging for phase transitions

* Prepare for future loop integration

Constraints:

* Keep implementation simple
* No overengineering
* No agent frameworks

Return:

* updated engine.py
