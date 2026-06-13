export function stageZh(stage: string): string {
  if (stage.startsWith("Group ")) return "小組賽 " + stage.replace("Group ", "");
  const map: Record<string, string> = {
    "Round of 32": "32強",
    "Round of 16": "16強",
    "Quarter-final": "八強",
    "Semi-final": "四強",
    "Third Place": "季軍戰",
    "Final": "決賽",
  };
  return map[stage] || stage;
}

export function outcomeZh(o: string): string {
  return { home: "主勝", draw: "和局", away: "客勝" }[o] || o;
}
