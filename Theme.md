# LexGuard Design System v1.0

> **Theme:** Authoritative • Secure • Legal • Professional • Trustworthy

---

# Brand Concept

**LexGuard** represents authority, integrity, and security — built for a Secure Digital Document Management System for Legal & Investigation Documents. The interface should feel like a serious, government-grade product: trustworthy, precise, and confident, not a flashy AI startup.

---

# Color Palette

## Primary Colors

| Role | Color | Hex |
|------|------|------|
| Primary (Deep Navy) | 🔵 | `#0F1E3D` |
| Primary Hover | 🔵 | `#0A1530` |
| Primary Light | 🔵 | `#2E4270` |
| Secondary (Gold/Brass) | 🟡 | `#C9A227` |
| Secondary Hover | 🟡 | `#A9860F` |
| Accent (Steel Teal) | 🟢 | `#0E7C86` |
| Accent Hover | 🟢 | `#0A5F67` |

---

## Semantic Colors

| Purpose | Hex |
|----------|-----|
| Success (Verified) | `#16A34A` |
| Warning (Pending) | `#D97706` |
| Error (Tamper Alert) | `#DC2626` |
| Info | `#2563EB` |

---

# Background Colors

| Element | Hex |
|----------|-----|
| Background | `#0A0F1C` |
| Surface | `#111A2C` |
| Card | `#16202E` |
| Elevated Card | `#1C2A3D` |
| Sidebar | `#0D1524` |
| Navbar | `rgba(10,15,28,0.85)` |

---

# Text Colors

| Type | Hex |
|------|-----|
| Primary Text | `#F1F5F9` |
| Secondary Text | `#94A3B8` |
| Muted Text | `#64748B` |
| Disabled Text | `#475569` |

---

# Borders

| Type | Value |
|------|-------|
| Primary Border | `#26324A` |
| Light Border | `rgba(255,255,255,0.08)` |
| Focus Border | `#0E7C86` |

---

# Gradients

## Header/Hero Gradient (use sparingly — one place only)

```css
linear-gradient(
 135deg,
 #0F1E3D 0%,
 #0E7C86 100%
);
```

## Verified Badge Gradient

```css
linear-gradient(
135deg,
#16A34A,
#0E7C86
);
```

## Tamper Alert Gradient

```css
linear-gradient(
135deg,
#DC2626,
#7A1313
);
```

> Note: Unlike typical AI-product UIs, LexGuard avoids heavy gradient use across the interface. Gradients are reserved only for the header and status badges — everything else stays flat for a serious, professional feel.

---

# Buttons

## Primary Button

| Property | Value |
|-----------|-------|
| Background | `#0F1E3D` |
| Hover | `#0A1530` |
| Text | `#F1F5F9` |

## Secondary Button (Gold — for key legal actions)

| Property | Value |
|-----------|-------|
| Background | Transparent |
| Border | `#C9A227` |
| Text | `#C9A227` |
| Hover Background | `rgba(201,162,39,0.12)` |

## Verify Button (Teal)

| Property | Value |
|-----------|-------|
| Background | `#0E7C86` |
| Hover | `#0A5F67` |
| Text | `#FFFFFF` |

## Danger Button (Tamper/Delete)

`#DC2626`

## Success Button (Approve/Confirm)

`#16A34A`

---

# Input Fields

| Property | Value |
|-----------|-------|
| Background | `#111A2C` |
| Border | `#26324A` |
| Focus Border | `#0E7C86` |
| Placeholder | `#64748B` |
| Text | `#F1F5F9` |

---

# Document Status Badge Colors

| Status | Color |
|------------|-------|
| Verified / Authentic | `#16A34A` |
| Tampered / Alert | `#DC2626` |
| Pending Review | `#D97706` |
| Processing (OCR/AI) | `#2563EB` |
| Archived | `#64748B` |

---

# Role Badge Colors

| Role | Color |
|------|-------|
| Admin | `#C9A227` |
| Investigation Officer | `#2563EB` |
| Legal Officer | `#0E7C86` |
| Viewer | `#64748B` |

---

# Typography

| Usage | Font |
|-------|------|
| Logo | Sora |
| Headings | Sora |
| Body | Inter |
| Hash / Blockchain / Code | JetBrains Mono |

---

# Border Radius

| Component | Radius |
|-----------|--------|
| Small | 6px |
| Medium | 10px |
| Large | 14px |
| Cards | 16px |
| Buttons | 8px |

> Kept intentionally less rounded than typical AI-product UIs (no 24px pill cards) — sharper corners reinforce a formal, government-grade feel.

---

# Spacing System

```text
4px
8px
12px
16px
24px
32px
48px
64px
96px
```

---

# Shadows

## Small

```css
0 2px 8px rgba(0,0,0,0.20)
```

## Medium

```css
0 8px 24px rgba(0,0,0,0.30)
```

## Large

```css
0 16px 48px rgba(0,0,0,0.40)
```

## Verified Glow

```css
0 0 20px rgba(22,163,74,0.25)
```

## Tamper Alert Glow

```css
0 0 20px rgba(220,38,38,0.30)
```

---

# Motion

| Animation | Value |
|------------|-------|
| Transition | `200ms ease` |
| Card Hover | `translateY(-3px)` |
| Button Hover | `scale(1.02)` |
| Alert Pulse (Tamper Detected) | `pulse 1.2s ease-in-out infinite` |

> Motion kept minimal and functional — no decorative animation. The only expressive motion is the tamper-alert pulse, which is a deliberate security cue, not decoration.

---

# Document Card Design

| Property | Value |
|-----------|-------|
| Background | `#16202E` |
| Border | `rgba(255,255,255,0.08)` |
| Radius | `16px` |
| Padding | `20px` |
| Hover Border | `#0E7C86` |
| Verified Indicator | Green dot + `#16A34A` left border |
| Tampered Indicator | Red dot + `#DC2626` left border, subtle pulse |

---

# Design Language

- Authoritative & Secure
- Professional / Government-grade
- High Trust
- Minimal Gradient Use
- Flat, Confident Surfaces
- Sharp-but-not-harsh Corners
- Clear Status Signaling (Verified / Tampered / Pending)
- Data-dense but Organized
- Evidence-First Layout
- Dark Mode by Default (reduces eye strain for long document review sessions)
- Inspired by structural logic of modern SaaS dashboards, but visually distinct — no purple/neon AI aesthetic

---

# Design Principles

1. **Documents and cases are the hero.** UI supports verification and investigation work, never distracts from it.
2. **Status must be instantly readable.** Verified vs Tampered vs Pending should be understandable in under a second, from color alone.
3. **Consistent 8px grid** for all spacing.
4. **Accessibility first** — strong contrast, since this may be used in courtrooms, offices, and low-light investigation rooms.
5. **Restrained motion.** Investigators and legal officers need a serious tool, not an animated consumer app.
6. **Gold is used sparingly** — only for legal/authority actions (Admin role, case approval, official seals) so it retains meaning.
7. **Color is functional, not decorative.** Every color maps to a real system state (role, status, alert).

---

> **LexGuard Visual Identity:**  
> A secure, authoritative document management platform with a navy-and-gold identity rooted in legal trust, a steel-teal accent representing the technical security layer (hashing, blockchain, verification), and a disciplined dark interface built for serious investigative and legal work — not a generic AI dashboard.