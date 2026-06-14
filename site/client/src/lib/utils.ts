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

/** 賽前倒數狀態。根據 kickoff_utc 與當前時間，回傳供「即將開賽 / 進行中 / 已結束」標記用的資訊。
 *  - phase: upcoming（未開賽）| live（開賽後 ~2.5h 內，視為進行中）| past（已結束）| unknown（無 kickoff_utc）
 *  - msToKick: 距離開賽的毫秒數（負值代表已開賽）
 *  - label: 繁中倒數標籤，例如「3 小時後開賽」「12 分鐘後開賽」「進行中」
 *  - soon: 是否在 24 小時內開賽（用於置頂與醒目標記） */
export interface CountdownInfo {
  phase: "upcoming" | "live" | "past" | "unknown";
  msToKick: number;
  label: string;
  soon: boolean;
}

const LIVE_WINDOW_MS = 2.5 * 60 * 60 * 1000; // 開賽後 2.5 小時內視為進行中

export function countdown(
  f: { kickoff_utc?: string },
  now: number = Date.now()
): CountdownInfo {
  if (!f.kickoff_utc) {
    return { phase: "unknown", msToKick: Infinity, label: "", soon: false };
  }
  const kick = new Date(f.kickoff_utc).getTime();
  if (isNaN(kick)) {
    return { phase: "unknown", msToKick: Infinity, label: "", soon: false };
  }
  const ms = kick - now;
  if (ms <= 0) {
    if (-ms <= LIVE_WINDOW_MS) {
      return { phase: "live", msToKick: ms, label: "進行中", soon: false };
    }
    return { phase: "past", msToKick: ms, label: "已開賽", soon: false };
  }
  const soon = ms <= 24 * 60 * 60 * 1000;
  const totalMin = Math.floor(ms / 60000);
  const days = Math.floor(totalMin / (60 * 24));
  const hours = Math.floor((totalMin % (60 * 24)) / 60);
  const mins = totalMin % 60;
  let label: string;
  if (days >= 1) {
    label = hours > 0 ? `${days} 天 ${hours} 小時後開賽` : `${days} 天後開賽`;
  } else if (hours >= 1) {
    label = mins > 0 ? `${hours} 小時 ${mins} 分鐘後開賽` : `${hours} 小時後開賽`;
  } else {
    label = `${Math.max(mins, 1)} 分鐘後開賽`;
  }
  return { phase: "upcoming", msToKick: ms, label, soon };
}
