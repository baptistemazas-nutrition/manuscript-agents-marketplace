# Contributing — optimize Manuscript Agents together

The point of hosting this as a marketplace: everyone installs the same plugin **and** can improve it. Two ways to contribute.

## A. Tweak your own copy (local, not shared)
In Cowork, open the installed plugin and click **“Customize”** — Claude opens a task to adjust the plugin's skills for your workflow. Changes stay on your machine. Good for personal preferences.

## B. Share an improvement with everyone (pull request)
1. **Fork** this repo (or create a branch if you have write access).
2. **Edit** under `manuscript-agents/skills/…` — improve a `SKILL.md`, add a reference in `references/`, add an agent, fix a template, or add a whole new skill folder.
3. **Test locally** before submitting (see *Testing*).
4. **Bump the version** in `manuscript-agents/.claude-plugin/plugin.json` (semver: patch = fix, minor = new content, major = breaking).
5. Open a **pull request** describing what you changed and why.
6. After merge, everyone runs **“update marketplace”** in Cowork and reinstalls to get it.

## ⚠️ Validation rules — read before you submit
These are the rules that keep the plugin **installable**. Breaking them makes Cowork reject the plugin with *“Plugin validation failed.”*

1. **Skill frontmatter = `name` + `description` only.** Each `skills/<name>/SKILL.md` starts with:
   ```
   ---
   name: kebab-case-name
   description: "…"
   ---
   ```
   Do **not** add a `metadata:` block or other custom keys (only `argument-hint`, `user-invocable`, `compatibility` are also allowed). A `metadata:` block fails validation.
2. **`description` ≤ 1024 characters.** Keep it dense; put trigger phrases at the end.
3. **`name` is kebab-case** (`[a-z0-9-]`), ≤ 64 chars, and **matches the folder name**.
4. **Every folder directly under `skills/` is a real skill** with a `SKILL.md`. Don't put support folders (`shared/`, `scripts/`) under `skills/` — keep them at the plugin root if needed.
5. **`plugin.json` keys:** `name`, `version`, `description`, `author` (keep it minimal, like Anthropic's plugins).
6. **Keep it lean.** No `__pycache__`, no zero-byte files, no non-ASCII filenames, no giant binaries. Reference plugins run ~50–700 KB; ours is fine at ~0.7 MB — don't balloon it (e.g. don't commit datasets or PDFs).
7. **marketplace.json** (`.claude-plugin/marketplace.json`) lists the plugin with `source: "./manuscript-agents"`; update its `description` if the plugin's scope changes.

## Testing before a PR
- **Quick check** (run from the repo root):
  ```bash
  python3 - <<'PY'
  import os,re,yaml,json
  root="manuscript-agents"; AL={"name","description","argument-hint","user-invocable","compatibility"}
  for d in sorted(os.listdir(f"{root}/skills")):
      p=f"{root}/skills/{d}/SKILL.md"; 
      if not os.path.isfile(p): print("MISSING SKILL.md:",d); continue
      y=yaml.safe_load(re.match(r'^---\n(.*?)\n---',open(p,encoding='utf-8').read(),re.S).group(1))
      bad = (set(y)-AL) or len(y["description"])>1024 or not re.fullmatch(r"[a-z0-9-]+",y["name"])
      print(("BAD " if bad else "OK  ")+d, "desc",len(y["description"]))
  json.load(open(f"{root}/.claude-plugin/plugin.json")); print("plugin.json OK")
  PY
  ```
- **Stats engine** (if you touched `manuscript-statistics/assets/stats_toolkit.py`):
  ```bash
  cd manuscript-agents/skills/manuscript-statistics/assets
  bash bootstrap_env.sh && python3 -c "import stats_toolkit as t; print(t.versions())"
  ```
- **End-to-end**: package the plugin folder as a `.plugin` (zip) and install it locally via Customize → Plugins → import, then trigger the changed skill.

## Style for skill content
- `SKILL.md` is instructions **for Claude** (imperative: “Run…”, “Choose…”), not docs for a human.
- Put depth in `references/` (progressive disclosure); keep `SKILL.md` focused.
- Maintain the human-in-the-loop ethos: the tool does the grunt work; the researcher owns the question, method, and interpretation.

## License
Contributions are accepted under the project's **CC BY-NC 4.0** license (non-commercial, attribution). Don't add content you can't license this way.
