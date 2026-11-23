# Dil Se Hindi: design system ("Gulal")

This is the design as built in `index.html`. Product truths live in `PRODUCT.md`; the direction that was chosen is in `design/direction-contract.md`.

## Theme: Gulal

Gulal is the coloured powder thrown at Holi. The app is an iOS shell coloured by that powder. Every phrase you learn adds a dot of pigment to a rangoli you are making for her, and each screen takes the pigment of the stage you are in.

- Mood: joyful but calm. In the evening it is deep indigo with bright pigment. In the day it is moonstone white with powder in the corners.
- Signature: the rangoli. Your vocabulary is drawn as rings of dots around a medallion that holds your newest word.
- Progress is drawn as dots: the rangoli, daily goal, lesson dots on Journey beads, level dots, the week chart. The one exception is the thin progress bar inside a lesson, which is a native task control.

### Pigments

| Pigment | Role | Light | Dark | Text-safe (light / dark) | Ink on it (light / dark) |
|---|---|---|---|---|---|
| rani (pink) | Stage 1, brand action | `#E0157A` | `#FF4FA0` | `#B80F63` / `#FF7AB8` | white / `#14102B` |
| kesari (saffron) | Stage 2, gyms | `#FF8B1F` | `#FFA040` | `#A65200` / `#FFB46B` | `#14102B` / `#14102B` |
| mor (peacock) | Stage 3, Talk, memory | `#10A5A8` | `#2ED3C9` | `#047A7D` / `#5EE3DA` | `#14102B` / `#14102B` |
| neel (indigo) | Stage 4, Me | `#5546E8` | `#8E82FF` | `#3F31C9` / `#ADA4FF` | white / `#14102B` |
| haldi (turmeric) | Stage 5 | `#FFC62E` | `#FFD35C` | `#8A6100` / `#FFDD85` | `#14102B` / `#14102B` |
| jamuni (violet) | Reading Devanagari track, your saved words | `#8F2FD6` | `#C17BFF` | `#7322B5` / `#D3A1FF` | white / `#14102B` |
| hara (green) | Right answers only | `#2FA85A` | `#4FD483` | `#1C7A3F` / `#7BE3A3` | `#14102B` / `#14102B` |
| laal (red) | Wrong answers only | `#E23B3B` | `#FF6B6B` | `#C42B2B` / `#FF8F8F` | white / `#14102B` |

The `--on-<pigment>` tokens hold the "ink on it" column. Any text or icon placed on a raw pigment uses them, which keeps every pairing at WCAG AA. Buttons for right and wrong answers use `--good-btn` and `--bad-btn`, which are deeper than the raw pigments in light mode.

### Grounds and neutrals

| Token | Light | Dark | Use |
|---|---|---|---|
| `--ground` | `#F7F5FB` moonstone | `#15102E` night indigo | page background |
| `--surface` | `#FFFFFF` | `#201A42` | lists, cards, sheets content |
| `--surface-2` | `#F0EDF7` | `#2A2352` | inset boxes (notes, facts) |
| `--ink` | `#1A1433` | `#F5F2FF` | text |
| `--ink-2` | `#5B5573` | `#BDB6DB` | secondary text (AA on every surface) |
| `--ink-3` | `#7E789A` | `#958EB8` | chevrons, lock icons, never body text |
| `--act` | `#D0106F` | `#D9187A` | primary buttons |
| `--glass` | `rgba(249,248,253,.74)` | `rgba(27,21,58,.70)` | system chrome only: tab bar, compact bar, dock, toast, talk bar |

The neutrals all lean toward indigo, so the greys feel like part of the night ground rather than a default.

## Type

- Display: **Eczar** (Google Fonts, 500 to 800). It covers both Latin and Devanagari, so Hindi and English headings share one voice. Used for large titles, the Hindi greeting, stage names, every Hindi word (`.deva`), verdicts and the praise word on results.
- Text: the system UI face (SF Pro on iPhone). On Apple devices `html` uses `font: -apple-system-body`, so all rem sizes follow the reader's Dynamic Type setting.
- Fallbacks: Kohinoor Devanagari and Noto Sans Devanagari for Hindi, Georgia for Latin display.
- Scale: greeting 2.35rem/700, large title 2.1rem/700, stage title 1.6rem, question word clamp(2.4rem, 11vw, 3.4rem), body 1rem, secondary 0.85 to 0.94rem, tab labels 0.62rem.
- Hindi is marked `lang="hi"` at render time so VoiceOver reads it with a Hindi voice.

## Layout: the iOS shell

- Large title at the top of each tab. It collapses into a compact title in a sticky glass bar once you scroll. Pushed screens (Your memory, Story, Talk) get a back button with the parent's name.
- A floating glass tab bar: Today, Journey, Practice, Words, Me. A tinted lens slides between tabs. Today carries a badge with the number of phrases due.
- Each top-level screen opens with one **powder field**: a rounded panel (radius 26) in its pigment, with four radial powder clouds in its corners. Quiet native rows sit below it on the ground. The Today and Your memory fields take the pigment of the stage you are in, so the home screen changes colour as you progress.
- Practice opens with Talk where Claude is available (inside claude.ai). In the home-screen app it opens with your next story instead, and Talk becomes a row that opens Dil Se in Claude.
- Gold (haldi) marks goals reached; green and red are kept for right and wrong answers only.
- Sheets rise from the bottom for focused tasks (unit details, confirmations).
- Lessons are a full-screen cover: a close button, a progress bar and a streak counter on top, a **deck** of question cards with two card edges stacked under the current card, and a glass dock with the action.
- Gutters use `max(16px, env(safe-area-inset-*))`. The claude.ai wrapper pads the top and bottom by the safe-area insets; the home-screen build adds the same padding itself.

