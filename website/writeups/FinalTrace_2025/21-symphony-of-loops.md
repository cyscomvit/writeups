---
layout: writeup

title: Symphony of Loops
difficulty: Medium
points: 500
categories: [Musical Cipher]
tags: []

flag: CYS{K3V1N_DUR4NT_M1DD13_G4M3}
---

## Symphony of Loops

- **Category**: Musical Cipher
- **Author**: Aadhyanth

## Challenge Description

The Bard's Enigma: Symphony of Loops

Attend, O seeker of hidden verse! Before thee resonates a spectral melody, an artifact known only as the "Symphony of Loops." Legend tells of a mad court composer, Elmsworth, who claimed to have transcribed the very song of the Aether – a haunting refrain caught in an endless, maddening cycle.

Dismissed as a lunatic, Elmsworth vanished, leaving behind only this enchanted score, captured not on parchment, but within this peculiar digital phial (a MIDI file, they call it in lesser realms). It is said that Elmsworth encoded his final, defiant truth within the music itself, believing only a mind attuned to both harmony and cipher could unravel it.

Listen closely to the repeating bars. Observe the dance of the notes upon the unseen staff. Within this loop, each key press, each rise and fall in tone, is no mere sound – it is a symbol, a letter in a forgotten alphabet where music itself forms the words.

Thy task is to break the cycle, to listen beyond the melody and perceive the message woven into its very structure. Decipher the notes, translate their hidden meaning, and reveal the secret Elmsworth entrusted to his looping symphony. But take heed – madness oft lies within such endless refrains.

Make sure to wrap thy message in CYS{...}

### Tools Used

- MIDI file viewer
- A notebook and pen

### Step-by-Step Solution

#### Step 1:

Open the .mid file with any midi file viewer (ex. https://signalmidi.app/edit)

#### Step 2:

Note down the sequence of piano keys from the viewer in the correct order
D#6, D#4, D7, C#4, F#6, B7, G#5, C#7, A#6, E4, F#6, C7, B7, F6, C#4, G#5, G#5, C#4, D#4, B7, B5, E4, F6, D#4 is the obtained sequence

#### Step 3:

The keys are numbered from a transpose of the standard MIDI indexing system.
Instead of assigning the value of 60 to C4, the value of 0 has been assigned to C0. (This is apparent from the repeating B7 keys, which can be inferred to be underscores)
The number of each key represents an ASCII value.

### Flag

```
CYS{K3V1N_DUR4NT_M1DD13_G4M3}
```
