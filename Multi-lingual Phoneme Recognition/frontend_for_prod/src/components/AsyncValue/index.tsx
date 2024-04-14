"use client"

import { useEffect, useState } from "react"

interface AsyncProps<T> {
    value: Promise<T>
}

export function AsyncValue<T>(props: AsyncProps<T>) {
    const [value, setValue] = useState<T>()
    useEffect(()=>{props.value.then(setValue)},[props])
    return <>{value}</>
}