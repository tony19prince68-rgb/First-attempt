# Instagram agent skills

13 Claude Code skills for running an Instagram account: Reels, captions,
carousels, stories, profile scoring, weekly plans, comments, replies, DMs,
repurposing, audits, viral research, and a humanizer.

Copied from [jakeschincariol/instagram-agent-skill](https://github.com/jakeschincariol/instagram-agent-skill)
by Jake Schincariol (MIT). See `LICENSE`. The original README has the full docs.

## Use

The skills live in `.claude/skills/`, so Claude Code picks them up whenever
you open this repo. To use them everywhere:

```bash
cp -r .claude/skills/ig-* ~/.claude/skills/
```

Fill in `templates/voice.md` and copy it to `~/.claude/instagram/voice.md`.
Every skill reads it.

## Skills

| command | what it does |
| --- | --- |
| `/ig-reel` | Reel script: scored hooks, script, on-screen text, timed beat sheet |
| `/ig-viral` | Finds what's working in your niche and builds a swipe file |
| `/ig-caption` | Caption, linted against the 125-character feed cut |
| `/ig-carousel` | Carousel cover, slide copy and 1080x1350 files |
| `/ig-story` | Daily story sequence and stickers |
| `/ig-profile` | Profile score out of 100, then rewrites |
| `/ig-plan` | The week's posts and engagement list |
| `/ig-human` | Humanizer: strips AI tells and scores the draft |
| `/ig-comment` | Comments on other people's posts |
| `/ig-reply` | Replies to comments on your posts |
| `/ig-dm` | DMs, pitches and follow-ups |
| `/ig-repurpose` | One long asset into a week of content |
| `/ig-audit` | Post-mortem on what you've posted |

Nothing posts to Instagram automatically. The skills write drafts and you post them.
