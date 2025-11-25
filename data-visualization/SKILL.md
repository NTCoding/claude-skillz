---
name: Data Visualization
description: "Comprehensive data visualization skill covering visual execution and technical implementation. Includes perceptual foundations, chart selection, layout algorithms, and library guidance. Load on-demand when building charts, graphs, dashboards, or any visual data representation."
version: 1.0.0
---

# Data Visualization

Visualization is communication. Every visual element must serve understanding.

## Critical Rules

🚨 **Use established algorithms.** Graph layout, tree layout, spatial indexing—these problems are solved. Check dagre, d3-force, ELK.js before implementing anything custom.

🚨 **Choose encodings by perceptual accuracy.** Position beats length beats angle beats area beats color. Prefer bar charts over pie charts over bubble charts.

🚨 **Never rely on color alone.** 8% of men are colorblind. Use shape, pattern, or labels as backup encoding.

🚨 **Match rendering to scale.** SVG for <1000 elements, Canvas for 1000-10000, WebGL for >10000.

---

## 1. Visual Encoding

### Marks & Channels

**Marks** are geometric primitives representing data:
- Points (scatter plots, dot plots)
- Lines (line charts, network edges)
- Areas (bar charts, area charts, maps)

**Channels** are visual properties applied to marks:
- Position (x, y coordinates)
- Size (length, area, volume)
- Color (hue, saturation, lightness)
- Shape (circle, square, triangle)
- Orientation (angle, slope)

### Cleveland & McGill Hierarchy (1984)

Visual encodings ranked by perceptual accuracy:

1. **Position along common scale** (most accurate)
2. Position on non-aligned scales
3. Length
4. Angle/slope
5. Area
6. Volume
7. **Color saturation/hue** (least accurate)

**Implication:** Bar charts (position) > pie charts (angle) > bubble charts (area)

### Preattentive Attributes

Properties processed in <250ms without conscious effort:
- Color (hue, saturation)
- Form (orientation, length, width, size, shape)
- Spatial position
- Motion

Use preattentive attributes for the most important data—they "pop out" automatically.

### Channel Effectiveness by Data Type

| Data Type | Best Channels |
|-----------|---------------|
| Quantitative | Position, length, angle, area |
| Ordinal | Position, density, saturation |
| Categorical | Shape, hue, spatial region |

---

## 2. Interaction Design

### Shneiderman's Mantra (1996)

"Overview first, zoom and filter, then details on demand"

1. **Overview** — Show entire dataset, establish context
2. **Zoom & Filter** — Reduce complexity, focus on subset
3. **Details on Demand** — Tooltips, click-to-expand, drill-down

### Interaction Patterns

| Pattern | Use Case |
|---------|----------|
| Brushing & linking | Cross-highlighting across coordinated views |
| Focus + context | Fisheye lens, detail-on-demand panels |
| Direct manipulation | Drag nodes, resize elements, reorder |
| Animated transitions | Help users track changes between states |
| Pan & zoom | Navigate large visualizations |
| Filtering | Reduce data to relevant subset |
| Selection | Highlight specific data points |

---

## 3. Chart Selection

### By Question Type

| Question | Chart Type | Why |
|----------|------------|-----|
| How do values compare? | Bar chart | Position encoding is most accurate |
| How has this changed over time? | Line chart | Shows trends, handles many points |
| What's the distribution? | Histogram, box plot | Shows spread, outliers, shape |
| What's the relationship? | Scatter plot | Reveals correlation, clusters |
| What's the part-to-whole? | Stacked bar, treemap | Shows composition |
| What are the connections? | Network graph, Sankey | Shows relationships, flows |
| What's the hierarchy? | Tree, sunburst, treemap | Shows parent-child structure |
| Where is it? | Choropleth, symbol map | Geographic context |

### By Data Volume

| Volume | Approach |
|--------|----------|
| <20 points | Simple charts, direct labeling |
| 20-500 | Standard visualization |
| 500-5000 | Consider aggregation, filtering |
| 5000+ | Aggregation mandatory, or Canvas/WebGL |

### Common Anti-Patterns

- ❌ Pie charts with >5 slices (use bar chart)
- ❌ 3D charts without strong justification
- ❌ Dual-axis with unrelated scales (misleading)
- ❌ Non-zero baselines for bar charts (distorts perception)
- ❌ Truncated axes without clear indication

---

## 4. Color

### Palette Types

| Type | Use Case | Examples |
|------|----------|----------|
| Sequential | Low to high values | Blues, Greens, Viridis |
| Diverging | Values diverge from midpoint | RdBu, BrBG, Spectral |
| Categorical | Distinct categories | Set2, Tableau10, Category10 |

### Colorblind Safety

- 8% of men, 0.5% of women have color vision deficiency
- **Never rely on color alone**—use shape, pattern, labels
- Safe sequential: viridis, cividis, plasma
- Safe categorical: ColorBrewer's colorblind-safe options
- Test with: Coblis, Sim Daltonism, Chrome DevTools

### Perceptual Uniformity

- **Avoid rainbow colormaps** (jet)—perceptual steps are uneven
- Use viridis, parula, cividis for sequential data
- These ensure equal perceptual distance between values

