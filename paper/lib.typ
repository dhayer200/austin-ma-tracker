// Paper template, adapted from the polymath template used in chalkIQ.

#let _accent = rgb("#2E5FA3")

#let template(doc) = {
  set text(font: "New Computer Modern", size: 9.5pt, fallback: true)
  set page(
    paper: "us-letter",
    margin: (top: 1.0in, bottom: 1.0in, left: 1.1in, right: 1.1in),
    numbering: "1",
  )
  set par(leading: 0.7em, spacing: 1.1em, justify: true)
  set heading(numbering: "1.")
  show heading.where(level: 1): it => {
    v(0.6em)
    text(fill: _accent, weight: 700, size: 1.25em, it.body)
    v(0.2em)
  }
  show heading.where(level: 2): it => {
    v(0.4em)
    text(fill: _accent, weight: 700, size: 1.05em, it.body)
  }
  show link: it => text(fill: _accent, it)
  doc
}

#let header(title, author, date, topic) = [
  #text(fill: _accent, weight: 700, size: 1.4em, title)
  #v(0.2em)
  #grid(
    columns: (1fr, 1fr),
    align: (left, right),
    text(size: 0.95em)[#author \ #topic],
    text(size: 0.95em)[#date],
  )
  #v(0.6em)
  #line(length: 100%, stroke: 0.5pt + _accent)
  #v(0.2em)
]

#let abstract(body) = {
  v(0.6em)
  block(
    width: 100%,
    inset: (x: 0.6em, y: 0.5em),
    [
      #text(fill: _accent, weight: 700)[Abstract.] #body
    ]
  )
  v(0.6em)
}

#let fig(path, caption) = figure(
  image(path, width: 95%),
  caption: caption,
)
