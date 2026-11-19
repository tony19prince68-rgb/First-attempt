import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Status } from '../types'

const status = atom({ plugin: 'prompt-master', key: 'status' } as const, 'idle' as Status)
// The draft as it was before the last rewrite, so one click can undo it.
const original = atom({ plugin: 'prompt-master', key: 'original' } as const, null as string | null)

const SYSTEM = `You are Prompt Master. You rewrite a user's rough, hastily typed prompt for an AI coding and writing assistant into a better prompt.

Rules:
- Keep the user's intent, facts, names, file paths, code and constraints exactly. Never invent requirements, files or details they did not give.
- Fix spelling and grammar; make it clear, specific and unambiguous.
- State the goal first, then relevant context, then concrete requirements or steps, then the expected output or definition of done, when the draft supports them.
- Use short bullet points only when there are several distinct requirements; keep a simple ask as one or two sentences.
- Write in the user's voice ("I want...", "Please..."), in the draft's language.
- Do not answer the prompt. Output ONLY the rewritten prompt: no preamble, no quotes, no commentary.`

async function rewrite($: EngineInterface, given?: string) {
  if ((await read($, status)) === 'working') return
  const box = await $.prompt.read()
  const source = given?.trim() ? given : box.text
  const draft = source.trim()
  if (!draft) {
    $.ui.toast('Prompt Master: type a rough prompt first')
    return
  }
  await update($, status, () => 'working')
  try {
    const r = await $.model.complete({
      model: 'sonnet',
      system: SYSTEM,
      prompt: `Rewrite this draft prompt:\n\n<draft>\n${draft}\n</draft>`,
      maxTokens: 2048,
      effort: 'low',
      timeoutMs: 60000,
    })
    if (!r.isAnswered || !r.text.trim()) {
      $.ui.toast('Prompt Master: rewrite failed, your draft is unchanged')
      return
    }
    const better = r.text.trim().replace(/^<draft>\s*|\s*<\/draft>$/g, '')
    const filled = await $.prompt.fill({ text: better, mode: 'replace' })
    if (filled.isFilled) {
      await update($, original, () => source)
      $.ui.toast('Prompt Master: draft rewritten. Review it, then send')
    }
  } finally {
    await update($, status, () => 'idle')
  }
}

async function undo($: EngineInterface) {
  const before = await read($, original)
  if (before === null) return
  await $.prompt.fill({ text: before, mode: 'replace' })
  await update($, original, () => null)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'prompt-master',
      description: 'Rewrite the prompt draft into a clearer, better prompt',
    })
    return next(e)
  })

  // /prompt-master <rough prompt>: the rewrite lands in the prompt box.
  on('command.run', { command: 'prompt-master' }, async ($, e) => {
    void rewrite($, e.args)
    return { text: 'Prompt Master is rewriting your draft.' }
  })

  // Sending the prompt drops the undo.
  on('prompt.submit', async ($, e, next) => {
    await update($, original, () => null).catch(() => {})
    return next(e)
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    const isWorking = (await read($, status)) === 'working'
    const canUndo = (await read($, original)) !== null

    return (
      <Box flexDirection="row" gap={1}>
        <Button
          key="rewrite"
          label={isWorking ? 'Prompt Master: rewriting...' : '✨ Prompt Master'}
          onPress={() => void rewrite($)}
        />
        {canUndo && !isWorking && (
          <Button key="undo" label="Undo rewrite" onPress={() => void undo($)} />
        )}
        {!canUndo && !isWorking && <Text dimColor>rewrite your draft before sending</Text>}
      </Box>
    )
  })
}
