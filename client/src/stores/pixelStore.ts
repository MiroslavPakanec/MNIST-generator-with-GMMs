import { defineStore } from "pinia"
import { Ref, ref } from "vue"

export const usePixelStore = defineStore('pixels', () => {
    const dim: Ref<number> = ref(28)
    const pixels: Ref<number[][]> = ref([])
    const isProcessing: Ref<boolean> = ref(false)
    const sharpeningTresholds: Ref<[number, number]> = ref([100, 220]) 


    const reset = (): void => {
        const matrix: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
              row.push(255)
            }
            matrix.push(row)
        }
        pixels.value = matrix
    }

    const invert = (pixels: number[][]): number[][] => {
        const inverted: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                row.push(255 - pixels[i][j])
            }
            inverted.push(row)
        }
        return inverted
    }

    const scale = (pixels: number[][]): number[][] => {
        const scaled: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                const value: number = Math.round(clamp(pixels[i][j], 0, 255))
                row.push(value)
            }
            scaled.push(row)
        }
        return scaled
    }

    const sharpen = (pixels: number[][], top_treshold: number, bottom_treshold: number): number[][] => {
        const sharpened: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                if (pixels[i][j] > top_treshold) row.push(255)
                else if (pixels[i][j] < bottom_treshold) row.push(0)
                else row.push(pixels[i][j])
            }
            sharpened.push(row)
        }
        return sharpened
    }

    const rotate = (pixels: number[][]): number[][] => {
        const rotated: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                row.push(pixels[j][i])
            }
            rotated.push(row)
        }
        return rotated
    }

    const reshape = (pixels: number[]): number[][] => {
        if (pixels.length !== dim.value * dim.value) throw 'Attempting to process digit with invalid dimentions'
        const processedDigit: number[][] = []
        let rowIndex = 0;
        let row: number[] = []
        for (const pixel of pixels) {
            if (rowIndex >= dim.value) {
                processedDigit.push(row)
                rowIndex = 0
                row = []
            }
            row.push(pixel)
            rowIndex += 1
        }
        processedDigit.push(row)
        return processedDigit
    }

    const setGeneratedPixels = (rawPixels: number[]): void => {
        isProcessing.value = true
        const reshaped: number[][] = reshape(rawPixels)
        const scaled: number[][] = scale(reshaped)
        const inverted: number[][] = invert(scaled)
        const rotated: number[][] = rotate(inverted)
        const sharpened: number[][] = sharpen(rotated, sharpeningTresholds.value[1], sharpeningTresholds.value[0])
        isProcessing.value = false
        pixels.value = sharpened
    }

    const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)
    
    return { pixels, reset, setGeneratedPixels, isProcessing, sharpeningTresholds }
})