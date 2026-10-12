"""Regenerate public aggregate plots and editable conceptual diagrams."""
import csv
from io import StringIO
from pathlib import Path
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
BLUE, RED, INK = "#256f85", "#b45b4c", "#24333e"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.labelcolor": INK, "text.color": INK})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    svg = StringIO()
    fig.savefig(svg, format="svg", bbox_inches="tight", facecolor="white")
    (OUT / f"{name}.svg").write_text("\n".join(line.rstrip() for line in svg.getvalue().splitlines()) + "\n")
    plt.close(fig)


def diagram(name, title, nodes, edges, note):
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set(xlim=(0, 12), ylim=(0, 5.5))
    ax.axis("off")
    ax.text(0.3, 5.15, title, fontsize=20, weight="bold")
    model = ET.Element("mxGraphModel", page="1", pageWidth="1200", pageHeight="550")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    for i, (x, y, w, h, label, future) in enumerate(nodes):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.04",
                             facecolor="#f0f5f5" if not future else "#fff5e4",
                             edgecolor=INK, linewidth=1.6, linestyle="--" if future else "-")
        box.set_sketch_params(scale=1, length=100, randomness=2)
        ax.add_patch(box)
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=12)
        cell = ET.SubElement(root, "mxCell", id=f"n{i}", value=label,
                             style=f"rounded=1;whiteSpace=wrap;html=0;sketch=1;comic=1;fontSize=16;fillColor={'#fff5e4' if future else '#f0f5f5'};dashed={int(future)};",
                             vertex="1", parent="1")
        ET.SubElement(cell, "mxGeometry", x=str(x*100), y=str((5.5-y-h)*100),
                      width=str(w*100), height=str(h*100), **{"as": "geometry"})
    for j, (a, b, label) in enumerate(edges):
        x, y, w, h, *_ = nodes[a]
        bx, by, bw, bh, *_ = nodes[b]
        center, target = (x+w/2, y+h/2), (bx+bw/2, by+bh/2)
        dx, dy = target[0]-center[0], target[1]-center[1]
        source_scale = .5 / max(abs(dx)/w, abs(dy)/h)
        target_scale = .5 / max(abs(dx)/bw, abs(dy)/bh)
        start = (center[0]+dx*source_scale, center[1]+dy*source_scale)
        end = (target[0]-dx*target_scale, target[1]-dy*target_scale)
        ax.annotate("", xy=end, xytext=start,
                    arrowprops={"arrowstyle": "->", "color": INK, "lw": 1.5,
                                "shrinkA": 5, "shrinkB": 5})
        if label:
            ax.text((start[0]+end[0])/2, (start[1]+end[1])/2+.15,
                    label.replace("Compression at matched cadence", "Compression at\nmatched cadence"), ha="center", fontsize=10,
                    bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})
        cell = ET.SubElement(root, "mxCell", id=f"e{j}", value=label,
                             style="edgeStyle=orthogonalEdgeStyle;rounded=1;sketch=1;endArrow=block;html=0;",
                             edge="1", parent="1", source=f"n{a}", target=f"n{b}")
        ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    ax.text(.3, .2, note, fontsize=11)
    for ident, text, y in [("title", title, 0), ("note", note, 510)]:
        cell = ET.SubElement(root, "mxCell", id=ident, value=text, vertex="1", parent="1",
                             style="text;html=0;whiteSpace=wrap;fontSize=18;align=left;")
        ET.SubElement(cell, "mxGeometry", x="30", y=str(y), width="1140", height="40", **{"as":"geometry"})
    ET.ElementTree(model).write(OUT / f"{name}.drawio", encoding="utf-8", xml_declaration=True)
    save(fig, name)


