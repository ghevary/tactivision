<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-6 font-sans">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4 mb-6 border-b border-slate-800 pb-4">
      <div>
        <div class="flex items-center gap-2">
          <span class="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider bg-sky-500/20 text-sky-400 border border-sky-500/30 rounded-full">
            TactiVision AI · Dataset v1.1.0 (Synthetic)
          </span>
          <span class="text-xs text-slate-400">Grounded AI + d3-delaunay Engine</span>
        </div>
        <h1 class="text-2xl font-bold tracking-tight mt-1">
          TactiVision AI <span class="text-sky-400 font-normal">| Spatial & Multi-Agent Sandbox</span>
        </h1>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button
          v-for="(preset, key) in tacticalPresets"
          :key="key"
          @click="applyPreset(key)"
          :class="[
            'px-3 py-1.5 text-xs font-semibold rounded-lg border transition',
            activePreset === key
              ? 'bg-sky-500 text-slate-950 border-sky-400 shadow-lg shadow-sky-500/20'
              : 'bg-slate-900 text-slate-300 border-slate-700 hover:border-slate-500'
          ]"
        >
          {{ preset.label }}
        </button>
        <button
          @click="toggleLiveSim"
          :class="[
            'px-3 py-1.5 text-xs font-bold rounded-lg border transition flex items-center gap-1.5',
            isSimulating
              ? 'bg-emerald-500 text-slate-950 border-emerald-400'
              : 'bg-slate-900 text-emerald-400 border-emerald-500/40 hover:bg-emerald-500/10'
          ]"
        >
          <span class="w-2 h-2 rounded-full" :class="isSimulating ? 'bg-slate-950 animate-ping' : 'bg-emerald-400'"></span>
          {{ isSimulating ? 'Pause Stream' : 'Live Sim Stream' }}
        </button>
      </div>
    </div>

    <div class="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-6">
      <div class="lg:col-span-8 bg-slate-900/90 border border-slate-800 rounded-2xl p-4 shadow-xl">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-3 text-xs">
          <div class="flex items-center gap-4">
            <label class="flex items-center gap-1.5 cursor-pointer select-none">
              <input type="checkbox" v-model="showVoronoi" class="accent-sky-400 rounded" />
              <span class="text-slate-300">Voronoi Pitch Control</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer select-none">
              <input type="checkbox" v-model="showPassingLanes" class="accent-sky-400 rounded" />
              <span class="text-slate-300">Open Passing Lanes</span>
            </label>
            <label class="flex items-center gap-1.5 cursor-pointer select-none">
              <input type="checkbox" v-model="showZone14" class="accent-amber-400 rounded" />
              <span class="text-amber-300">Zone 14 & Half-Spaces</span>
            </label>
          </div>
          <span class="text-slate-400 italic">Drag pin pemain untuk simulasi "What-If"</span>
        </div>

        <div class="relative w-full overflow-hidden rounded-xl border border-slate-700/80 bg-emerald-950">
          <canvas
            ref="pitchCanvas"
            width="840"
            height="544"
            class="w-full h-auto block cursor-grab active:cursor-grabbing"
            @mousedown="onMouseDown"
            @mousemove="onMouseMove"
            @mouseup="onMouseUp"
            @mouseleave="onMouseUp"
          ></canvas>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3">
            <div class="text-xs text-slate-400">Home Pitch Control</div>
            <div class="text-xl font-bold text-sky-400 mt-0.5">{{ metrics.skyControlPct }}%</div>
            <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
              <div class="bg-sky-400 h-full transition-all duration-150" :style="{ width: metrics.skyControlPct + '%' }"></div>
            </div>
          </div>
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3">
            <div class="text-xs text-slate-400">Zone 14 Dominance</div>
            <div class="text-xl font-bold text-amber-400 mt-0.5">{{ metrics.zone14Pct }}%</div>
            <div class="text-[11px] text-slate-500 mt-1">Area kunci depan penalti</div>
          </div>
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3">
            <div class="text-xs text-slate-400">Open Passing Lanes</div>
            <div class="text-xl font-bold text-emerald-400 mt-0.5">{{ metrics.openLanesCount }} Jalur</div>
            <div class="text-[11px] text-slate-500 mt-1">Dari pemegang bola</div>
          </div>
          <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3">
            <div class="text-xs text-slate-400">Expected Threat (xT)</div>
            <div class="text-xl font-bold text-purple-400 mt-0.5">{{ metrics.xTScore }}</div>
            <div class="text-[11px] text-slate-500 mt-1">Risiko Transisi: {{ metrics.transitionRisk }}</div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-4 flex flex-col gap-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4">
          <div class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
            Target Audience Persona
          </div>
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="p in ['Fan', 'Analyst', 'Broadcaster']"
              :key="p"
              @click="activePersona = p"
              :class="[
                'py-2 text-xs font-bold rounded-lg border transition',
                activePersona === p
                  ? 'bg-indigo-600 text-white border-indigo-400'
                  : 'bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700'
              ]"
            >
              {{ p }}
            </button>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 flex-1 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Multi-Agent Trace (Grounded AI)
              </span>
              <span class="text-[11px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Shared State Synced
              </span>
            </div>
            <div class="space-y-2.5 text-xs">
              <div class="p-3 rounded-xl bg-slate-950 border border-sky-500/30">
                <div class="font-bold text-sky-400 flex items-center justify-between">
                  <span>1. Spatial Telemetry Agent (MCP)</span>
                  <span>Active</span>
                </div>
                <p class="text-slate-300 mt-1 leading-relaxed">
                  Pemain terakhir digeser: <b>{{ lastMovedPlayerName }}</b>. Penguasaan Zone 14 berada di <b>{{ metrics.zone14Pct }}%</b> dengan <b>{{ metrics.openLanesCount }}</b> opsi umpan progresif terbuka.
                </p>
              </div>
              <div class="p-3 rounded-xl bg-slate-950 border border-amber-500/30">
                <div class="font-bold text-amber-400 flex items-center justify-between">
                  <span>2. Tactical & Risk Critic Agent</span>
                  <span>Verified</span>
                </div>
                <p class="text-slate-300 mt-1 leading-relaxed">
                  {{ tacticalCriticText }}
                </p>
              </div>
              <div class="p-3 rounded-xl bg-slate-950 border border-indigo-500/40">
                <div class="font-bold text-indigo-400 flex items-center justify-between">
                  <span>3. Narrative Producer ({{ activePersona }} Mode)</span>
                  <span>Live</span>
                </div>
                <p class="text-slate-200 mt-1.5 leading-relaxed italic">
                  "{{ personaNarrativeText }}"
                </p>
              </div>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-500 flex justify-between">
            <span>Coord System: 105m × 68m</span>
            <span>Engine: d3-delaunay + Grounded AI</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { Delaunay } from 'd3-delaunay'
