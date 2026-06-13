// Map team names to ISO country codes → flag emoji
const CODES: Record<string, string> = {
  Mexico: "MX", "South Africa": "ZA", "South Korea": "KR", "Czech Republic": "CZ",
  Canada: "CA", "Bosnia & Herzegovina": "BA", Qatar: "QA", Switzerland: "CH",
  Brazil: "BR", Morocco: "MA", Haiti: "HT", Scotland: "GB-SCT",
  USA: "US", Paraguay: "PY", Australia: "AU", Turkey: "TR",
  Germany: "DE", Curacao: "CW", "Ivory Coast": "CI", Ecuador: "EC",
  Netherlands: "NL", Japan: "JP", Sweden: "SE", Tunisia: "TN",
  Belgium: "BE", Egypt: "EG", Iran: "IR", "New Zealand": "NZ",
  Spain: "ES", "Cape Verde": "CV", "Saudi Arabia": "SA", Uruguay: "UY",
  France: "FR", Senegal: "SN", Iraq: "IQ", Norway: "NO",
  Argentina: "AR", Algeria: "DZ", Austria: "AT", Jordan: "JO",
  Portugal: "PT", "DR Congo": "CD", Uzbekistan: "UZ", Colombia: "CO",
  England: "GB-ENG", Croatia: "HR", Ghana: "GH", Panama: "PA",
};

// Traditional Chinese team names
export const ZH: Record<string, string> = {
  Mexico: "墨西哥", "South Africa": "南非", "South Korea": "南韓", "Czech Republic": "捷克",
  Canada: "加拿大", "Bosnia & Herzegovina": "波黑", Qatar: "卡塔爾", Switzerland: "瑞士",
  Brazil: "巴西", Morocco: "摩洛哥", Haiti: "海地", Scotland: "蘇格蘭",
  USA: "美國", Paraguay: "巴拉圭", Australia: "澳洲", Turkey: "土耳其",
  Germany: "德國", Curacao: "庫拉索", "Ivory Coast": "象牙海岸", Ecuador: "厄瓜多爾",
  Netherlands: "荷蘭", Japan: "日本", Sweden: "瑞典", Tunisia: "突尼西亞",
  Belgium: "比利時", Egypt: "埃及", Iran: "伊朗", "New Zealand": "紐西蘭",
  Spain: "西班牙", "Cape Verde": "佛得角", "Saudi Arabia": "沙特", Uruguay: "烏拉圭",
  France: "法國", Senegal: "塞內加爾", Iraq: "伊拉克", Norway: "挪威",
  Argentina: "阿根廷", Algeria: "阿爾及利亞", Austria: "奧地利", Jordan: "約旦",
  Portugal: "葡萄牙", "DR Congo": "剛果民主", Uzbekistan: "烏茲別克", Colombia: "哥倫比亞",
  England: "英格蘭", Croatia: "克羅地亞", Ghana: "加納", Panama: "巴拿馬",
  TBD: "待定",
};

export function flag(team: string): string {
  const code = CODES[team];
  if (!code) return "🏳️";
  // Special sub-flags (Scotland/England) have no clean emoji on all platforms; use generic
  if (code === "GB-SCT") return "🏴󠁧󠁢󠁳󠁣󠁴󠁿";
  if (code === "GB-ENG") return "🏴󠁧󠁢󠁥󠁮󠁧󠁿";
  return code
    .toUpperCase()
    .replace(/./g, (c) => String.fromCodePoint(127397 + c.charCodeAt(0)));
}

export function zh(team: string): string {
  return ZH[team] || team;
}
