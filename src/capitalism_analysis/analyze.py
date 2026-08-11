from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Section:
    heading: str
    level: int
    line: int
    text: str


@dataclass(frozen=True)
class Claim:
    id: str
    label: str
    family: str
    kind: str
    status: str
    source_lines: list[int]
    text: str
    supports: list[str]
    challenges: list[str]
    assumptions: list[str]
    falsifier: str


def parse_sections(path: Path) -> list[Section]:
    lines = path.read_text(encoding="utf-8").splitlines()
    hits = [(i + 1, len(m.group(1)), m.group(2).strip())
            for i, line in enumerate(lines)
            if (m := re.match(r"^(#{1,6})\s+(.+?)\s*$", line))]
    sections: list[Section] = []
    for n, (line_no, level, heading) in enumerate(hits):
        start = line_no
        end = hits[n + 1][0] - 1 if n + 1 < len(hits) else len(lines)
        text = "\n".join(lines[start:end]).strip()
        sections.append(Section(heading, level, line_no, text))
    return sections


def _lines(path: Path, start: int) -> list[int]:
    return list(range(start, start + 1))


def seed_claims() -> list[Claim]:
    # These are analytic units, not endorsements. Status says what kind of
    # proposition the entry presents, not whether the proposition is true.
    return [
        Claim("D1", "Capitalism is contested and definitionally plural", "definition", "diagnostic", "framing", [9, 11, 13], "The entry treats capitalism as a disputed concept with competing economic, social-order, and disciplinary definitions.", ["M1", "I1", "P1"], [], ["The entry is selective and aimed at normative philosophy", "Different definitions may not describe the same object"], "Show that the alleged definitions converge on one necessary and sufficient core."),
        Claim("M1", "Marx: accumulation depends on wage labor and private control", "theory", "descriptive", "conditional", [25, 27, 29, 33, 35, 37], "Capitalism is a historically specific social relation in which private control of production, wage labor, commodity exchange, and accumulation form a reinforcing structure.", ["X1", "X2", "X3"], ["H1", "I1", "R1"], ["Labor theory of value", "Workers lack independent access to subsistence", "Competition compels accumulation"], "Find a capitalist regime with the specified wage/property/exchange structure but without the alleged accumulation dynamic, or a non-capitalist regime with the same structure."),
        Claim("W1", "Weber: capitalist durability is culturally motivated", "theory", "causal", "conditional", [43], "Modern capitalism is sustained by an internalized cultural spirit, historically linked to Protestant work and saving, rather than by material relations alone.", ["X2"], ["M1", "S1"], ["Cultural internalization causes durable accumulation", "The Roman case is a meaningful comparison"], "Demonstrate comparable capitalist accumulation without the proposed cultural mechanism, or the mechanism without capitalist accumulation."),
        Claim("S1", "Schumpeter: entrepreneurship drives creative destruction", "theory", "causal", "conditional", [47], "Risk-taking entrepreneurs combine factors of production and drive recurring innovation that displaces older methods and values.", ["X2", "X3"], ["M1"], ["Entrepreneurial agency is analytically distinct from competition", "Innovation produces both abundance and social fatigue"], "Compare innovation regimes with and without entrepreneurial coordination while holding capital, labor, and technology constant."),
        Claim("H1", "Hayek/Friedman: free markets and property yield efficiency", "defense", "normative-causal", "conditional", [51, 83, 95, 113], "Private property and relatively unfettered markets coordinate dispersed information, promote preference satisfaction, and protect economic or political freedom.", ["WEL1", "EFF1", "FRE1", "POL1"], ["M1", "P1", "X1"], ["Prices aggregate relevant information", "Exchange is sufficiently voluntary", "Political power is decentralized rather than concentrated"], "A planner, regulated market, or alternative ownership regime must outperform the market on the specified efficiency/freedom metric under comparable conditions."),
        Claim("I1", "Institutions constitute markets rather than merely constrain them", "theory", "constitutive", "conditional", [55], "Property rights, rule of law, and political institutions are prerequisites of capitalist markets and their healthy operation.", ["H1", "P1"], [], ["Institutional rules are constitutive rather than external", "The relevant institutions can be specified and compared"], "Identify a functioning capitalist market with no legal-political institutional substrate, or show institutions are irrelevant to its performance."),
        Claim("P1", "Polanyi: land, labor, and money are fictitious commodities", "theory", "causal", "conditional", [59, 61, 63], "Generalized markets require state-mediated commodification of things not originally produced as commodities, which generates social countermovements.", ["I1", "X3", "R2"], ["H1", "D1"], ["Commodification requires political action", "Market exposure produces recurring protective responses"], "Find generalized market exchange without state-mediated commodification or without the predicted countermovement."),
        Claim("K1", "Keynes: investment depends on uncertain expectations and liquidity preference", "theory", "causal", "conditional", [69], "Investment and economic reproduction depend on expectations, money, credit, and the choice between productive investment and liquid assets.", ["R1", "EFF1"], ["H1"], ["Liquidity preference is systematically underproductive", "Money is not reducible to a neutral medium"], "Show that investment is governed independently of expectations/liquidity, or that liquidity preference does not affect reproduction under relevant conditions."),
        Claim("WEL1", "Markets can raise welfare and benefit the worst off", "defense", "normative-causal", "conditional", [79], "Competitive markets and division of labor can maximize wealth, with sufficient redistribution or growth reaching everyone, including the worst off.", ["H1", "EFF1"], ["R2", "X2"], ["Growth translates into broad welfare gains", "The comparison class includes viable alternatives"], "A comparable non-market arrangement produces greater welfare for the worst off, or growth systematically fails to reach them."),
        Claim("EFF1", "Markets process dispersed information more effectively than planners", "defense", "epistemic", "conditional", [83], "Market prices and decentralized exchange can coordinate information that no central planner can fully possess.", ["H1"], ["P1", "R2"], ["Relevant information is distributed", "Price signals are not systematically distorted", "Coordination is the correct objective"], "A non-market institution consistently coordinates the same dispersed information better at comparable cost."),
        Claim("FRE1", "Market exchange is voluntary and protects negative liberty", "defense", "normative", "contested", [95], "Markets minimize coercive interference and allow individuals to pursue their own ends.", ["H1", "POL1"], ["X1", "X2"], ["Formal consent tracks substantive freedom", "Workers have reasonable alternatives"], "Show systematic coercion, domination, or lack of meaningful exit within otherwise voluntary market contracts."),
        Claim("POL1", "Economic freedom disperses political power", "defense", "causal", "contested", [113], "Separating economic and political power helps protect political freedom and expression.", ["FRE1"], ["R2", "X2"], ["Economic wealth remains sufficiently dispersed", "Private power does not capture political institutions"], "Show that capitalist economic concentration predictably undermines the fair value of political liberty."),
        Claim("X1", "Capitalism exploits labor through surplus extraction", "critique", "normative-causal", "contested", [153, 157, 159, 163], "Capitalist production extracts value from workers under conditions that may be unequal, unfair, or disrespectfully advantage-taking.", ["M1", "X2", "X3"], ["H1", "N1"], ["The surplus is not justified as rent or entrepreneurial input", "Workers lack meaningful alternatives", "The relevant account of wrongness is specified"], "Show that workers have genuine alternatives and that the residual is justified by a fair account of productive contribution, or reject the proposed wrong-making condition."),
        Claim("X2", "Capitalism structurally dominates workers or producers", "critique", "normative-causal", "contested", [171, 173, 175, 179], "Ownership and market dependence can give employers, capitalists, or impersonal market forces unilateral or arbitrary power over productive activity and subsistence.", ["X1", "R2"], ["H1", "N1"], ["Domination requires meaningful exit/control", "The locus is interactional, structural, dependent, or impersonal"], "Demonstrate reciprocal control, meaningful exit, and non-arbitrary governance across the relevant employment or market relation."),
        Claim("X3", "Capitalism commodifies and destabilizes social reproduction/nature", "critique", "systemic", "conditional", [11, 27, 59, 63], "Market organization depends on care, nature, and political institutions while representing them as autonomous or commodifiable, producing recurring social resistance and ecological strain.", ["M1", "P1"], ["H1", "N1"], ["Dependence is necessary and systemic rather than accidental", "The costs are normatively objectionable"], "Show that capitalist reproduction can be sustained without the alleged externalized care/nature/political supports or that the supports are not harmed."),
        Claim("R1", "Capitalism has endogenous crisis or self-undermining tendencies", "critique", "functional", "conditional", [139], "Capitalist dynamics can undermine the conditions of their own functioning through accumulation, financial instability, unemployment, or underinvestment.", ["M1", "K1", "X3"], ["H1"], ["The system's proper function is independently specified", "The tendency is systematic rather than episodic"], "Show robust counterexamples across capitalist regimes, or specify a stable mechanism that prevents the predicted failure."),
        Claim("R2", "Welfare-state capitalism cannot secure justice", "critique", "normative-causal", "contested", [143, 145, 149], "Large private inequalities can undermine fair opportunity, political equality, reciprocity, and self-respect even when a social minimum is guaranteed.", ["X2", "POL1"], ["WEL1", "H1", "N1"], ["Wealth converts into political influence", "The inequality is institutional rather than contingent", "Justice requires more than a floor"], "Show a welfare-state capitalist arrangement that preserves fair opportunity, political equality, reciprocity, and self-respect despite large private inequality."),
        Claim("N1", "Critiques must establish distinctiveness, causality, systematicity, and perhaps non-contingency", "meta", "methodological", "framing", [135], "A critique of capitalism is stronger when it shows the defect is distinctive to capitalism, caused by it, systematic, and not merely contingent.", ["R1", "R2", "X1", "X2", "X3"], [], ["Capitalism has a stable target definition", "The standards of critique are accepted"], "Show the alleged defect occurs independently of capitalism, or that the critique standards exclude influential critiques without good reason."),
    ]