import { analyzeTacticalShiftWithGemini } from '../services/geminiClient'

const PITCH_M_WIDTH = 105
const PITCH_M_HEIGHT = 68
const SCALE = 8

const pitchCanvas = ref(null)
const showVoronoi = ref(true)
const showPassingLanes = ref(true)
const showZone14 = ref(true)
const activePreset = ref('box_midfield')
const activePersona = ref('Analyst')
const isSimulating = ref(false)
const lastMovedPlayerName = ref('#5 J. Stones-Hybrid (Inverted Pivot)')
const lastInteractionId = ref(undefined)

let draggedPlayer = null
let simInterval = null

const players = reactive([
  { id: 'H1', num: 31, name: 'E. Moraes', team: 'sky', x: 14, y: 34 },
  { id: 'H2', num: 2, name: 'K. Walker-P', team: 'sky', x: 42, y: 52 },
  { id: 'H3', num: 3, name: 'R. Dias-S', team: 'sky', x: 38, y: 34 },
  { id: 'H4', num: 24, name: 'J. Gvardiol', team: 'sky', x: 42, y: 16 },
  { id: 'H5', num: 5, name: 'J. Stones-Hybrid', team: 'sky', x: 57, y: 26 },
  { id: 'H6', num: 16, name: 'R. Cascante', team: 'sky', x: 56, y: 41, hasBall: true },
  { id: 'H7', num: 17, name: 'K. Vandenberg', team: 'sky', x: 75, y: 45 },
  { id: 'H8', num: 47, name: 'P. Foden-W', team: 'sky', x: 74, y: 23 },
  { id: 'H9', num: 20, name: 'B. Mota-Silva', team: 'sky', x: 80, y: 61 },
  { id: 'H10', num: 11, name: 'J. Doku-M', team: 'sky', x: 80, y: 7 },
  { id: 'H11', num: 9, name: 'E. Braut-Vik', team: 'sky', x: 85, y: 34 },
  { id: 'A1', num: 24, name: 'A. Onana-N', team: 'red', x: 99, y: 34 },
  { id: 'A2', num: 20, name: 'D. Dalot', team: 'red', x: 86, y: 15 },
  { id: 'A3', num: 4, name: 'M. De Ligt', team: 'red', x: 87, y: 28 },
  { id: 'A4', num: 6, name: 'L. Martinez', team: 'red', x: 87, y: 40 },
  { id: 'A5', num: 3, name: 'N. Mazraoui', team: 'red', x: 86, y: 53 },
  { id: 'A6', num: 18, name: 'C. Casemiro', team: 'red', x: 76, y: 39 },
  { id: 'A7', num: 37, name: 'K. Mainoo', team: 'red', x: 75, y: 27 },
  { id: 'A8', num: 8, name: 'B. Fernandes', team: 'red', x: 65, y: 34 },
  { id: 'A9', num: 17, name: 'A. Garnacho', team: 'red', x: 70, y: 12 },
  { id: 'A10', num: 10, name: 'M. Rashford', team: 'red', x: 69, y: 56 },
  { id: 'A11', num: 9, name: 'R. Hojlund', team: 'red', x: 59, y: 31 }
])

