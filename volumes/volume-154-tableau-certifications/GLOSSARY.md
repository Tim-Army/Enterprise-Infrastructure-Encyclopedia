# Volume CLIV — Glossary

| Term | Definition |
|:---|:---|
| **Calculated field** | A derived value defined with Tableau's formula language (e.g. Profit Ratio = SUM(Profit)/SUM(Sales)) — extending the data with the specific metrics an analysis needs. |
| **Certified data source** | A curated, documented, published dataset with metrics defined once, that analysts build on — the organization's single source of truth, preventing inconsistent metric definitions. |
| **Dashboard action** | A user interaction on one view that affects others — filter (click to filter other views), highlight, or navigate — turning a static dashboard into an interactive exploration tool. |
| **Dimension** | A qualitative field (region, product, date) that slices the data into groups — answers "by what?" Contrast measure. |
| **Discrete vs continuous** | Blue (discrete) fields create headers (distinct labeled categories); green (continuous) fields create an axis (an unbroken range). Independent of dimension/measure, and a heavily-tested, commonly-confused distinction. |
| **Extract (.hyper)** | A snapshot of data pulled into Tableau's fast Hyper engine — fast for interaction but only as fresh as the last refresh. Contrast a live connection (always current, source-speed). |
| **LOD expression** | Level-of-Detail expression (FIXED, INCLUDE, EXCLUDE) that computes a measure at a specified aggregation level independent of the view — letting analysis mix levels (e.g. a customer lifetime total on an order-level view). |
| **Measure** | A quantitative field (sales, profit, quantity) that is aggregated (summed, averaged) within the groups dimensions define — answers "how much?" |
| **Relationships** | Tableau's modern data model — defining how tables relate without flattening them, so Tableau joins contextually per visualization and avoids the duplication naive joins cause. |
| **Show Me** | Tableau's panel suggesting appropriate chart types for the selected fields — a nudge toward suitable visualizations. |
| **Story** | A sequence of views/dashboards (story points) that walk a viewer through an analysis in order — for explaining findings persuasively, versus a dashboard's open exploration. |
| **Table calculation** | A calculation on the already-aggregated data in the view (running total, percent of total, rank, moving average) — dependent on partition and order (compute using). |
| **Tableau Prep** | Tableau's dedicated visual data-preparation tool — building a flow of cleaning and shaping steps (a visual ETL pipeline). |
| **Tableau Desktop / Server / Cloud / Public** | The authoring tool (Desktop), the self-hosted sharing/governance platform (Server), its SaaS form (Cloud), and free public hosting (Public). |
| **VizQL** | Tableau's core engine translating fields dragged onto shelves into both a database query and a visual rendering — why building a viz feels like drawing rather than querying. |