def claims_by_id(claims: Iterable[Claim]) -> dict[str, Claim]:
    return {c.id: c for c in claims}


def argument_edges(claims: Iterable[Claim]) -> list[dict[str, str]]:
    out = []
    for c in claims:
        for target in c.supports:
            out.append({"source": c.id, "target": target, "relation": "supports"})
        for target in c.challenges:
            out.append({"source": c.id, "target": target, "relation": "challenges"})
    return out


def render_report(claims: list[Claim], sections: list[Section]) -> str:
    count = len(claims)
    contested = sum(c.status == "contested" for c in claims)
    lines = ["# Capitalism: claim and argument map", "", "Source: Stanford Encyclopedia of Philosophy, `source/sep-capitalism.md`.", "", "This is an argument reconstruction, not a truth verdict. `status` records epistemic posture in the entry: framing, conditional, or contested.", "", f"The map contains {count} analytic claims; {contested} are explicitly marked contested.", "", "## Main structural findings", "", "1. The entry does not defend or reject one fully specified object. It begins with definition pluralism (D1), then compares partial models of capitalism.", "2. The strongest positive chain is `I1 → H1 → EFF1/WEL1/FRE1/POL1`: institutions make markets possible; markets are then defended as efficient, welfare-producing, and freedom-preserving.", "3. The strongest critical chain is `M1/P1/K1 → X1/X2/X3/R1/R2`: ownership, commodification, monetary investment, and dependence are used to explain exploitation, domination, externalized reproduction, crisis, and distributive injustice.", "4. Several disputes are not empirical disagreements yet. They are disagreements about the object, the metric, or the wrong-making condition. In particular, `FRE1` and `X2` share facts about employment but use different concepts of freedom.", "5. `N1` is the gatekeeper claim: it asks whether a problem is genuinely a critique of capitalism or merely a critique of one arrangement or component.", "", "## Claims", "", "| ID | Family | Kind | Status | Claim |", "|---|---|---|---|---|"]
    for c in claims:
        lines.append(f"| {c.id} | {c.family} | {c.kind} | {c.status} | {c.text} |")
    lines += ["", "## Falsifier register", "", "Each claim has a proposed falsifier in `data/claims.json`. These are research prompts, not completed tests. The SEP entry itself is a survey and does not supply a matched empirical adjudication for most causal claims.", "", "## Boundary of this analysis", "", "The parser records section structure, but the claim ledger is curated rather than generated by pretending that every sentence is an atomic claim. The next useful extension is source-level passage alignment and an evidence ledger for the cited works."]
    return "\n".join(lines) + "\n"


def write_outputs(source: Path, out_dir: Path) -> None:
    import json
    out_dir.mkdir(parents=True, exist_ok=True)
    sections = parse_sections(source)
    claims = seed_claims()
    (out_dir / "sections.json").write_text(json.dumps([asdict(s) for s in sections], indent=2), encoding="utf-8")
    (out_dir / "claims.json").write_text(json.dumps([asdict(c) for c in claims], indent=2), encoding="utf-8")
    (out_dir / "edges.json").write_text(json.dumps(argument_edges(claims), indent=2), encoding="utf-8")
    lines = ["digraph claims {", "  graph [rankdir=LR];"]
    for c in claims:
        lines.append(f'  {c.id} [label="{c.id}: {c.label}"];')
    for e in argument_edges(claims):
        style = "solid" if e["relation"] == "supports" else "dashed"
        color = "darkgreen" if e["relation"] == "supports" else "firebrick"
        lines.append(f'  {e["source"]} -> {e["target"]} [style={style}, color={color}, label="{e["relation"]}"];')
    lines.append("}")
    (out_dir / "argument-map.dot").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "report.md").write_text(render_report(claims, sections), encoding="utf-8")