const tacticalPresets = {
  box_midfield: {
    label: '3-2-4-1 Inverted Box',
    coords: { H5: [57, 26], H6: [56, 41], H7: [75, 45], H8: [74, 23], H2: [42, 52], H4: [42, 16] }
  },
  wide_overload: {
    label: '4-3-3 Wide Overload',
    coords: { H5: [40, 24], H6: [58, 34], H7: [71, 48], H8: [71, 20], H2: [68, 63], H4: [64, 8] }
  },
  all_out_press: {
    label: '2-3-5 High Press',
    coords: { H5: [65, 25], H6: [64, 42], H7: [81, 43], H8: [81, 25], H2: [65, 55], H4: [65, 13] }
  }
}

const metrics = reactive({
  skyControlPct: 58,
  zone14Pct: 54,
  openLanesCount: 4,
  xTScore: '0.78',
  transitionRisk: 'Low'
})

function applyPreset(key) {
  activePreset.value = key
  const map = tacticalPresets[key].coords
  players.forEach((p) => {
    if (map[p.id]) {
      p.x = map[p.id][0]
      p.y = map[p.id][1]
    }
  })
  renderPitch()
}

function isPassOpen(holder, target, opponents) {
  const dx = target.x - holder.x
  const dy = target.y - holder.y
  const lenSq = dx * dx + dy * dy
  if (lenSq === 0) return false
  for (const opp of opponents) {
    let t = ((opp.x - holder.x) * dx + (opp.y - holder.y) * dy) / lenSq
    t = Math.max(0.08, Math.min(0.92, t))
    const projX = holder.x + t * dx
    const projY = holder.y + t * dy
    const dist = Math.hypot(opp.x - projX, opp.y - projY)
    if (dist < 3.4) return false
  }
  return true
}

function calculateSpatialMetrics() {
  let skyCells = 0
  let totalCells = 0
  let z14Sky = 0
  let z14Total = 0
  for (let gx = 2; gx < PITCH_M_WIDTH; gx += 2.5) {
    for (let gy = 2; gy < PITCH_M_HEIGHT; gy += 2.5) {
      let minDist = Infinity
      let closestTeam = 'sky'
      for (const p of players) {
        const d = (p.x - gx) ** 2 + (p.y - gy) ** 2
        if (d < minDist) {
          minDist = d
          closestTeam = p.team
        }
      }
      totalCells++
      if (closestTeam === 'sky') skyCells++
      if (gx >= 70 && gx <= 88.5 && gy >= 20 && gy <= 48) {
        z14Total++
        if (closestTeam === 'sky') z14Sky++
      }
    }
  }
  metrics.skyControlPct = Math.round((skyCells / totalCells) * 100)
  metrics.zone14Pct = z14Total ? Math.round((z14Sky / z14Total) * 100) : 50
  const holder = players.find((p) => p.hasBall) || players[5]
  const teammates = players.filter((p) => p.team === 'sky' && p.id !== holder.id)
  const opponents = players.filter((p) => p.team === 'red')
  let openCount = 0
  teammates.forEach((tm) => {
    if (isPassOpen(holder, tm, opponents)) openCount++
  })
  metrics.openLanesCount = openCount
  const defendersBehindBall = players.filter((p) => p.team === 'sky' && p.x < 50).length
  metrics.transitionRisk = defendersBehindBall <= 3 ? 'High (Exposed)' : 'Controlled'
  metrics.xTScore = ((metrics.zone14Pct * 0.011) + (openCount * 0.045)).toFixed(2)
}

