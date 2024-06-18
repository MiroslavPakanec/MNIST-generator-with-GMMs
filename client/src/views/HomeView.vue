<template>
  <div id="container" :style="{ background: gradient }" >
    <div id="navbar" :style="{'width': `${canvasWidth}px`, 'marginTop': `${marginTop}px`}">
      <button class="btn btn-loader" @click="generate(0)" :disabled="isGenerateButtonDisabled">0</button>
      <button class="btn btn-loader" @click="generate(1)" :disabled="isGenerateButtonDisabled">1</button>
      <button class="btn btn-loader" @click="generate(2)" :disabled="isGenerateButtonDisabled">2</button>
      <button class="btn btn-loader" @click="generate(3)" :disabled="isGenerateButtonDisabled">3</button>
      <button class="btn btn-loader" @click="generate(4)" :disabled="isGenerateButtonDisabled">4</button>
      <button class="btn btn-loader" @click="generate(5)" :disabled="isGenerateButtonDisabled">5</button>
      <button class="btn btn-loader" @click="generate(6)" :disabled="isGenerateButtonDisabled">6</button>
      <button class="btn btn-loader" @click="generate(7)" :disabled="isGenerateButtonDisabled">7</button>
      <button class="btn btn-loader" @click="generate(8)" :disabled="isGenerateButtonDisabled">8</button>
      <button class="btn btn-loader" @click="generate(9)" :disabled="isGenerateButtonDisabled">9</button>
      <button class="btn btn-loader" @click="pixelStore.reset()" :disabled="isGenerateButtonDisabled">Reset</button>
    </div>
    <div id="canvas-container" :style="{ 'height': `${canvasHeight}px`}">
      <div id="slider-container" :style="{ 'height': `${canvasHeight}px`}">
        <div id="slider-label-container">
          <p>{{pixelStore.sharpeningTresholds[1]}} - {{pixelStore.sharpeningTresholds[0]}}</p>
        </div>
        <Slider :style="{ 'height': `${canvasHeight}px`}" v-model="pixelStore.sharpeningTresholds" range :min="0" :max="255" orientation="vertical" />
      </div>
      <div id="canvas" :style="{ 'height': `${canvasHeight}px`, 'width': `${canvasWidth}px` }" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import p5 from 'p5'
import Slider from 'primevue/slider';

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
const isGenerateButtonDisabled: ComputedRef<boolean> = computed(() => httpStore.isFetching || pixelStore.isProcessing)

const mouseXPercent: Ref<number> = ref(0)
const mouseYPercent: Ref<number> = ref(0)
const gradient: ComputedRef<string> = computed(() => `radial-gradient(at ${mouseXPercent.value}% ${mouseYPercent.value}%, #F05941, #22092C)`)
  
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
    sketch.background(255,255,255)
    drawPixels(sketch)
  }

  sketch.mouseMoved = () => {
    mouseXPercent.value = clamp(0, sketch.mouseX / canvasWidth.value, 1) * 100
    mouseYPercent.value = clamp(0, sketch.mouseY / canvasHeight.value, 1) * 100
  }
}

const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)

const generate = async (digit: number): Promise<void> => {
  const flatDigit: number[] | undefined = await httpStore.generateDigit(digit)
  if (!flatDigit) return
  pixelStore.setGeneratedPixels(flatDigit)
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
  background: radial-gradient(at center, #db9833, #ff8dc2);
}

#canvas-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  margin: auto;
  gap: 20px;
}

#slider-container {
  width: 100px;
  display: flex;
  align-items: center;justify-content: space-around;
  gap: 20px;
}

#slider-label-container {
  height: 50px;
  width: 200px;
  color: white;
}

#canvas {
  padding: 10px;
  background-color: rgba(255,255,255, 1);
  border-radius: 20px;
  border: 1px solid rgb(51, 152, 219);
  box-sizing: content-box;
}

#navbar {
  margin: auto;
  margin-bottom: 30px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-left: 130px !important;
  padding: 5px;
  gap: 10px;
}

.btn {
  padding: 15px;
  border: 1px solid #cacaca;
  background-color: transparent;
  color: #cacaca;
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
  border: 1px solid white;
  color: #872341;
  background-color: white;
}

.btn:disabled {
  border: 1px solid #4e2c5b;
  color: #4e2c5b;
  background-color: rgba(219, 128, 255, 0.2);
  cursor: not-allowed;
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
