import { clsx } from 'clsx';
import type { ClassValue } from 'clsx';
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

const WEEKDAY_ZH = ["日", "一", "二", "三", "四", "五", "六"];

/** 將 fixture 的開賽時間轉成香港時間顯示。
 *  優先用 kickoff_utc（精確），否則退回 date + kickoff_local（不轉時區）。 */
export function kickoffHkt(
  f: { kickoff_utc?: string; date: string; kickoff_local: string },
  opts: { withWeekday?: boolean; withYear?: boolean } = {}
): string {
  if (f.kickoff_utc) {
    try {
      const d = new Date(f.kickoff_utc);
      const date = d.toLocaleDateString("zh-HK", {
        timeZone: "Asia/Hong_Kong",
        ...(opts.withYear ? { year: "numeric" } : {}),
        month: "2-digit",
        day: "2-digit",
      });
      const time = d.toLocaleTimeString("zh-HK", {
        timeZone: "Asia/Hong_Kong",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      });
      if (opts.withWeekday) {
        const dayIdx = new Date(
          d.toLocaleString("en-US", { timeZone: "Asia/Hong_Kong" })
        ).getDay();
        return `${date}（${WEEKDAY_ZH[dayIdx]}）${time}`;
      }
      return `${date} ${time}`;
    } catch {
      /* fall through */
    }
  }
  return `${f.date.slice(5)} ${f.kickoff_local}`;
}
