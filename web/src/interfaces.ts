export interface Item {
    id: number
    type: string
    by: string
    time: number
    url: string
    score: number
    title: string
    // parts: ??
    deleted: boolean

    text?: string   // HTML
    dead?: boolean
    parent?: number
    poll?: number
    kids?: Item[]
    descendants?: number
}

export interface ReaderData {
    status: number
    html: string
    title: string
    language: string
    date: any //TODO
    authors: string[]
    url: string
    image?: string
    native_ad: boolean
}
