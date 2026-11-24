// Adds a graphite pencil sketch to each slide that names one (<section data-sketch="...">).
// The text is never moved or restyled. The script measures every line of text on the slide,
// finds the largest empty square (allowing a little bleed off the right and bottom edges),
// avoids the strip TikTok covers with its caption, and puts the sketch there, behind the
// text (z-index -1 inside an isolated slide), blended into the slide colour.
(function () {
  const css = `
    section[data-sketch] { isolation: isolate }
    .sketch { position: absolute; z-index: -1; pointer-events: none;
      mix-blend-mode: multiply; filter: grayscale(1) contrast(1.5) brightness(1.12);
      -webkit-mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent), linear-gradient(transparent, #000 5%, #000 95%, transparent);
      -webkit-mask-composite: source-in; mask-composite: intersect }
    .dark .sketch { mix-blend-mode: screen; filter: grayscale(1) contrast(1.5) brightness(1.12) invert(1); opacity: .9 }
    .end .sketch, .violet .sketch { opacity: .8 }`
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st)

  const W = 1080, H = 1920, C = 10                // grid cell in px
  const PAD = 26                                  // clear space kept around every line of text
  const BLEED_R = 120, BLEED_B = 260              // how far a sketch may run off the right / bottom edge
  const TOP = 170                                 // keep clear of TikTok's top tabs
  const CAPTION_Y = 1560                          // below this, TikTok's caption covers the left side
  const MAX = 900, CAP_PENALTY = .3

  function textRects(sec) {
    const out = [], r0 = sec.getBoundingClientRect()
    const walker = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT)
    while (walker.nextNode()) {
      const n = walker.currentNode
      if (!n.textContent.trim() || n.parentElement.closest('.sketch, .qmark')) continue
      const rg = document.createRange(); rg.selectNodeContents(n)
      for (const r of rg.getClientRects()) out.push({ x0: r.left - r0.left, y0: r.top - r0.top, x1: r.right - r0.left, y1: r.bottom - r0.top })
    }
    for (const el of sec.querySelectorAll('.pill')) {           // pill backgrounds count as text
      const r = el.getBoundingClientRect(); out.push({ x0: r.left - r0.left, y0: r.top - r0.top, x1: r.right - r0.left, y1: r.bottom - r0.top })
    }
    return out
  }

  function place(sec) {
    const cols = Math.ceil((W + BLEED_R) / C), rows = Math.ceil((H + BLEED_B) / C)
    const busy = new Uint8Array(cols * rows)
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (r * C < TOP) busy[r * cols + c] = 1
    for (const t of textRects(sec)) {
      const c0 = Math.max(0, Math.floor((t.x0 - PAD) / C)), c1 = Math.min(cols - 1, Math.ceil((t.x1 + PAD) / C))
      const r0 = Math.max(0, Math.floor((t.y0 - PAD) / C)), r1 = Math.min(rows - 1, Math.ceil((t.y1 + PAD) / C))
      for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) busy[r * cols + c] = 1
    }
    // prefix sums of busy cells, so any rectangle can be tested in O(1)
    const P = new Uint32Array((cols + 1) * (rows + 1)), pw = cols + 1
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++)
      P[(r + 1) * pw + c + 1] = busy[r * cols + c] + P[r * pw + c + 1] + P[(r + 1) * pw + c] - P[r * pw + c]
    const free = (c0, r0, cw, rh) => P[(r0 + rh) * pw + c0 + cw] - P[r0 * pw + c0 + cw] - P[(r0 + rh) * pw + c0] + P[r0 * pw + c0] === 0
    const img = sec.querySelector(':scope > img.sketch'), aspect = img.naturalWidth / img.naturalHeight
    let best = null
    for (let hC = Math.floor(Math.min(MAX / aspect, MAX) / C); hC >= 22; hC -= 2) {
      const wC = Math.round(hC * aspect)
      if (wC > cols || hC > rows) continue
      for (let r = 0; r + hC <= rows; r += 2) for (let c = 0; c + wC <= cols; c += 2) {
        if (!free(c, r, wC, hC)) continue
        const x = c * C, y = r * C, w = wC * C, h = hC * C
        const vx = Math.max(0, Math.min(x + w, W) - Math.max(x, 0)), vy = Math.max(0, Math.min(y + h, H) - Math.max(y, 0))
        let seen = vx * vy
        const capTop = Math.max(y, CAPTION_Y), capBot = Math.min(y + h, H)
        if (capBot > capTop) seen -= CAP_PENALTY * vx * (capBot - capTop)
        if (y + h > H) seen -= .5 * (y + h - H) * vx        // cropped off the bottom
        if (x + w > W) seen -= .5 * (x + w - W) * vy        // cropped off the right
        if (!best || seen > best.seen) best = { x, y, w, h, seen }
      }
      if (best && best.h > hC * C * 1.6) break             // much smaller sizes can't win any more
    }
    if (!best) return
    Object.assign(img.style, { left: best.x + 'px', top: best.y + 'px', width: best.w + 'px', height: best.h + 'px' })
  }

  const secs = [...document.querySelectorAll('section[data-sketch]')]
  const loads = secs.map(sec => {
    const img = new Image(); img.className = 'sketch'; img.alt = ''
    img.src = sec.dataset.sketch; sec.prepend(img)
    return img.decode().catch(() => {})
  })
  window.__placed = Promise.all([document.fonts.ready, ...loads]).then(() => secs.forEach(place))
})()