def main():
    OUT.mkdir(exist_ok=True)
    with (ROOT / "data/aggregated/overall_tradeoff.csv").open() as file:
        data = list(csv.DictReader(file))
    speeds = [float(row["setting"].split("-")[1]) for row in data]
    sr = [float(row["SR"]) for row in data]
    actual = [float(row["paired_median_speedup"]) for row in data]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(speeds, sr, "o-", color=BLUE, linewidth=2)
    for x, y in zip(speeds, sr):
        ax.annotate(f"{y:.2f}%", (x, y), xytext=(0, 9), textcoords="offset points", ha="center")
    ax.set(xlabel="Requested temporal acceleration (×)", ylabel="Success rate (%)",
           title="Reliability falls under aggressive acceleration", ylim=(0, 110), xticks=speeds)
    save(fig, "speed_reliability_curve")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(actual, sr, "o-", color=BLUE, linewidth=2)
    for i, (x, y) in enumerate(zip(actual, sr)):
        ax.annotate(f"RT-{speeds[i]:.1f}", (x, y), xytext=(-45, 8), textcoords="offset points")
    ax.set(xlabel="Achieved paired median speedup (×)", ylabel="Success rate (%)",
           title="Observed speed–reliability operating points", ylim=(0, 110), xlim=(.9, 1.65))
    fig.subplots_adjust(bottom=.23)
    fig.text(.12, .01, "Paired eligible episodes; no uncertainty estimates shown.", fontsize=10)
    save(fig, "speed_reliability_pareto")
    labels = {
        "query_boundary_translation_direction_change_proxy": "Direction-change proxy",
        "requested_translation_bound_excess_fraction": "Requested bound excess",
        "eef_path_efficiency": "EEF path efficiency",
    }
    with (ROOT / "data/aggregated/exploratory_instability_summary.csv").open() as file:
        diagnostic = {row["metric"]: row for row in csv.DictReader(file)
                      if row["scope"] == "selected_tasks"}
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (metric, label) in zip(axes, labels.items()):
        row = diagnostic[metric]
        values = [float(row["failure_median"]), float(row["success_median"])]
        ax.bar(["Failure", "Success"], values, color=[RED, BLUE], width=.55)
        ax.set(title=label, ylabel="Median", ylim=(0, max(values)*1.3))
        for i, value in enumerate(values):
            ax.text(i, value, f"{value:g}", ha="center", va="bottom")
    fig.suptitle("Exploratory RT3: first 100 control steps / 5 seconds", fontsize=17)
    fig.text(.5, .01, "N=31 failures / 19 successes • association only • task-level counterexamples exist", ha="center", fontsize=11)
    fig.tight_layout(rect=(0, .06, 1, .92))
    save(fig, "diagnostic_proxy_summary")
    diagram("hypothesis_space", "Four competing mechanisms — no winner selected", [
        (.5, 3, 4.8, 1.2, "H1  Motion realization distortion\nCommands ≠ physical motion", False),
        (6.5, 3, 4.8, 1.2, "H2  Cross-query commitment\nIntent changes across queries", False),
        (.5, 1.1, 4.8, 1.2, "H3  Interaction completion\nMotion advances before contact completes", False),
        (6.5, 1.1, 4.8, 1.2, "H4  Object deviation / failed recovery\nPerturbed state → unstable continuation", False)], [],
        "Hypotheses may coexist. Proxy associations do not establish causal ordering.")
    diagram("causal_control_design", "Separate compression from cadence / prefix effects", [
        (.5, 3.4, 3.2, 1.1, "S1-Q10\n1× • raw ten-step prefix", False),
        (8.2, 3.4, 3.2, 1.1, "S1-Q3\n1× • raw a0–a2; re-query", False),
        (4.3, 1.1, 3.2, 1.1, "S3-Q3\n3× • compressed execution", False)],
        [(0, 1, "Tests cadence / prefix effects"), (1, 2, "Compression at matched cadence"),
         (0, 2, "Current comparison:\nchanges both")],
        "Proposed task4 study: outcome-independent init; no causal mechanism established yet.")
    diagram("stability_plugin_concept", "Existing accelerator + proposed stability plug-in", [
        (.2, 3.1, 2, 1.2, "Frozen π0.5\nAction chunk", False),
        (2.9, 3.1, 2, 1.2, "Existing\naccelerator", False),
        (5.7, 2.9, 3.2, 1.6, "FUTURE stability plug-in\nMonitor / Corrector\nUnder investigation", True),
        (9.6, 3.1, 2, 1.2, "Robot\nexecution", False),
        (5.7, 1, 3.2, .8, "Execution feedback\nSignals to be determined", True)],
        [(0, 1, ""), (1, 2, ""), (2, 3, ""), (3, 4, ""), (4, 2, "")],
        "Concept only, not implemented. Privileged simulator state is diagnostic ground truth.")


if __name__ == "__main__":
    main()
