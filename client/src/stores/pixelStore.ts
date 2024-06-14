import { defineStore } from "pinia"
import { Ref, ref } from "vue"

export const usePixelStore = defineStore('pixels', () => {
    const dim: Ref<number> = ref(28)
    const pixels: Ref<number[][]> = ref([])

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

    // mx: Mouse X coord
    // my: Mouse Y coord
    // d: brush diameter
    // w: Canvas width
    const draw = (mx: number, my: number, d: number, w: number): void => {
        const n = dim.value
        const pixelSize = w / n
        const r: number = d / 2
        const startX: number = Math.max(0, Math.floor((mx - r) / pixelSize))
        const endX: number = Math.min(n, Math.ceil((mx + r) / pixelSize))
        const startY: number = Math.max(0, Math.floor((my - r) / pixelSize))
        const endY: number = Math.min(n, Math.ceil((my + r) / pixelSize))
      
        for (let i = startX; i <= endX; i++) {
          for (let j = startY; j <= endY; j++) {
            if (i < 0 || i >= n || j < 0 || j >= n) continue
            pixels.value[i][j] -= 20
            pixels.value[i][j] = clamp(pixels.value[i][j], 0, 255)    
          }
        }
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

    const flatten = (pixels: number[][]): number[] => {
        const flat: number[] = []
        for (let i = 0; i <= 27; i++) {
            for (let j = 0; j <= 27; j++) {
                flat.push(pixels[j][i]);
            }
        }
        return flat
    }

    const pixelsToString = (): string => {
        const inverted: number[][] = invert(pixels.value)
        const flattened: number[] = flatten(inverted)
        return JSON.stringify(flattened)
    }

    const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)
    
    return { pixels, reset, draw, invert, flatten, pixelsToString }
})