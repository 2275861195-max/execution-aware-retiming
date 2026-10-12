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
                     "svg.hashsalt": "execution-aware-retiming",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.labelcolor": INK, "text.color": INK})


def save(fig, name):
    fig.savefig(OUT / f"{name}.png", dpi=180, bbox_inches="tight", facecolor="white")
    svg = StringIO()
    fig.savefig(svg, format="svg", bbox_inches="tight", facecolor="white", metadata={"Date": None})
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


def overview(data, diagnostic):
    fig = plt.figure(figsize=(16, 10))
    grid = fig.add_gridspec(3, 2, height_ratios=[1.25, 1, 1], hspace=.58, wspace=.26)
    ax = fig.add_subplot(grid[0, :])
    ax.set(xlim=(0, 16), ylim=(0, 3.5))
    ax.axis("off")
    ax.set_title("A  Frozen policy → temporal accelerator → future stability layer", loc="left", weight="bold")
    blocks = [(.1, 1.45, 2, 1, "Observation\n+ robot state", False),
              (2.8, 1.45, 2, 1, "Frozen π0.5\n10-action chunk", False),
              (5.5, 1.45, 2.3, 1, "Existing accelerator\nsource-time mapping", False),
              (8.5, 1.1, 4, 1.7, "PROPOSED stability plug-in\nMonitor: mechanism-dependent signal\nCorrector: minimal intervention", True),
              (13.2, 1.45, 2.6, 1, "Controller + robot\nphysical interaction", False)]
    for x, y, w, h, label, future in blocks:
        patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.03", linewidth=1.7,
                               edgecolor=INK, facecolor="#fff2d8" if future else "#e5f0f2",
                               linestyle="--" if future else "-")
        patch.set_sketch_params(1, 100, 2)
        ax.add_patch(patch)
        ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=11)
    for a, b in zip(blocks, blocks[1:]):
        ax.annotate("", xy=(b[0]-.07, 1.95), xytext=(a[0]+a[2]+.07, 1.95),
                    arrowprops={"arrowstyle":"->", "color":INK, "lw":1.8})
    ax.annotate("", xy=(10.5, 1.02), xytext=(14.5, 1.35),
                arrowprops={"arrowstyle":"->", "color":INK, "connectionstyle":"angle,angleA=-90,angleB=0,rad=8"})
    ax.text(12.7, .55, "Execution feedback\nDeployable signals not yet fixed", ha="center", fontsize=10)
    for y, indices, label, color in [(0.77, range(10), "1×: unit source intervals", BLUE),
                                      (.32, ["[0,3)", "[3,6)", "[6,9)"], "3×: compressed intervals", RED)]:
        ax.text(.1, y, label, va="center", fontsize=10)
        for i, index in enumerate(indices):
            spacing = .3 if y > .5 else .9
            width = spacing-.07
            x = 2.85+i*spacing
            ax.add_patch(FancyBboxPatch((x, y-.13), width, .26, boxstyle="round,pad=.01", facecolor=color, edgecolor="white"))
            ax.text(x+width/2, y, str(index), ha="center", va="center", color="white", fontsize=8)
    ax.text(6.2, .12, "Mapping illustration only—not a measured trajectory or full retimer specification", fontsize=9)
    ax = fig.add_subplot(grid[1, 0])
    speeds = [float(row["setting"].split("-")[1]) for row in data]
    sr = [float(row["SR"]) for row in data]
    ax.plot(speeds, sr, "o-", color=BLUE, lw=2)
    for x, y in zip(speeds, sr):
        ax.annotate(f"{y:.2f}%", (x, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=10)
    ax.set(title="B  Requested acceleration vs reliability", xlabel="Requested factor (×)", ylabel="Success (%)", ylim=(0, 112), xticks=speeds)
    ax = fig.add_subplot(grid[1, 1])
    actual = [float(row["paired_median_speedup"]) for row in data]
    ax.plot(actual, sr, "o-", color=RED, lw=2)
    for x, y, speed in zip(actual, sr, speeds):
        ax.annotate(f"{speed:g}×", (x, y), xytext=(-25, 8), textcoords="offset points", fontsize=10)
    ax.set(title="C  Realized speed gain saturates", xlabel="Paired median speedup (×)", ylabel="Success (%)", ylim=(0, 112), xlim=(.93, 1.63))
    ax = fig.add_subplot(grid[2, 0])
    metrics = list(diagnostic.values())
    names = ["Direction\nchange", "Requested\nbound excess", "EEF path\nefficiency"]
    for offset, column, label, color in [(-.18, "failure_median", "Failure (N=31)", RED), (.18, "success_median", "Success (N=19)", BLUE)]:
        values = [float(row[column]) for row in metrics]
        positions = [i+offset for i in range(3)]
        ax.bar(positions, values, width=.34, color=color, label=label)
        for x, y in zip(positions, values):
            ax.text(x, y+.02, f"{y:g}", ha="center", fontsize=9)
    ax.set(title="D  Exploratory RT3 proxies—not causes", ylabel="Median", ylim=(0, 1.13), xticks=range(3), xticklabels=names)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.text(.5, -.33, "First 100 steps / 5 s; task-level counterexamples exist\nCompare outcomes within each metric only", transform=ax.transAxes, ha="center", fontsize=9)
    ax = fig.add_subplot(grid[2, 1])
    ax.set(xlim=(0, 10), ylim=(0, 5))
    ax.axis("off")
    ax.set_title("E  Proposed control—not a completed experiment", loc="left")
    for x, y, label in [(1.6, 4.05, "S1-Q10\nRaw ten-step prefix"), (8.2, 4.05, "S1-Q3\nRaw a0–a2; re-query"), (5, 1.1, "S3-Q3\nCompressed execution")]:
        ax.text(x, y, label, ha="center", va="center", fontsize=11,
                bbox={"boxstyle":"round,pad=.45", "fc":"#e5f0f2", "ec":INK})
    for start, end in [((3, 4.05), (6.65, 4.05)), ((7.6, 3.3), (5.8, 1.95)), ((2.2, 3.3), (4.2, 1.95))]:
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle":"->", "color":INK})
    ax.text(4.9, 4.75, "Cadence / prefix effects", ha="center", fontsize=9)
    ax.text(8, 2.3, "Compression at\nmatched cadence", ha="center", fontsize=9)
    ax.text(1.6, 2.3, "Both change", ha="center", fontsize=9)
    ax.text(5, -.25, "Task4 counterexample • 20 outcome-independent init × 3 conditions", ha="center", fontsize=9)
    fig.suptitle("Towards stable temporal acceleration: evidence → diagnosis → intervention", fontsize=20, weight="bold", y=.99)
    fig.text(.06, .005, "Aggregate observations supplied by authors; no uncertainty estimates. Proposed plug-in is not implemented or validated.", fontsize=10)
    save(fig, "research_overview")


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
    overview(data, diagnostic)
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