function renderPitch() {
  const canvas = pitchCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const W = canvas.width
  const H = canvas.height
  ctx.clearRect(0, 0, W, H)
  ctx.fillStyle = '#062c1e'
  ctx.fillRect(0, 0, W, H)

  if (showVoronoi.value) {
    const pts = players.map((p) => [p.x * SCALE, p.y * SCALE])
    const delaunay = Delaunay.from(pts)
    const voronoi = delaunay.voronoi([0, 0, W, H])
    players.forEach((p, i) => {
      ctx.beginPath()
      voronoi.renderCell(i, ctx)
      ctx.fillStyle = p.team === 'sky' ? 'rgba(56, 189, 248, 0.22)' : 'rgba(239, 68, 68, 0.20)'
      ctx.fill()
      ctx.strokeStyle = p.team === 'sky' ? 'rgba(56, 189, 248, 0.35)' : 'rgba(239, 68, 68, 0.30)'
      ctx.lineWidth = 1
      ctx.stroke()
    })
  }

  if (showZone14.value) {
    const zX = 70 * SCALE
    const zY = 20 * SCALE
    const zW = 18.5 * SCALE
    const zH = 28 * SCALE
    ctx.fillStyle = 'rgba(251, 191, 36, 0.16)'
    ctx.fillRect(zX, zY, zW, zH)
    ctx.strokeStyle = 'rgba(251, 191, 36, 0.8)'
    ctx.setLineDash([5, 4])
    ctx.lineWidth = 1.5
    ctx.strokeRect(zX, zY, zW, zH)
    ctx.setLineDash([])
    ctx.fillStyle = '#fbbf24'
    ctx.font = 'bold 10px sans-serif'
    ctx.fillText('ZONE 14 (GOLDEN POCKET)', zX + 8, zY + 14)
  }

  ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)'
  ctx.lineWidth = 1.5
  ctx.strokeRect(4, 4, W - 8, H - 8)
  ctx.beginPath()
  ctx.moveTo(W / 2, 4)
  ctx.lineTo(W / 2, H - 4)
  ctx.stroke()
  ctx.beginPath()
  ctx.arc(W / 2, H / 2, 9.15 * SCALE, 0, Math.PI * 2)
  ctx.stroke()
  const penW = 16.5 * SCALE
  const penH = 40.3 * SCALE
  const penY = (H - penH) / 2
  ctx.strokeRect(4, penY, penW, penH)
  ctx.strokeRect(W - 4 - penW, penY, penW, penH)

  const holder = players.find((p) => p.hasBall) || players[5]
  const opponents = players.filter((p) => p.team === 'red')
  if (showPassingLanes.value && holder) {
    players
      .filter((p) => p.team === 'sky' && p.id !== holder.id)
      .forEach((tm) => {
        const open = isPassOpen(holder, tm, opponents)
        const dist = Math.hypot(tm.x - holder.x, tm.y - holder.y)
        if (dist < 38) {
          ctx.beginPath()
          ctx.moveTo(holder.x * SCALE, holder.y * SCALE)
          ctx.lineTo(tm.x * SCALE, tm.y * SCALE)
          if (open) {
            ctx.strokeStyle = 'rgba(52, 211, 153, 0.85)'
            ctx.lineWidth = 2
            ctx.setLineDash([6, 4])
          } else {
            ctx.strokeStyle = 'rgba(248, 113, 113, 0.28)'
            ctx.lineWidth = 1
            ctx.setLineDash([2, 4])
          }
          ctx.stroke()
          ctx.setLineDash([])
        }
      })
  }

  players.forEach((p) => {
    const px = p.x * SCALE
    const py = p.y * SCALE
    if (p.hasBall) {
      ctx.beginPath()
      ctx.arc(px, py, 16, 0, Math.PI * 2)
      ctx.strokeStyle = '#38bdf8'
      ctx.lineWidth = 2
      ctx.stroke()
    }
    ctx.beginPath()
    ctx.arc(px, py, 11, 0, Math.PI * 2)
    ctx.fillStyle = p.team === 'sky' ? '#38bdf8' : '#ef4444'
    ctx.fill()
    ctx.strokeStyle = '#0f172a'
    ctx.lineWidth = 2
    ctx.stroke()
    ctx.fillStyle = p.team === 'sky' ? '#020617' : '#ffffff'
    ctx.font = 'bold 10px sans-serif'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(p.num, px, py)
  })

  calculateSpatialMetrics()
}

