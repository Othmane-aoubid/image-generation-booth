<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <header class="border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-purple-500">Image Generation</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <div v-if="processedImage" class="mb-8">
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold">Generated Image</h2>
            <button
              @click="processedImage = null"
              class="text-gray-400 hover:text-white"
            >
              <span class="material-icons">close</span>
            </button>
          </div>
          <div class="relative">
            <img
              :src="processedImage"
              alt="Generated Image"
              class="w-full rounded-lg"
            />
          </div>
          <div class="mt-4 text-sm text-gray-400">
            <p>Model: {{ selectedModel }}</p>
          </div>
        </div>
      </div>

      <ImageGrid 
        @model-selected="handleModelSelect" 
        :showCamera="showCamera"
        @close-camera="showCamera = false"
      />

      <!-- Camera Modal -->
      <div v-if="showCamera" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50">
        <div class="absolute inset-0 flex items-center justify-center p-4">
          <div class="bg-gray-800 rounded-xl w-full max-w-4xl">
            <div class="p-6">
              <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-semibold">Take Photo</h2>
                <button 
                  @click="showCamera = false"
                  class="text-gray-400 hover:text-white"
                >
                  <span class="material-icons">close</span>
                </button>
              </div>
              <CameraCapture 
                @image-captured="handleImageCapture"
                :selectedModel="selectedModel"
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref } from "vue";
import ImageGrid from "./components/ImageGrid.vue";
import CameraCapture from "./components/CameraCapture.vue";

export default {
  name: "App",
  components: {
    ImageGrid,
    CameraCapture,
  },
  setup() {
    const processedImage = ref(null);
    const selectedModel = ref("");
    const showCamera = ref(false);

    const handleModelSelect = (modelId) => {
      selectedModel.value = modelId;
      showCamera.value = true;
    };

    const generateImage = async (initImage) => {
      try {
        const response = await fetch("http://localhost:5000/generate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: selectedModel.value,
            init_image: initImage,
          }),
        });

        const data = await response.json();
        processedImage.value = data.image;
        showCamera.value = false;
      } catch (error) {
        console.error("Error generating image:", error);
      }
    };

    const handleImageCapture = async (data) => {
      processedImage.value = data.dataUrl;
      try {
        await generateImage(data.dataUrl);
      } catch (error) {
        console.error("Error processing image:", error);
      }
    };

    return {
      processedImage,
      selectedModel,
      showCamera,
      handleModelSelect,
      handleImageCapture,
    };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', sans-serif;
  background-color: #111827;
}

.material-icons {
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
}
</style>