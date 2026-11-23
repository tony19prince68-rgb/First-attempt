"""Builds the Inner Compass TikTok carousels (1080x1920) as HTML, one folder each.

    python3 carousels/build_carousels.py

Each carousel's slides.html is then shot to slide-NN.png. Same design system as
2026-11-23-autopilot-signs: heavy Inter Display type, one accent colour, one
inverted "hard one" slide, a closing ask. Layouts vary by format.
"""
import html
from pathlib import Path

HERE = Path(__file__).parent
DATE = '2026-11-24'

THEMES = {
    'orange': dict(bg='#FFF4E8', accent='#D9481A', soft='#FFC9A8', light='#FF9A6B', muted='#5A4A40', end='#D9481A', endsoft='#FFE2D2'),
    'mint':   dict(bg='#E9F7EF', accent='#0F7A52', soft='#A8E3C5', light='#5FD3A0', muted='#3F5A4D', end='#0F7A52', endsoft='#D6F3E4'),
    'rasp':   dict(bg='#FDEEF1', accent='#C42D62', soft='#F7B8CC', light='#FF86AE', muted='#5E4650', end='#C42D62', endsoft='#FFDCE7'),
    'blue':   dict(bg='#EAF3FF', accent='#1D57CC', soft='#B5CEFA', light='#7FA8FF', muted='#435068', end='#1D57CC', endsoft='#DCE8FF'),
    'violet': dict(bg='#F4EFFF', accent='#5B2EE0', soft='#C9B2FF', light='#B79BFF', muted='#4B4360', end='#5B2EE0', endsoft='#EDE6FF'),
    'teal':   dict(bg='#F3EFE6', accent='#0E6A66', soft='#A9DAD5', light='#5CCFC6', muted='#4E4A40', end='#0E6A66', endsoft='#D7F0EE'),
}

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0 }
body { background: #222; font-family: 'Inter Display', Inter, 'Noto Color Emoji', sans-serif }
.s { width: 1080px; height: 1920px; position: relative; overflow: hidden; background: var(--bg); color: #120C1E; padding: 300px 110px 0 }
.s.dark { background: #0B0713; color: #fff }
.s.end { background: var(--end); color: #fff }
.tag { position: relative; z-index: 1; font: 700 38px Inter; letter-spacing: 6px; text-transform: uppercase; color: var(--accent); margin-bottom: 70px }
.dark .tag { color: var(--light) } .end .tag { color: var(--endsoft) }
h1 { font-weight: 900; font-size: 146px; line-height: 1.02; letter-spacing: -3px }
.mark { background: linear-gradient(transparent 58%, var(--soft) 58%, var(--soft) 92%, transparent 92%); padding: 0 6px; margin: 0 -6px }
.sub { font: 700 54px Inter; color: var(--accent); margin-top: 80px }
.num { font-weight: 900; font-size: 380px; line-height: .8; color: var(--accent); letter-spacing: -12px; margin-bottom: 60px }
.dark .num { color: var(--light) }
h2 { font-weight: 800; font-size: 100px; line-height: 1.08; letter-spacing: -2px }
p { font: 400 54px/1.36 Inter; color: var(--muted); margin-top: 54px; max-width: 840px }
.dark p { color: #C9C0DC } .end p { color: var(--endsoft) }
.next { position: absolute; left: 110px; top: 1480px; font: 700 38px Inter; color: var(--accent); letter-spacing: 1px }
.dark .next { color: var(--light) }
.pill { display: inline-block; font: 800 36px Inter; letter-spacing: 5px; padding: 12px 26px; border-radius: 999px; margin-bottom: 40px }
.pill.lie { background: #120C1E; color: #fff } .dark .pill.lie { background: #fff; color: #120C1E }
.pill.truth { background: var(--accent); color: #fff; margin-top: 90px } .dark .pill.truth { background: var(--light); color: #0B0713 }
.struck { text-decoration: line-through; text-decoration-color: var(--accent); text-decoration-thickness: 10px; color: #8A8296 }
.dark .struck { color: #8E86A3; text-decoration-color: var(--light) }
.truth-text { font: 600 64px/1.3 Inter; color: #120C1E; margin-top: 0 } .dark .truth-text { color: #fff }
.old { font-weight: 800; font-size: 110px; letter-spacing: -2px }
.arrow { font-weight: 900; font-size: 120px; color: var(--accent); line-height: 1.1; margin: 20px 0 } .dark .arrow { color: var(--light) }
.new { font-weight: 900; font-size: 168px; line-height: .98; letter-spacing: -5px; color: var(--accent) } .dark .new { color: var(--light) }
.q { font-weight: 900; font-size: 420px; line-height: .7; color: var(--accent); height: 220px } .dark .q { color: var(--light) }
.small { position: relative; z-index: 1; font: 700 40px Inter; color: var(--accent); letter-spacing: 2px; margin-bottom: 60px } .dark .small { color: var(--light) }
.qmark { position: absolute; right: 40px; top: 160px; font-weight: 900; font-size: 900px; line-height: 1; color: var(--soft); opacity: .45 }
.dark .qmark { color: #2A2140; opacity: 1 }
.big { font-weight: 900; font-size: 160px; line-height: 1; letter-spacing: -4px }
.lead { font: 600 64px Inter !important; color: #fff !important; margin-top: 90px !important }
.follow { font-weight: 700 !important; color: #fff !important; margin-top: 120px !important }
"""

e = html.escape


def cover(tag, title, mark, sub):
    t = e(title).replace(e(mark), f'<span class="mark">{e(mark)}</span>', 1)
    return f'<div class="tag">{e(tag)}</div><h1>{t}</h1><div class="sub">{e(sub)}</div>'


def slide(kind, d, dark=False, nxt='→'):
    cls = 's dark' if dark else 's'
    tag = f'<div class="tag">{e(d["tag"])}</div>' if d.get('tag') else ''
    nx = f'<div class="next">{e(nxt)}</div>' if nxt else ''
    if kind == 'num':
        body = f'{tag}<div class="num">{d["n"]}</div><h2>{e(d["h"])}</h2><p>{e(d["p"])}</p>'
    elif kind == 'lie':
        body = (f'{tag}<div class="pill lie">LIE #{d["n"]}</div><h2 class="struck">{e(d["lie"])}</h2>'
                f'<div class="pill truth">TRUTH</div><p class="truth-text">{e(d["truth"])}</p>')
    elif kind == 'swap':
        body = (f'{tag}<div class="small">{d["n"]:02d} · We call it</div><div class="old struck">{e(d["old"])}</div>'
                f'<div class="arrow">↓</div><div class="new">{e(d["new"])}</div><p>{e(d["p"])}</p>')
    elif kind == 'quote':
        body = f'{tag}<div class="q">“</div><h2>{e(d["h"])}</h2><p>{e(d["p"])}</p>'
    elif kind == 'question':
        body = f'<div class="qmark">?</div>{tag}<div class="small">{e(d["k"])}</div><h2 style="font-size:108px;position:relative">{e(d["h"])}</h2>'
        if d.get('p'):
            body += f'<p style="position:relative">{e(d["p"])}</p>'
    elif kind == 'step':
        body = f'<div class="small">{e(d["k"])}</div><h2 style="font-size:116px">{e(d["h"])}</h2><p>{e(d["p"])}</p>'
    return f'<section class="{cls}">{body}{nx}</section>'


def end(ask, lead, share):
    return (f'<section class="s end"><div class="tag">Your turn</div><div class="big">{e(ask)}</div>'
            f'<p class="lead">{e(lead)}</p><p>{e(share)}</p>'
            f'<p class="follow">Follow @atheic for the parts nobody posts. 🧭</p></section>')


C = []

# 1. myth vs truth
C.append(('5-lies-about-waking-up', 'orange', [
    f'<section class="s">{cover("Inner Compass 🧭", "5 lies you’ve been told about waking up", "lies", "#3 keeps most people stuck →")}</section>',
    slide('lie', dict(n=1, lie='It feels peaceful.', truth='At first it mostly feels disorienting. The peace comes later, and quietly.'), nxt='Swipe →'),
    slide('lie', dict(n=2, lie='You’ll finally find your purpose.', truth='Mostly you find out what isn’t it. That counts.')),
    slide('lie', dict(n=3, tag='The one that keeps people stuck', lie='Once you see it, you can’t go back.', truth='You can. You will. Drifting back to sleep is part of it, not proof you failed.'), dark=True),
    slide('lie', dict(n=4, lie='Awake people are always calm.', truth='They still get angry. They just notice it sooner.')),
    slide('lie', dict(n=5, lie='You have to leave everything behind.', truth='Most people change how they show up, not where they live.')),
    end('Which one did you believe longest?', 'Comment the number.', 'Send it to someone who’s been told #3.'),
]))

# 2. reframes
C.append(('what-we-call-it', 'mint', [
    f'<section class="s">{cover("Inner Compass 🧭", "What we call it vs. what it really is", "really", "#5 is the uncomfortable one →")}</section>',
    slide('swap', dict(n=1, old='Busy', new='Avoiding', p='A full calendar can be a very good place to hide.'), nxt='Swipe →'),
    slide('swap', dict(n=2, old='Being nice', new='Being scared', p='Of their reaction. Not of hurting them.')),
    slide('swap', dict(n=3, old='Relaxing', new='Numbing', p='If you need to switch off every night, ask what you’re switching off from.')),
    slide('swap', dict(n=4, old='Ambition', new='Approval', p='Would you still want it if nobody could see it?')),
    slide('swap', dict(n=5, tag='The uncomfortable one', old='Loyalty', new='Habit', p='Some of the people you stay for, you’d never choose today.'), dark=True),
    slide('swap', dict(n=6, old='“I’m fine”', new='Not looking', p='Fine is what we say when we’d rather not check.')),
    end('Which one stung?', 'Tell me in the comments.', 'Send it to the busiest person you know.'),
]))

# 3. body signals
C.append(('body-noticed-first', 'rasp', [
    f'<section class="s">{cover("Inner Compass 🧭", "Your body noticed before you did", "body", "6 signals most people ignore →")}</section>',
    slide('num', dict(n=1, h='Your jaw is tight on Sunday nights.', p='Part of you is already sitting at Monday.'), nxt='Swipe →'),
    slide('num', dict(n=2, h='You hold your breath when your phone lights up.', p='Check next time. Most people do.')),
    slide('num', dict(n=3, h='You’re drained after some people and fine after others.', p='That’s not you being difficult. That’s information.')),
    slide('num', dict(n=4, h='Your shoulders drop the second you’re alone.', p='Notice who you were bracing for.')),
    slide('num', dict(tag='The one people explain away', n=5, h='Your stomach drops right after you say yes.', p='Your mouth agreed. Something else didn’t.'), dark=True),
    slide('num', dict(n=6, h='You only feel how tired you are when you finally stop.', p='Rest isn’t making you tired. It’s just the first time you’re still enough to notice.')),
    end('Which one does your body do?', 'Comment the number.', 'Send it to someone whose jaw is tight right now.'),
]))

# 4. sentences
C.append(('sentences-that-keep-you-asleep', 'blue', [
    f'<section class="s">{cover("Inner Compass 🧭", "6 sentences that keep you asleep", "asleep", "You said one of these today →")}</section>',
    slide('quote', dict(h='I’m just tired.', p='Sometimes it’s sleep. Sometimes it’s the life.'), nxt='Swipe →'),
    slide('quote', dict(h='That’s just how I am.', p='Or how you learned to be, so long ago it feels like you.')),
    slide('quote', dict(h='I’ll start on Monday.', p='Monday is where most changes go to wait.')),
    slide('quote', dict(h='It is what it is.', p='Usually said right before accepting something you shouldn’t.')),
    slide('quote', dict(tag='The spiritual one', h='Everything happens for a reason.', p='Comforting. Also a good way to never ask what the reason was.'), dark=True),
    slide('quote', dict(h='I’m fine.', p='The sentence most of us have practised the most.')),
    end('Which one do you say most?', 'Be honest in the comments.', 'Send it to the friend who says “I’m fine” the most.'),
]))

# 5. questions
qs = ['If nobody could ever see it, would you still want it?',
      'What are you waiting for permission to do?',
      'Who are you still trying to prove wrong?',
      'What do you keep calling “not the right time”?',
      'Which version of you are your friends still friends with?',
      'What would you stop tomorrow if nobody would be disappointed?',
      'If this year repeated forever, would you be okay?']
qslides = [f'<section class="s">{cover("Inner Compass 🧭", "7 questions you avoid asking yourself", "avoid", "Answer before you swipe →")}</section>']
for i, q in enumerate(qs, 1):
    d = dict(k=f'Question {i} / 7', h=q)
    if i == 1: d['p'] = 'Answer it in your head first.'
    if i == 6: d['tag'] = 'The one people skip'
    qslides.append(slide('question', d, dark=(i == 6), nxt='Swipe →' if i == 1 else '→'))
qslides.append(end('Which one did you skip?', 'Comment its number.', 'Send it to someone who’d answer #7 honestly.'))
C.append(('questions-you-avoid', 'violet', qslides))

# 6. interactive
C.append(('try-this-before-you-scroll', 'teal', [
    f'<section class="s">{cover("Inner Compass 🧭", "Try this before you scroll", "before", "It takes 40 seconds →")}</section>',
    slide('step', dict(k='Step 1 · 5 seconds', h='Unclench your jaw.', p='You didn’t know it was tight. Most people don’t.'), nxt='Swipe →'),
    slide('step', dict(k='Step 2 · 5 seconds', h='Drop your shoulders.', p='Further than that.')),
    slide('step', dict(k='Step 3 · 10 seconds', h='Take one breath slower than you need.', p='In through the nose. Out like a sigh.')),
    slide('step', dict(k='Step 4 · 15 seconds', h='Find three sounds you’d stopped hearing.', p='A fridge. Traffic. Your own breathing.')),
    slide('step', dict(k='Step 5 · the honest part', h='Notice how much you wanted to skip this.', p='That pull towards the next thing? That’s autopilot.'), dark=True),
    slide('step', dict(k='Done', h='You were actually here for 40 seconds.', p='Do it again tonight, before you pick up your phone.')),
    end('Did you actually do it?', 'Comment “done” if you did.', 'Send it to someone who needs 40 seconds today.'),
]))


# graphite sketch set for each carousel: sketches/<key>-NN.png, one per slide (see sketches.js)
SKETCHES = {'5-lies-about-waking-up': 'lies', 'what-we-call-it': 'call', 'body-noticed-first': 'body',
            'sentences-that-keep-you-asleep': 'sentences', 'questions-you-avoid': 'questions',
            'try-this-before-you-scroll': 'try'}


def with_sketch(section, key, i):
    path = f'sketches/{key}-{i:02d}.png'
    if not (HERE / path).exists():
        return section
    return section.replace('<section ', f'<section data-sketch="../{path}" ', 1)


def build():
    out = []
    for slug, theme, slides in C:
        t = THEMES[theme]
        vars_ = ';'.join(f'--{k}:{v}' for k, v in t.items())
        folder = HERE / f'{DATE}-{slug}'
        folder.mkdir(exist_ok=True)
        key = SKETCHES.get(slug)
        if key:
            slides = [with_sketch(s, key, i) for i, s in enumerate(slides, 1)]
        (folder / 'slides.html').write_text(
            f'<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}</style></head>'
            f'<body>{"".join(slides)}<script src="../sketches.js"></script></body></html>')
        out.append(folder)
    return out


if __name__ == '__main__':
    for f in build():
        print(f)
