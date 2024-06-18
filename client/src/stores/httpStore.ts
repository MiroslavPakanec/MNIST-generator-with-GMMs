import { defineStore } from "pinia"
import { usePixelStore } from "./pixelStore"
import { Ref, ref } from "vue"

export const useHttpStore = defineStore('http', () => {
    const pixelStore = usePixelStore()

    const isFetching: Ref<boolean> = ref(false)

    const generateDigit = async (digit: number): Promise<number[] | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'GET'
        const options = { headers, method }
        const url = `${process.env.VUE_APP_GENERATE_ENDPOINT_URL}?label=${digit}`
        const response: any = await request(url, options, 'Failed to generate digit.')
        if (response.error === undefined) return response
        alert(response.error)
        return undefined
    }

    const request = async (url: string, options: any, errorMessage?: string): Promise<any> => {
        try {
            isFetching.value = true
            const response: any = await fetch(url, options)
            if (response?.ok) return await response.json()
            else return { error: (await response.json())?.error ?? errorMessage ?? 'Something went wrong' }
        } catch (error: any) {
            console.log(error)
            return { error: errorMessage ?? error.message ?? 'Something went wrong' }
        } finally {
            isFetching.value = false
        }
    }

    return { generateDigit: generateDigit, isFetching }
})
