import { defineStore } from "pinia"
import { usePixelStore } from "./pixelStore"
import { Ref, ref } from "vue"

export const useHttpStore = defineStore('http', () => {
    const pixelStore = usePixelStore()

    const isFetching: Ref<boolean> = ref(false)

    const predictDigit = async (): Promise<number | undefined> => {
        const headers = { 'Content-Type': 'application/json' }
        const method = 'POST'
        const body: string = pixelStore.pixelsToString()
        const options = { headers, method, body }
        const url: string = process.env.VUE_APP_PREDICT_ENDPOINT_URL
        const response: any = await request(url, options, 'Failed to predict digit.')
        if (response.error === undefined) return response.prediction
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
            return { error: errorMessage ?? error.message ?? 'Something went wrong' }
        } finally {
            isFetching.value = false
        }
    }

    return { predictDigit, isFetching }
})
