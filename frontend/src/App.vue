<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-gray-900">Image Generation</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <div v-if="processedImage" class="mb-8">
        <div class="bg-white rounded-lg shadow-lg p-4">
          <h2 class="text-xl font-semibold mb-4">Generated Image</h2>
          <div class="relative">
            <img 
              :src="processedImage" 
              alt="Generated Image"
              class="w-full rounded-lg shadow-md"
            />
            <button 
              @click="processedImage = null"
              class="absolute top-2 right-2 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100"
            >
              <span class="material-icons">close</span>
            </button>
          </div>
          <div class="mt-4 text-sm text-gray-600">
            <p>Model: {{ currentModel?.name }}</p>
          </div>
        </div>
      </div>
      
      <ImageGrid @image-captured="handleImageCapture" />
      <CameraCapture @image-captured="handleImageCapture" />
    </main>
  </div>
</template>

<script>
import ImageGrid from './components/ImageGrid.vue'
import CameraCapture from './components/CameraCapture.vue'

export default {
  name: 'App',
  components: {
    ImageGrid,
    CameraCapture
  },
  data() {
    return {
      processedImage: null,
      currentModel: null
    }
  },
  methods: {
    async handleImageCapture(data) {
      // Show the captured image immediately
      this.processedImage = data.dataUrl;
      this.currentModel = data.model;

      try {
        // TODO: Send to backend for processing
        // const response = await fetch('/api/process', {
        //   method: 'POST',
        //   body: data.formData
        // });
        // const result = await response.json();
        // this.processedImage = result.imageUrl;
      } catch (error) {
        console.error('Error processing image:', error);
      }
    }
  }
}
</script>

<style scoped>
/* No styles defined */
</style>
