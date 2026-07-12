# Agent Tool Naming Standard

All tools are registered in `tools/catalog.json` and validated in CI.

- Use lowercase `snake_case` and verb-first `action_object` names.
- Add a domain namespace when actions could collide.
- Keep one narrow responsibility per tool; split god tools.
- Avoid abbreviations, slang, implementation jargon, and duplicate names.
- Keep released names stable.
- Descriptions state what the tool does, when to use it, what it returns, and an example.
- Parameters use descriptive snake_case, explicit types/enums, minimal required fields, and server-side validation.
- Review name, action orientation, scope, description, typed parameters, uniqueness, and namespace before merge.