### Color Guidelines

- 4.5:1 contrast ratio for text (WCAG AA)
- 3:1 contrast for UI components
- Max 7-10 distinct categorical colors
- Use saturation/lightness variation for emphasis

---

## 5. Layout Algorithms

🚨 **Before implementing ANY layout algorithm, check if a library exists.**

### Algorithm → Library Mapping

| Problem | Algorithm | Libraries |
|---------|-----------|-----------|
| Layered/DAG graphs | Sugiyama (1981) | dagre, ELK.js |
| Force-directed networks | Fruchterman-Reingold (1991) | d3-force, Cytoscape.js |
| Tree layouts | Reingold-Tilford (1981) | d3-hierarchy |
| Treemaps | Squarified (2000) | d3-hierarchy, ECharts |
| Circle packing | Wang (2006) | d3-hierarchy |
| Sankey diagrams | — | d3-sankey |
| Chord diagrams | — | d3-chord |
| Large graphs (10k+) | WebGL + spatial indexing | Sigma.js, G6, deck.gl |
| Spatial queries | Quadtree, R-tree | d3-quadtree, rbush |
| Edge crossing minimization | Barth (2002) | Built into dagre/ELK |

### When to Use Each Layout

| Layout | Best For |
|--------|----------|
| Sugiyama (dagre) | Flowcharts, dependency graphs, DAGs with direction |
| Force-directed | Social networks, organic relationships, exploration |
| Tree | Hierarchies with single parent per node |
| Treemap | Hierarchies with quantitative values |
| Circular | Emphasizing central nodes, ring structures |
| Matrix | Dense graphs where edges would overlap |

**These problems are solved. Never implement from scratch.**

---

## 6. Rendering & Performance

### Rendering Technology Thresholds

```
<1000 elements    → SVG
                    - DOM events work naturally
                    - Accessibility (ARIA) supported
                    - Crisp at any zoom level
                    - CSS styling

1000-10000        → Canvas
                    - Batch rendering
                    - Manual hit testing required
                    - Lower memory footprint
                    - requestAnimationFrame for animation

>10000            → WebGL
                    - GPU acceleration
                    - Sigma.js, deck.gl, regl
                    - Complex setup
                    - Limited text rendering
```

### Performance Patterns

| Pattern | When to Use |
|---------|-------------|
| Web Workers | Layout computation (never block main thread) |
| Spatial indexing | Hit detection with quadtree/R-tree |
| Level-of-detail | Simplify distant/small elements |
| Viewport culling | Only render visible elements |
| Debouncing | Expensive interactions (zoom, filter) |
| Virtualization | Long lists of chart components |
| Aggregation | Too many data points to render individually |

### Anti-Patterns

- ❌ 5000 SVG nodes (use Canvas)
- ❌ Layout computation on main thread
- ❌ Hit testing without spatial indexing
- ❌ Rendering off-screen elements
- ❌ Animating thousands of elements individually

---

## 7. Libraries

### Graph Layouts

| Library | Best For | Notes |
|---------|----------|-------|
| dagre | Layered DAGs, flowcharts | Sugiyama algorithm, good defaults |
| dagre-d3 | dagre + D3 rendering | SVG output |
| ELK.js | Complex layouts, compound graphs | Eclipse Layout Kernel, highly configurable |
| d3-force | Organic networks | Fruchterman-Reingold, customizable forces |
| Cytoscape.js | Graph analysis + visualization | Rich algorithm library |
| Sigma.js | Large graphs (10k+) | WebGL rendering |
| G6/AntV | Enterprise graphs | Full-featured, Chinese ecosystem |
| vis-network | Quick prototypes | Easy API, limited customization |

### Charting

| Library | Best For | Notes |
|---------|----------|-------|
| D3.js | Custom, highly interactive | Low-level, maximum control |
| Observable Plot | Quick exploration | D3 team, excellent defaults |
| Recharts | React integration | Declarative, composable |
| Victory | React integration | Animation support |
| ECharts | Feature-rich dashboards | Great mobile, large dataset support |
| Vega-Lite | Grammar of graphics | Declarative JSON spec |
| Chart.js | Simple charts | Easy setup, limited customization |
| Plotly | Scientific visualization | 3D support, interactivity |

### When to Use D3 vs Higher-Level Libraries

**Use D3 when:**
- Need complete control over rendering
- Building novel/custom visualizations
- Integrating with existing SVG/Canvas code
- Performance-critical with custom optimizations

**Use higher-level libraries when:**
- Standard chart types suffice
- Faster development time matters
- Team less experienced with D3
- Need built-in responsiveness/animation

---

## 8. Composition & Layout

### Project Composition (Dashboard Level)

- **Visual hierarchy** — Guide eye to most important first
- **Grid systems** — Align elements for coherence
- **Grouping** — Related visualizations together
- **White space** — Breathing room, not wasted space
- **Reading flow** — Z-pattern or F-pattern for Western audiences

### Chart Composition (Single Chart)