function getMouseMeters(evt) {
  const rect = pitchCanvas.value.getBoundingClientRect()
  const scaleX = pitchCanvas.value.width / rect.width
  const scaleY = pitchCanvas.value.height / rect.height
  const mx = ((evt.clientX - rect.left) * scaleX) / SCALE
  const my = ((evt.clientY - rect.top) * scaleY) / SCALE
  return { mx, my }
}

function onMouseDown(evt) {
  const { mx, my } = getMouseMeters(evt)
  for (const p of players) {
    if (Math.hypot(p.x - mx, p.y - my) < 2.2) {
      draggedPlayer = p
      lastMovedPlayerName.value = `#${p.num} ${p.name}`
      break
    }
  }
}

function onMouseMove(evt) {
  if (!draggedPlayer) return
  const { mx, my } = getMouseMeters(evt)
  draggedPlayer.x = Math.max(2, Math.min(PITCH_M_WIDTH - 2, mx))
  draggedPlayer.y = Math.max(2, Math.min(PITCH_M_HEIGHT - 2, my))
  renderPitch()
}

async function onMouseUp() {
  if (!draggedPlayer) return
  const movedPlayer = draggedPlayer
  draggedPlayer = null

  const payload = {
    moved_player: { id: movedPlayer.id, name: movedPlayer.name, new_x: movedPlayer.x, new_y: movedPlayer.y },
    spatial_metrics: {
      sky_pitch_control_pct: metrics.skyControlPct,
      zone14_dominance_pct: metrics.zone14Pct,
      open_passing_lanes: metrics.openLanesCount,
      expected_threat_xt: metrics.xTScore,
      transition_risk: metrics.transitionRisk
    },
    persona: activePersona.value,
    previousInteractionId: lastInteractionId.value
  }

  try {
    const res = await fetch('/api/v1/agents/analyze-tactical-shift', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      const data = await res.json()
      lastInteractionId.value = data.interaction_id
    }
  } catch (_) {
    // Fallback ke reaktivitas lokal bila endpoint belum aktif
  }
}

function toggleLiveSim() {
  isSimulating.value = !isSimulating.value
  if (isSimulating.value) {
    simInterval = setInterval(() => {
      players.forEach((p) => {
        if (p !== draggedPlayer) {
          p.x = Math.max(3, Math.min(102, p.x + (Math.random() - 0.48) * 0.6))
          p.y = Math.max(3, Math.min(65, p.y + (Math.random() - 0.5) * 0.6))
        }
      })
      renderPitch()
    }, 80)
  } else {
    clearInterval(simInterval)
  }
}

const tacticalCriticText = computed(() => {
  if (metrics.zone14Pct >= 60) {
    return `Overload sukses di Zone 14 (${metrics.zone14Pct}%). Pertahanan blok rendah lawan tertarik ke dalam, namun perhatikan risiko transisi (${metrics.transitionRisk}).`
  }
  return `Struktur blok tengah lawan masih rapat. Naikkan Inverted Fullback (#5) ke half-space untuk menambah opsi umpan dari #16.`
})

const personaNarrativeText = computed(() => {
  if (activePersona.value === 'Fan') {
    return `Tim menyerang mengurung pertahanan lawan! Dengan menggeser ${lastMovedPlayerName.value}, celah di depan kotak penalti terbuka lebar dengan ${metrics.openLanesCount} jalur umpan siap dieksekusi.`
  }
  if (activePersona.value === 'Broadcaster') {
    return `[CUE LIVE] Perhatikan bagaimana ${lastMovedPlayerName.value} masuk ke kantong ruang Zone 14—penguasaan ruang melonjak ke ${metrics.zone14Pct}% dan xT menyentuh ${metrics.xTScore}!`
  }
  return `Konfigurasi spasial menghasilkan ${metrics.skyControlPct}% pitch control dan ${metrics.zone14Pct}% dominasi Zone 14. Nilai Expected Threat (xT) berada pada ${metrics.xTScore} dengan status rest-defense ${metrics.transitionRisk}.`
})

watch([showVoronoi, showPassingLanes, showZone14], () => renderPitch())
onMounted(() => renderPitch())
onUnmounted(() => { if (simInterval) clearInterval(simInterval) })
</script>
