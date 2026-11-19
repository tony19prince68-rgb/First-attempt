# Prompt Master

Rewrites your rough prompt into a clear, specific, well-structured one before you send it.

- Type a rough draft in the prompt box, then press the **✨ Prompt Master** button in the band just above the input. The draft is replaced with the improved prompt so you can review and edit it before sending.
- **Undo rewrite** puts your original draft back.
- Or run `/prompt-master <rough prompt>` to rewrite text you pass it.

The rewrite keeps your intent, names, paths and code, and never answers the prompt itself. It uses one small Sonnet call, counted in your session cost.

## Install

In a Claude Code session, type:

```
/plugin install prompt-master --marketplace tony19prince68-rgb/first-attempt
```

Answer `y` to add the marketplace, then pick a scope.

In this repository it is already on: `.claude/settings.json` adds this marketplace and enables `prompt-master@first-attempt`, so Claude Code offers to install it when you open the project.
