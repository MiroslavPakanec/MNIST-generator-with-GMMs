<template>
  <div id="container" :style="{ background: gradient }" >
    <div id="navbar" :style="{'width': `${canvasWidth}px`, 'marginTop': `${marginTop}px`}">
      <button class="btn" @click="reset()">Reset</button>
      <button class="btn btn-loader" @click="predict()" :disabled="isPredictButtonDisabled">
        <span v-if="showLoader" class="loader"></span>
        {{ predictButtonText }}
      </button>
      <button class="btn" @click="copy()">{{ copyButtonText }}</button>
      <span v-if="prediction !== undefined" id="prediction">Prediction: {{ prediction }}</span>
    </div>
    <div id="canvas" :style="{ 'height': `${canvasHeight}px`, 'width': `${canvasWidth}px` }" />
  </div>
</template>

<script lang="ts" setup>
import p5 from 'p5'
import { ComputedRef, Ref, computed, onMounted, ref } from 'vue'
import { usePixelStore } from '@/stores/pixelStore'
import { useHttpStore } from '@/stores/httpStore'

const pixelStore = usePixelStore()
const httpStore = useHttpStore()

const brushDiameter: Ref<number> = ref(20)
const canvasPercent: Ref<number> = ref(0.6)
const canvasWidth: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const canvasHeight: Ref<number> = ref(window.innerHeight * canvasPercent.value)
const marginTop: ComputedRef<number> = computed(() => (window.innerHeight / 2) - (canvasHeight.value / 2))
const copyButtonText: Ref<string> = ref('Copy')
const predictButtonText: ComputedRef<string> = computed(() => httpStore.isFetching ? 'Predicting...' : 'Predict')
const isPredictButtonDisabled: ComputedRef<boolean> = computed(() => httpStore.isFetching)
const showLoader: ComputedRef<boolean> = computed(() => httpStore.isFetching)

const isLmbPressed: Ref<boolean> = ref(false)
const mouseXPercent: Ref<number> = ref(0)
const mouseYPercent: Ref<number> = ref(0)
const gradient: ComputedRef<string> = computed(() => `radial-gradient(at ${mouseXPercent.value}% ${mouseYPercent.value}%, #3498db, #9b59b6)`)
const prediction: Ref<string | undefined> = ref(undefined)
  
const getMouseX = (sketch: any): number => sketch.mouseX - (canvasWidth.value / 2)
const getMouseY = (sketch: any): number => sketch.mouseY - (canvasHeight.value / 2)

const skipRender = (sketch: any): boolean => {
  const r: number = brushDiameter.value / 2
  if (sketch.mouseX - r >= canvasWidth.value) return true
  if (sketch.mouseX + r <= 0) return true
  if (sketch.mouseY - r >= canvasHeight.value) return true
  if (sketch.mouseY + r <= 0) return true
  return false
}

const drawCursor = (sketch: any): void => {
  sketch.strokeWeight = 1
  sketch.fill(255,255,255)
  sketch.ellipse(getMouseX(sketch), getMouseY(sketch), brushDiameter.value, brushDiameter.value)
}

const drawPixels = (sketch: any): void => {
  sketch.stroke(150, 150, 150)
  sketch.strokeWeight = 1
  for (let i = 0; i < pixelStore.pixels.length; i++) {
    const row = pixelStore.pixels[i]
    for (let j = 0; j < row.length; j++) {
      const pixel: number = row[j]
      sketch.fill(pixel, pixel, pixel)
      const w: number = canvasWidth.value / 28
      const h: number = w
      const x: number = (w * i) - (canvasHeight.value / 2)
      const y: number = (h * j) - (canvasHeight.value / 2)
      sketch.rect(x, y, w, h)
    }
  }
}

const sketch = (sketch: any) => {
  sketch.setup = () => {
    sketch.createCanvas(canvasWidth.value, canvasHeight.value, sketch.WEBGL)
    pixelStore.reset()
  }

  sketch.windowResized = () => {
    canvasWidth.value = window.innerHeight * canvasPercent.value
    canvasHeight.value = window.innerHeight * canvasPercent.value
  }

  sketch.draw = () => {
    if (skipRender(sketch)) return
    if (isLmbPressed.value) pixelStore.draw(sketch.mouseX, sketch.mouseY, brushDiameter.value, canvasWidth.value)
    sketch.background(255,255,255)
    drawPixels(sketch)
    drawCursor(sketch)
  }

  sketch.mousePressed = () => {
    if (sketch.mouseButton === sketch.LEFT) isLmbPressed.value = true
  }

  sketch.mouseReleased = () => {
    if (sketch.mouseButton === sketch.LEFT) isLmbPressed.value = false
  }

  sketch.mouseMoved = () => {
    mouseXPercent.value = clamp(0, sketch.mouseX / canvasWidth.value, 1) * 100
    mouseYPercent.value = clamp(0, sketch.mouseY / canvasHeight.value, 1) * 100
  }
}

const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)

const predict = async (): Promise<void> => {
  const result: number | undefined = await httpStore.predictDigit()
  const resultStr: string = result === undefined ? 'Unknown' : result.toString()
  prediction.value = resultStr
}

const copy = async (): Promise<void> => {
  const pixels: string = pixelStore.pixelsToString()
  await navigator.clipboard.writeText(pixels)
  copyButtonText.value = 'Copied!'
  setTimeout(() => {
    copyButtonText.value = 'Copy';
  }, 2000);
}

const reset = () => {
  pixelStore.reset()
  prediction.value = undefined
}

onMounted(() => {
  const sketch_element = document.getElementById('canvas')
  if (sketch_element === null) return
  new p5(sketch, sketch_element)
})
</script>

<style scoped>
#container {
  height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  background: rgb(155, 89, 182);
  background: radial-gradient(at center, rgb(51, 152, 219), #9b59b6);
}

#canvas {
  padding: 10px;
  background-color: rgba(255,255,255, 1);
  border-radius: 20px;
  border: 1px solid rgb(51, 152, 219);
  margin: auto;
  cursor: none;
}

#navbar {
  margin: auto;
  margin-bottom: 10px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 5px;
  gap: 10px;
}

.btn {
  padding: 15px;
  border: 1px solid white;
  background-color: transparent;
  color: white;
  border-radius: 5px;
  height: 50px;
}

.btn-loader {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.btn:hover {
  cursor: pointer;
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
}

.btn:disabled {
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
  cursor: not-allowed;
}

.btn.active {
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
}

#prediction { 
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
  border-radius: 5px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  padding-left: 10px;
  padding-right: 10px;
}

.loader {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: inline-block;
  border-top: 1px solid #FFF;
  border-right: 1px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after {
  content: '';  
  box-sizing: border-box;
  position: absolute;
  left: 0;
  top: 0;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border-bottom: 1px solid #4e2c5b;
  border-left: 1px solid transparent;
}
@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
} 


</style>
