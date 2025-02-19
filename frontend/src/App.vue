<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <header class="border-b border-gray-800">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <h1 class="text-2xl font-bold text-purple-500">Image Generation</h1>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-6">
      <ImageGrid 
        @model-selected="handleModelSelect" 
        :showCamera="showCamera"
        @close-camera="showCamera = false"
      />

      <div v-if="processedImage" class="mt-8">
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

      <!-- Camera Modal -->
      <div v-if="showCamera && !isGenerating" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50">
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

      <!-- Loading Modal -->
      <div v-if="isGenerating" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50">
        <div class="absolute inset-0 flex items-center justify-center p-4">
          <div class="bg-gray-800 rounded-xl w-full max-w-xl p-8">
            <div class="flex flex-col items-center justify-center">
              <div class="w-16 h-16 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p class="text-purple-400 text-lg">Generating your image...</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref } from "vue";
import { useToast } from "vue-toastification";
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
    const isGenerating = ref(false);
    const toast = useToast();

    const handleModelSelect = (modelId) => {
      selectedModel.value = modelId;
      showCamera.value = true;
    };

    const handleImageCapture = async (data) => {
      try {
        showCamera.value = false;
        isGenerating.value = true;

        // Convert base64 to blob
        const response = await fetch(data.dataUrl);
        const blob = await response.blob();

        // Create FormData
        const formData = new FormData();
        formData.append("image", blob, "image.jpg");
        formData.append("model_id", selectedModel.value);

        // Send to backend
        const apiResponse = await fetch("http://localhost:5000/generate", {
          method: "POST",
          body: formData,
        });

        const result = await apiResponse.json();
        
        if (!apiResponse.ok || !result.success) {
          throw new Error(result.error || "Failed to process image");
        }

        processedImage.value = result.image;
        toast.success("Image generated successfully!");
      } catch (error) {
        console.error("Error processing image:", error);
        toast.error(error.message || "Failed to process image. Please try again.");
      } finally {
        isGenerating.value = false;
      }
    };

    return {
      processedImage,
      selectedModel,
      showCamera,
      isGenerating,
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