| Element | Guidelines |
|---------|------------|
| Title | Clear, descriptive; top-left or centered above |
| Subtitle | Additional context; smaller, below title |
| Axes | Labeled with units; tick marks at meaningful intervals |
| Legend | Embedded when possible; external if complex |
| Aspect ratio | Affects slope perception; 45° banking for trends |
| Margins | Enough for labels; consistent across charts |

### Aspect Ratio Guidelines

- **Line charts:** ~16:9 for trends (banking to 45°)
- **Bar charts:** Depends on number of bars
- **Scatter plots:** Often square (1:1) for correlation
- **Maps:** Preserve geographic proportions

---

## 9. Annotation

### Annotation Types

| Type | Purpose |
|------|---------|
| Title | The "what" — identifies the visualization |
| Subtitle | Additional context, data source |
| Caption | The "so what" — key insight or takeaway |
| Axis labels | Variable names and units |
| Legend | Decode color/shape/size mappings |
| Callouts | Highlight specific data points |
| Reference lines | Benchmarks, targets, averages |
| Source citation | Data provenance |

### Best Practices

- **Annotate the insight, not just the data** — "Sales peaked in Q3" not just "Sales over time"
- **Use callouts sparingly** — Highlight 1-3 key points maximum
- **Direct labeling** — Embed labels in chart when possible (vs separate legend)
- **Provide context** — Benchmarks, historical reference, targets
- **Layer information** — Overview visible, details on interaction

### Text Hierarchy

1. Title (largest, boldest)
2. Subtitle/caption
3. Axis titles
4. Tick labels
5. Annotations
6. Source (smallest)

---

## 10. Accessibility

### WCAG Requirements

- **AA minimum** (AAA preferred)
- 4.5:1 contrast ratio for normal text
- 3:1 contrast for large text and UI components
- No information conveyed by color alone

### Keyboard Navigation

- Tab through interactive elements
- Arrow keys for traversing data points
- Enter/Space for selection
- Escape to cancel/close

### Screen Reader Support

```html
<svg role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Monthly Sales 2024</title>
  <desc id="chart-desc">Bar chart showing sales increasing from $10M in January to $15M in December</desc>
</svg>
```

- Use ARIA labels and roles
- Provide text alternatives
- Announce dynamic updates with live regions
- Structure for logical reading order

### Alternative Representations

- **Data tables** — Provide as fallback for all charts
- **Text summaries** — Describe key insights
- **Sonification** — Audio representation for time-series
- **Tactile graphics** — For physical accessibility

---

## 11. Anti-Patterns Summary

### Design Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do |
|--------------|----------------|------------|
| 3D charts | Distorts perception | Use 2D |
| Pie >5 slices | Hard to compare | Use bar chart |
| Dual unrelated axes | Misleading correlation | Separate charts |
| Non-zero baseline | Exaggerates differences | Start at zero |
| Rainbow colormap | Perceptually uneven | Use viridis |
| Color-only encoding | Excludes colorblind | Add shape/pattern |
| Chart junk | Distracts from data | Remove decoration |
| Overplotting | Hides data density | Aggregate or jitter |

### Implementation Anti-Patterns

| Anti-Pattern | Why It's Wrong | What to Do |
|--------------|----------------|------------|
| Custom graph layout | Reinventing solved problem | Use dagre/ELK |
| 5000 SVG nodes | Poor performance | Use Canvas |
| Main thread layout | Blocks UI | Use Web Worker |
| No spatial indexing | Slow hit detection | Use quadtree |
| Rendering off-screen | Wasted computation | Viewport culling |

---

## 12. Academic Foundations

### Seminal Papers

| Paper | Year | Contribution |
|-------|------|--------------|
| Cleveland & McGill "Graphical Perception" | 1984 | Visual encoding hierarchy |
| Shneiderman "The Eyes Have It" | 1996 | Overview-zoom-filter-details mantra |
| Gansner et al. "Drawing Directed Graphs" | 1993 | Foundation for dagre |
| Fruchterman & Reingold "Force-directed Placement" | 1991 | Foundation for d3-force |
| Sugiyama et al. "Hierarchical Systems" | 1981 | Layered graph layout |
| Barth et al. "Bilayer Cross Counting" | 2002 | Edge crossing minimization |
| Brewer "Color Use Guidelines" | 1994 | ColorBrewer palettes |

### Essential Resources

| Resource | Type | Focus |
|----------|------|-------|
| ColorBrewer (colorbrewer2.org) | Tool | Accessible color palettes |
| From Data to Viz (data-to-viz.com) | Guide | Chart selection decision tree |
| Visualization Analysis & Design (Munzner) | Textbook | Comprehensive theory |
| Data Visualisation (Kirk) | Textbook | Practitioner guide |
| Visual Display of Quantitative Information (Tufte) | Textbook | Data-ink ratio, chart junk |
| D3 Gallery (observablehq.com/@d3/gallery) | Examples | Implementation patterns |

---

## Summary

🚨 **Before implementing visualization:**

1. **What question are you answering?** → Select chart type
2. **What's your data volume?** → Select rendering technology
3. **Is there an established algorithm?** → Use the library
4. **Is it accessible?** → Color, keyboard, screen reader
5. **Does it follow perceptual best practices?** → Encoding hierarchy
