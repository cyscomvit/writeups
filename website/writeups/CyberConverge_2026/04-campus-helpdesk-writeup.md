---
layout: writeup

title: Campus Helpdesk
difficulty: Easy
points: 20
categories: [Web]
tags: []

flag: CYS{campus_helpdesk_7f29c1a8}
---

### Campus Helpdesk

* Author: Dibyadipan (0DayMonxrch)

This is a web-based CTF challenge involving **Stored Cross-Site Scripting (XSS)**.

First, submit a normal ticket and test whether HTML is interpreted in the ticket description:

```html
<b>test</b>
```

The text is rendered as HTML, indicating that the description is not safely escaped.

Next, confirm JavaScript execution:

```html
<script>alert(location.origin)</script>
```

The alert shows the challenge origin, confirming that JavaScript executes in the context of the helpdesk application.

Inspecting the ticket HTML reveals a hidden internal endpoint:

```text
data-review-endpoint="/api/internal/note"
```

The endpoint relies on the browser's existing `review_session` cookie. Although the cookie is `HttpOnly` and cannot be read using `document.cookie`, the browser automatically includes it in same-origin requests.

We can therefore use the stored XSS to make an authenticated request:

```html
<script>
fetch('/api/internal/note', {method: 'POST'})
    .then(r => r.text())
    .then(flag => document.body.innerText = flag);
</script>
```

Opening the ticket again executes the payload, makes the authenticated request, and displays the flag.