## Components

| Component | Notes |
|---|---|
| Rangoli (`rangoliSVG`) | One dot per speaking phrase (up to 640) in alternating rings around a scalloped circle. A learned dot takes its unit's pigment and grows with strength (box 1 to 5). Unlearned dots are hairline circles. On Your memory, due dots get an ink outline. |
| Medallion | The centre of the rangoli. It shows your newest word, or a word of the day. Tap it to hear the word. |
| Deck card | The next lesson as a pigment card with two stacked edges below it. |
| Bead thread | Journey units as beads on a dotted thread, each bead with three lesson dots. Conversation scenes sit on the thread as chat beads. |
| Dots meter | Daily goal (10 dots), level progress (20 dots), stage completion, strength rows. |
| List rows | 58px rows with a pigment icon tile, a title, a subtitle and a chevron. |
| Question card | The deck card in a lesson: a prompt, the Hindi word in Eczar, speaker and slow (tortoise) buttons, romanization that fades as a word gets strong. |
| Options | Numbered 58px rows (keys 1 to 4 work). Right turns hara, wrong turns laal. |
| Verdict dock | Glass dock tinted green or red, with an Eczar verdict ("Shaabaash!", "Not quite"), the answer, and Continue. |
| Result | A pigment field with a rangoli ornament behind the praise word (शाबाश, बहुत बढ़िया, अभ्यास), an XP count, medals, and Continue at the foot. |
| Icons | One authored SVG set on a 24px grid with a 1.9 stroke. There are no emoji or text glyphs used as icons. |

## Motion

GSAP 3.12.5 (cdnjs). Every animation goes through `G()`, which returns nothing when Reduce Motion is on, so the app is fully static and complete without motion.

- Signature, the rangoli bloom: after a lesson or review, Continue returns to Today. The dots you just earned are thrown in from the edges like powder, settle into the pattern, send out a small ripple, and the medallion takes your newest word.
- First load: the rangoli dots settle from a visible, smaller state and the scalloped ring turns slightly into place. The first frame is always complete.
- Deck: answering lifts the next card in. Continue slides the top card away to the left. A second tap during that exit is ignored, and so is a tap on Continue within 0.4 s of the verdict, so a double tap on Check never skips the feedback. The new card animates opacity only, so it keeps VoiceOver focus.
- Right answer: a small burst of pigment powder (canvas) from the verdict and a soft bell (WebAudio, "Bell sound" switch in Me).
- Wrong answer: the card gives a short elastic shake.
- Navigation: pushed screens slide in from the right and back out; tab switches change instantly, as on iOS, while the tab lens slides.
- Easing is exponential ease-out over 0.3 to 0.6 s, with up to 1.2 s for the bloom.

## Accessibility

- Automated check (axe-core, WCAG 2.1 A and AA) on 17 screens in both themes: no violations. No horizontal overflow at 320 and 375 px.
- Text and icons on pigments use the `--on-*` tokens. Locked medals and secondary text use `--ink-2`.
- Compact controls (chips, small round buttons, close buttons) keep their drawn size but get an invisible 44pt tap area.
- Visible focus ring, keyboard support in lessons (1 to 4, Enter), Escape closes sheets, live-region announcements for right and wrong answers and for toasts.
- Focus goes back to whatever opened a sheet when it closes. Each new lesson card takes focus so VoiceOver reads the question. Revealed English and romanization lose their "Reveal" label so they are read as themselves.
- Every text field is at least 16px, so iOS never zooms the page when you type.

## App icon: "Gulal Medallion"

Design philosophy: powder thrown in joy settles into order. The icon is a rangoli seen from above at night. Four rings of pigment dots (haldi, kesari, rani, neel, from the inside out) close around a white medallion that holds one word, दिल ("heart"), in Eczar. Holi powder drifts in from the corners: rani at top left, kesari at top right, mor at bottom right, neel at bottom left. The icon uses no gradients on the dots and no outline effects, so it reads at 60 px on a home screen. The source is `design/app-icon.svg`. The PNG sizes, including a maskable variant inside the 80% safe circle, are in `pwa/icons/`.

## Deliberate exceptions

- Field radius is 26 and the question card is 24. These are large stage surfaces, not cards, and follow iOS's larger container radii. Lists and rows use 16.
- The lesson progress bar is a bar. It is a native task control, so platform convention wins over the "dots, never bars" rule.

## Files

- `index.html`: the app. It is the claude.ai artifact and the source for everything else.
- `build_pwa.py`: wraps `index.html` into the iPhone home-screen app in `pwa/` (manifest, offline service worker, icons, standalone metadata).
- `design/direction-contract.md`: the direction that was locked before building.
