const MINUTE = 60
const HOUR = MINUTE * 60
const DAY = HOUR * 24
const WEEK = DAY * 7
const MONTH = DAY * 30

export function absround(num: number): number {
    return Math.round(Math.abs(num))
}


export function dateToText(timestamp: number): string {
    // inspired by https://github.com/premii/hn/blob/76ba1721f0ca5dead6fe9ac62afdf42911ebc244/a/js/helper.js#L292
    const now = Date.now() / 1000
    const diff = now - timestamp
    if (diff <= 60) {
        return diff / 60 + " seconds"
    }
    if (diff < HOUR) {
        const value = absround(diff / MINUTE)
        return value + " min" + (value === 1 ? "" : "s")
    }
    if (diff < DAY) {
        const value = absround(diff / HOUR)
        return value + " hr" + (value === 1 ? "" : "s")
    }
    if (diff < MONTH) {
        const value = absround(diff / DAY)
        return value + " day" + (value === 1 ? "" : "s")
    }
    const date = new Date(timestamp * 1000)
    return date.toLocaleString()
}

// @ts-ignore
export const isInStandaloneMode = () => ('standalone' in window.navigator) && (window.navigator.standalone);
